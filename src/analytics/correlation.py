"""Correlation validation — objective-level diversification assessment.

Instead of asking "are the stress group tags correct?", this asks:

1. Does the STABILISER actually stabilise? (low/negative correlation to
   compounders during equity stress)
2. Does OPTIONALITY provide crisis alpha? (negative correlation to equities
   in stress, or at minimum much lower loss)
3. Within COMPOUNDERS, is diversification real? (how correlated are the
   components — true vs false diversification)
4. Are any supposedly-independent positions actually the same bet?

The stress_correlation_group tag validation is retained as implementation
detail that feeds back into classification accuracy.

Strategy reference: current-finances/strategy-assumptions.md §7
"""

import logging
from dataclasses import dataclass, field

import pandas as pd

from src.db.connection import get_connection
from src.portfolio.valuation import PortfolioValuation

logger = logging.getLogger(__name__)


@dataclass
class PairCorrelation:
    ticker_a: str
    ticker_b: str
    role_a: str | None
    role_b: str | None
    group_a: str | None
    group_b: str | None
    same_group: bool
    corr_60d: float | None
    corr_252d: float | None
    corr_stress: float | None
    overlap_days: int
    flag: str | None = None
    detail: str = ""


@dataclass
class RoleDiversification:
    """How well-diversified is a capital role internally?"""
    role: str
    member_count: int
    avg_intra_corr_60d: float | None
    avg_intra_corr_stress: float | None
    highest_pair: str
    highest_corr: float | None
    assessment: str   # "well-diversified", "moderate", "concentrated", "false diversification"
    detail: str


@dataclass
class CrossRoleAssessment:
    """Does one role protect against another in stress?"""
    role_a: str
    role_b: str
    avg_cross_corr_stress: float | None
    assessment: str   # "protective", "neutral", "co-moving", "unknown"
    detail: str


@dataclass
class GroupValidation:
    group_name: str
    tickers: list[str]
    avg_intra_corr_stress: float | None
    min_intra_corr: float | None
    weakest_pair: str
    valid: bool
    detail: str


@dataclass
class CorrelationReport:
    # Objective-level assessments (headline)
    stabiliser_protects: CrossRoleAssessment | None = None
    optionality_performs: CrossRoleAssessment | None = None
    compounder_diversity: RoleDiversification | None = None
    # Supporting detail
    role_diversifications: list[RoleDiversification] = field(default_factory=list)
    cross_role_assessments: list[CrossRoleAssessment] = field(default_factory=list)
    pair_results: list[PairCorrelation] = field(default_factory=list)
    group_validations: list[GroupValidation] = field(default_factory=list)
    ungrouped_high_corr: list[PairCorrelation] = field(default_factory=list)
    analysis_window_days: int = 0
    stress_periods_used: int = 0


def _load_price_series(db_path=None) -> dict[str, pd.Series]:
    with get_connection(db_path) as conn:
        rows = conn.execute("""
            SELECT i.ticker, p.date, p.close_price
            FROM prices p
            JOIN instruments i ON i.id = p.instrument_id
            JOIN holdings h ON h.instrument_id = i.id
            ORDER BY i.ticker, p.date
        """).fetchall()
    series: dict[str, list] = {}
    for r in rows:
        t = r["ticker"]
        if t not in series:
            series[t] = {"dates": [], "prices": []}
        series[t]["dates"].append(r["date"])
        series[t]["prices"].append(r["close_price"])
    result: dict[str, pd.Series] = {}
    for t, data in series.items():
        result[t] = pd.Series(data["prices"], index=pd.DatetimeIndex(data["dates"]), name=t)
    return result


def _compute_returns(prices: dict[str, pd.Series]) -> pd.DataFrame:
    import numpy as np
    df = pd.DataFrame(prices).ffill(limit=5)
    return np.log(df / df.shift(1)).dropna(how="all")


def _identify_stress_periods(returns: pd.DataFrame, threshold: float = -0.15) -> pd.Series:
    candidates = ["VAS.AX", "BHP.AX", "VGS.AX", "SOL.AX"]
    proxy = None
    for c in candidates:
        if c in returns.columns:
            proxy = c
            break
    if proxy is None:
        return pd.Series(False, index=returns.index)
    cum = returns[proxy].rolling(60, min_periods=20).sum()
    return cum < threshold


def _get_classifications(db_path=None) -> dict[str, dict]:
    """Get role and stress group for each held instrument."""
    with get_connection(db_path) as conn:
        rows = conn.execute("""
            SELECT i.ticker, ic.capital_role, ic.stress_correlation_group
            FROM instruments i
            JOIN holdings h ON h.instrument_id = i.id
            LEFT JOIN instrument_classifications ic ON ic.instrument_id = i.id
        """).fetchall()
    return {r["ticker"]: {
        "role": r["capital_role"],
        "group": r["stress_correlation_group"],
    } for r in rows}


def compute_correlations(
    pv: PortfolioValuation, window: int = 252,
    stress_only: bool = False, db_path=None,
) -> CorrelationReport:
    report = CorrelationReport(analysis_window_days=window)

    prices = _load_price_series(db_path)
    if len(prices) < 2:
        return report

    returns = _compute_returns(prices)
    classifications = _get_classifications(db_path)
    stress_mask = _identify_stress_periods(returns)
    report.stress_periods_used = int(stress_mask.sum())

    tickers = sorted(returns.columns.tolist())

    # Compute all pairwise correlations
    for i, ta in enumerate(tickers):
        for tb in tickers[i + 1:]:
            pair = returns[[ta, tb]].dropna()
            if len(pair) < 30:
                continue

            ca = classifications.get(ta, {})
            cb = classifications.get(tb, {})
            group_a = ca.get("group")
            group_b = cb.get("group")
            role_a = ca.get("role")
            role_b = cb.get("role")
            same_group = group_a is not None and group_b is not None and group_a == group_b

            corr_full = (pair[ta].rolling(window).corr(pair[tb]).iloc[-1]
                         if len(pair) >= window else pair[ta].corr(pair[tb]))
            corr_60 = pair[ta].iloc[-60:].corr(pair[tb].iloc[-60:]) if len(pair) >= 60 else None
            stress_pair = pair[stress_mask.reindex(pair.index, fill_value=False)]
            corr_stress = stress_pair[ta].corr(stress_pair[tb]) if len(stress_pair) >= 20 else None

            ref_corr = corr_stress if corr_stress is not None else corr_full
            flag, detail = None, ""
            if same_group and ref_corr is not None and ref_corr < 0.5:
                flag = "over-grouped"
                detail = (
                    f"{ta}–{tb} grouped in '{group_a}' but stress correlation is {ref_corr:.2f}. "
                    f"They provide more diversification than assumed."
                )
            elif not same_group and ref_corr is not None and ref_corr > 0.7:
                flag = "under-grouped"
                ga, gb = group_a or "none", group_b or "none"
                detail = (
                    f"{ta}–{tb} in different groups ({ga} / {gb}) but stress correlation "
                    f"is {ref_corr:.2f}. They are effectively the same bet in a crisis."
                )

            pc = PairCorrelation(
                ticker_a=ta, ticker_b=tb,
                role_a=role_a, role_b=role_b,
                group_a=group_a, group_b=group_b,
                same_group=same_group,
                corr_60d=corr_60,
                corr_252d=corr_full if window == 252 else None,
                corr_stress=corr_stress,
                overlap_days=len(pair),
                flag=flag, detail=detail,
            )
            report.pair_results.append(pc)
            if flag == "under-grouped":
                report.ungrouped_high_corr.append(pc)

    # === OBJECTIVE-LEVEL ASSESSMENTS ===
    _assess_cross_role(report, "stabiliser", "compounder", "stabiliser_protects")
    _assess_cross_role(report, "optionality", "compounder", "optionality_performs")
    _assess_intra_role(report, "compounder", "compounder_diversity")
    _assess_intra_role(report, "stabiliser", None)
    _assess_intra_role(report, "optionality", None)

    # === GROUP VALIDATION (supporting detail) ===
    _validate_groups(report, classifications)

    return report


def _assess_cross_role(
    report: CorrelationReport, role_a: str, role_b: str, attr_name: str,
) -> None:
    """Assess whether role_a protects against role_b in stress."""
    cross_pairs = [
        p for p in report.pair_results
        if (p.role_a == role_a and p.role_b == role_b)
        or (p.role_a == role_b and p.role_b == role_a)
    ]

    stress_corrs = [p.corr_stress for p in cross_pairs if p.corr_stress is not None]
    avg_stress = sum(stress_corrs) / len(stress_corrs) if stress_corrs else None

    if avg_stress is None:
        assessment = CrossRoleAssessment(
            role_a=role_a, role_b=role_b,
            avg_cross_corr_stress=None,
            assessment="unknown",
            detail=f"Insufficient data to measure {role_a}–{role_b} stress correlation.",
        )
    elif avg_stress < -0.2:
        assessment = CrossRoleAssessment(
            role_a=role_a, role_b=role_b,
            avg_cross_corr_stress=avg_stress,
            assessment="protective",
            detail=(
                f"{role_a.title()} is negatively correlated with {role_b} in stress "
                f"(avg {avg_stress:.2f}). It actively offsets losses — functioning as designed."
            ),
        )
    elif avg_stress < 0.3:
        assessment = CrossRoleAssessment(
            role_a=role_a, role_b=role_b,
            avg_cross_corr_stress=avg_stress,
            assessment="neutral",
            detail=(
                f"{role_a.title()}–{role_b} stress correlation is {avg_stress:.2f}. "
                f"Provides diversification but doesn't actively offset losses."
            ),
        )
    else:
        assessment = CrossRoleAssessment(
            role_a=role_a, role_b=role_b,
            avg_cross_corr_stress=avg_stress,
            assessment="co-moving",
            detail=(
                f"WARNING: {role_a.title()} co-moves with {role_b} in stress "
                f"(avg {avg_stress:.2f}). It does NOT provide the protection it was "
                f"designed for. When compounders fall, {role_a} falls too."
            ),
        )

    report.cross_role_assessments.append(assessment)
    setattr(report, attr_name, assessment)


def _assess_intra_role(
    report: CorrelationReport, role: str, attr_name: str | None,
) -> None:
    """Assess diversification within a capital role."""
    intra_pairs = [
        p for p in report.pair_results
        if p.role_a == role and p.role_b == role
    ]

    tickers = set()
    for p in intra_pairs:
        tickers.add(p.ticker_a)
        tickers.add(p.ticker_b)

    if len(tickers) < 2:
        rd = RoleDiversification(
            role=role, member_count=len(tickers),
            avg_intra_corr_60d=None, avg_intra_corr_stress=None,
            highest_pair="N/A", highest_corr=None,
            assessment="N/A",
            detail=f"Only {len(tickers)} {role} instrument(s) — diversification not applicable.",
        )
        report.role_diversifications.append(rd)
        if attr_name:
            setattr(report, attr_name, rd)
        return

    corr_60s = [p.corr_60d for p in intra_pairs if p.corr_60d is not None]
    stress_corrs = [p.corr_stress for p in intra_pairs if p.corr_stress is not None]
    avg_60 = sum(corr_60s) / len(corr_60s) if corr_60s else None
    avg_stress = sum(stress_corrs) / len(stress_corrs) if stress_corrs else None

    # Find highest correlated pair
    ref_pairs = [(p, p.corr_stress if p.corr_stress is not None else p.corr_60d)
                  for p in intra_pairs]
    ref_pairs = [(p, c) for p, c in ref_pairs if c is not None]

    if ref_pairs:
        hp, hc = max(ref_pairs, key=lambda x: x[1])
        highest_pair = f"{hp.ticker_a}–{hp.ticker_b} ({hc:.2f})"
        highest_corr = hc
    else:
        highest_pair, highest_corr = "N/A", None

    ref = avg_stress if avg_stress is not None else avg_60
    if ref is None:
        assessment_str = "unknown"
        detail = f"Insufficient data to assess {role} diversification."
    elif ref < 0.2:
        assessment_str = "well-diversified"
        detail = (
            f"{role.title()} holdings have avg stress correlation {ref:.2f}. "
            f"Genuinely different bets — losses in one are unlikely to coincide with others."
        )
    elif ref < 0.5:
        assessment_str = "moderate"
        detail = (
            f"{role.title()} holdings have avg stress correlation {ref:.2f}. "
            f"Some shared drivers, but meaningful diversification exists."
        )
    elif ref < 0.7:
        assessment_str = "concentrated"
        detail = (
            f"{role.title()} holdings have avg stress correlation {ref:.2f}. "
            f"Moderate concentration — they tend to move together in stress."
        )
    else:
        assessment_str = "false diversification"
        detail = (
            f"WARNING: {role.title()} holdings have avg stress correlation {ref:.2f}. "
            f"Despite multiple positions, these are effectively the same bet. "
            f"Diversification is illusory."
        )

    rd = RoleDiversification(
        role=role, member_count=len(tickers),
        avg_intra_corr_60d=avg_60, avg_intra_corr_stress=avg_stress,
        highest_pair=highest_pair, highest_corr=highest_corr,
        assessment=assessment_str, detail=detail,
    )
    report.role_diversifications.append(rd)
    if attr_name:
        setattr(report, attr_name, rd)


def _validate_groups(report: CorrelationReport, classifications: dict) -> None:
    """Validate stress_correlation_group tags (supporting detail)."""
    groups: dict[str, list[str]] = {}
    for ticker, cls in classifications.items():
        grp = cls.get("group")
        if grp:
            groups.setdefault(grp, []).append(ticker)

    for grp_name, grp_tickers in sorted(groups.items()):
        if len(grp_tickers) < 2:
            report.group_validations.append(GroupValidation(
                group_name=grp_name, tickers=grp_tickers,
                avg_intra_corr_stress=None, min_intra_corr=None,
                weakest_pair=f"N/A (single member: {grp_tickers[0]})",
                valid=True, detail="Single member — no intra-group correlation.",
            ))
            continue

        intra = [p for p in report.pair_results if p.same_group and p.group_a == grp_name]
        stress_corrs = [p.corr_stress for p in intra if p.corr_stress is not None]
        avg_stress = sum(stress_corrs) / len(stress_corrs) if stress_corrs else None

        all_ref = [(p, p.corr_stress if p.corr_stress is not None else p.corr_60d)
                    for p in intra]
        all_ref = [(p, c) for p, c in all_ref if c is not None]

        if all_ref:
            wp, mc = min(all_ref, key=lambda x: x[1])
            weakest = f"{wp.ticker_a}–{wp.ticker_b} ({mc:.2f})"
            min_corr = mc
        else:
            weakest, min_corr = "N/A", None

        valid = min_corr is None or min_corr >= 0.5

        report.group_validations.append(GroupValidation(
            group_name=grp_name, tickers=grp_tickers,
            avg_intra_corr_stress=avg_stress,
            min_intra_corr=min_corr,
            weakest_pair=weakest,
            valid=valid,
            detail=(
                f"Avg stress corr: {avg_stress:.2f}" if avg_stress is not None
                else "Insufficient stress data"
            ),
        ))
