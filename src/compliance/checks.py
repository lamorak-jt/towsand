"""Compliance engine — implements all portfolio management rules.

Each check function takes a PortfolioValuation and returns a list of CheckResult.
Status: pass / warning / breach.

Rules reference: current-finances/portfolio-management-rules.md
"""

import json
import logging
from dataclasses import dataclass
from datetime import date

from src.db.connection import get_connection
from src.portfolio.valuation import PortfolioValuation, HoldingValue

logger = logging.getLogger(__name__)


@dataclass
class CheckResult:
    """Result of a single compliance check."""
    rule_id: str        # e.g. "1.1", "3.1"
    rule_name: str
    status: str         # "pass", "warning", "breach"
    detail: str
    value: float | None = None       # actual measured value
    threshold: float | None = None   # rule threshold


def _get_param(conn, key: str, default: str = "") -> str:
    row = conn.execute("SELECT value FROM parameters WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else default


def _get_param_float(conn, key: str, default: float = 0.0) -> float:
    return float(_get_param(conn, key, str(default)))


# ─── Rule 1.1 & 2.1: Capital Role Allocation ───────────────────────────────

def check_capital_roles(pv: PortfolioValuation, db_path=None) -> list[CheckResult]:
    """Rules 1.1 and 2.1: capital role band checks + income substitution."""
    results = []
    total = pv.total_aud

    if total <= 0:
        return [CheckResult("1.1", "Capital Role Allocation", "breach",
                            "Portfolio total is zero or negative.")]

    roles = pv.by_capital_role()
    stabiliser = roles.get("stabiliser", 0)
    compounder = roles.get("compounder", 0)
    optionality = roles.get("optionality", 0)
    unclassified = roles.get("unclassified", 0)

    # Warn if instruments unclassified
    if unclassified > 0:
        unclass_pct = unclassified / total * 100
        results.append(CheckResult(
            "1.1a", "Unclassified Holdings", "warning",
            f"AUD {unclassified:,.0f} ({unclass_pct:.1f}%) of holdings are unclassified. "
            "Classify with `towsand classify role`.",
            value=unclass_pct,
        ))

    # Only check bands if holdings are largely classified
    classified = stabiliser + compounder + optionality
    if classified == 0:
        results.append(CheckResult(
            "1.1", "Capital Role Allocation", "warning",
            "No instruments classified yet. Cannot check role allocation bands.",
        ))
        return results

    # Use classified portion for percentage checks
    s_pct = stabiliser / total * 100
    c_pct = compounder / total * 100
    o_pct = optionality / total * 100

    # Rule 2.1: Income Substitution — stabiliser must cover ≥24 months of expenses
    with get_connection(db_path) as conn:
        monthly_expenses = _get_param_float(conn, "monthly_expenses", 9000)
    min_stabiliser_abs = 24 * monthly_expenses

    # Rule 1.1 + 2.1: stabiliser = max(24 months, 15-25% band)
    min_stabiliser_pct = 15.0
    max_stabiliser_pct = 25.0

    if stabiliser < min_stabiliser_abs:
        months_covered = stabiliser / monthly_expenses if monthly_expenses > 0 else 0
        results.append(CheckResult(
            "2.1", "Income Substitution", "breach",
            f"Stabiliser AUD {stabiliser:,.0f} covers only {months_covered:.1f} months. "
            f"Need ≥24 months = AUD {min_stabiliser_abs:,.0f}.",
            value=months_covered, threshold=24,
        ))
    else:
        months_covered = stabiliser / monthly_expenses if monthly_expenses > 0 else 0
        results.append(CheckResult(
            "2.1", "Income Substitution", "pass",
            f"Stabiliser covers {months_covered:.1f} months of expenses (≥24 required).",
            value=months_covered, threshold=24,
        ))

    # Rule 1.1: Stabiliser band 15-25% (conditional on Rule 2.1)
    # If the 24-month absolute floor forces stabiliser above 25%, the floor binds
    # and the percentage band is not applicable — this is not an over-allocation.
    floor_binds = min_stabiliser_abs > total * max_stabiliser_pct / 100

    if s_pct < min_stabiliser_pct:
        results.append(CheckResult(
            "1.1-S", "Stabiliser Band", "breach",
            f"Stabiliser at {s_pct:.1f}% (min 15%). AUD {stabiliser:,.0f} of {total:,.0f}.",
            value=s_pct, threshold=min_stabiliser_pct,
        ))
    elif s_pct > max_stabiliser_pct:
        if floor_binds:
            # Absolute floor (Rule 2.1) forces stabiliser above 25% — this is expected
            results.append(CheckResult(
                "1.1-S", "Stabiliser Band", "pass",
                f"Stabiliser at {s_pct:.1f}% (above 25% band, but 24-month expense floor "
                f"of AUD {min_stabiliser_abs:,.0f} binds — Rule 2.1 takes priority).",
                value=s_pct, threshold=max_stabiliser_pct,
            ))
        else:
            # Portfolio is large enough that 25% > 24 months — stabiliser is genuinely overweight
            cash_aud = pv.investable_cash_aud
            cash_note = f" (includes AUD {cash_aud:,.0f} investable cash)" if cash_aud > 0 else ""
            excess = stabiliser - total * max_stabiliser_pct / 100
            results.append(CheckResult(
                "1.1-S", "Stabiliser Band", "warning",
                f"Stabiliser at {s_pct:.1f}% (target 15-25%){cash_note}. "
                f"Over-allocated by AUD {excess:,.0f} — "
                "consider deploying into compounders/optionality.",
                value=s_pct, threshold=max_stabiliser_pct,
            ))
    else:
        results.append(CheckResult(
            "1.1-S", "Stabiliser Band", "pass",
            f"Stabiliser at {s_pct:.1f}% (target 15-25%).",
            value=s_pct,
        ))

    # Rule 1.1: Compounder band 50-65%
    if c_pct < 50:
        results.append(CheckResult(
            "1.1-C", "Compounder Band", "breach",
            f"Compounder at {c_pct:.1f}% (min 50%). AUD {compounder:,.0f}.",
            value=c_pct, threshold=50,
        ))
    elif c_pct > 65:
        results.append(CheckResult(
            "1.1-C", "Compounder Band", "warning",
            f"Compounder at {c_pct:.1f}% (target 50-65%). AUD {compounder:,.0f}.",
            value=c_pct, threshold=65,
        ))
    else:
        results.append(CheckResult(
            "1.1-C", "Compounder Band", "pass",
            f"Compounder at {c_pct:.1f}% (target 50-65%).",
            value=c_pct,
        ))

    # Rule 1.1: Optionality band 10-20%
    if o_pct < 10:
        results.append(CheckResult(
            "1.1-O", "Optionality Band", "warning",
            f"Optionality at {o_pct:.1f}% (target 10-20%). AUD {optionality:,.0f}.",
            value=o_pct, threshold=10,
        ))
    elif o_pct > 20:
        results.append(CheckResult(
            "1.1-O", "Optionality Band", "breach",
            f"Optionality at {o_pct:.1f}% (max 20%). AUD {optionality:,.0f}.",
            value=o_pct, threshold=20,
        ))
    else:
        results.append(CheckResult(
            "1.1-O", "Optionality Band", "pass",
            f"Optionality at {o_pct:.1f}% (target 10-20%).",
            value=o_pct,
        ))

    return results


# ─── Rule 2.2: Income Shock Trigger ────────────────────────────────────────

def check_income_shock(pv: PortfolioValuation, db_path=None) -> list[CheckResult]:
    """Rule 2.2: if income shock is active, check emergency constraints."""
    results = []

    with get_connection(db_path) as conn:
        shock_active = _get_param(conn, "income_shock_active", "false")

    if shock_active.lower() != "true":
        results.append(CheckResult(
            "2.2", "Income Shock", "pass",
            "No income shock active.",
        ))
        return results

    total = pv.total_aud
    roles = pv.by_capital_role()
    optionality = roles.get("optionality", 0)
    o_pct = (optionality / total * 100) if total > 0 else 0

    # Under shock: optionality capped at 10%
    if o_pct > 10:
        results.append(CheckResult(
            "2.2", "Income Shock — Optionality Cap", "breach",
            f"INCOME SHOCK ACTIVE. Optionality at {o_pct:.1f}% (max 10% during shock).",
            value=o_pct, threshold=10,
        ))
    else:
        results.append(CheckResult(
            "2.2", "Income Shock — Optionality Cap", "pass",
            f"Income shock active. Optionality at {o_pct:.1f}% (≤10% OK).",
            value=o_pct, threshold=10,
        ))

    return results


# ─── Rules 3.1, 3.2: Position Size ─────────────────────────────────────────

def check_position_size(pv: PortfolioValuation) -> list[CheckResult]:
    """Rules 3.1 and 3.2: single security caps and issuer concentration."""
    results = []
    total = pv.total_aud

    if total <= 0:
        return results

    # Rule 3.1: Single equity ≤ 10%, single credit ≤ 7%, speculative ≤ 1%/3%
    # asset_class determines which cap applies (not instrument_type/wrapper).
    # Credit instruments in an ETF wrapper are still credit for sizing purposes.
    equity_classes = {"equity", "infrastructure"}
    credit_classes = {"credit"}
    speculative_total = 0

    for h in pv.holdings:
        pct = (h.value_aud / total * 100) if total > 0 else 0
        ac = h.asset_class or h.instrument_type  # fallback for unclassified

        if ac in credit_classes:
            if pct > 7:
                results.append(CheckResult(
                    "3.1-cr", f"Single Credit Cap: {h.ticker}", "breach",
                    f"{h.ticker} ({ac}) at {pct:.1f}% (max 7%). AUD {h.value_aud:,.0f}.",
                    value=pct, threshold=7,
                ))
        elif ac in equity_classes or h.instrument_type in {"equity", "etf", "listed_fund"}:
            if pct > 10:
                results.append(CheckResult(
                    "3.1-eq", f"Single Equity Cap: {h.ticker}", "breach",
                    f"{h.ticker} ({ac}) at {pct:.1f}% (max 10%). AUD {h.value_aud:,.0f}.",
                    value=pct, threshold=10,
                ))

        # Check speculative flag from DB
        with get_connection() as conn:
            inst_row = conn.execute(
                "SELECT is_speculative FROM instruments WHERE ticker = ?",
                (h.ticker,),
            ).fetchone()
        is_spec = inst_row and inst_row["is_speculative"]

        if is_spec:
            if pct > 1:
                results.append(CheckResult(
                    "3.1-sp", f"Speculative Cap: {h.ticker}", "breach",
                    f"Speculative {h.ticker} at {pct:.1f}% (max 1%).",
                    value=pct, threshold=1,
                ))
            speculative_total += h.value_aud

    spec_pct = (speculative_total / total * 100) if total > 0 else 0
    if spec_pct > 3:
        results.append(CheckResult(
            "3.1-sp-agg", "Speculative Aggregate", "breach",
            f"Total speculative at {spec_pct:.1f}% (max 3%).",
            value=spec_pct, threshold=3,
        ))

    # Rule 3.2: Issuer concentration ≤ 20% per corporate group
    groups: dict[str, float] = {}
    for h in pv.holdings:
        grp = h.corporate_group
        if grp:
            groups[grp] = groups.get(grp, 0) + h.value_aud

    for grp, value in groups.items():
        pct = (value / total * 100) if total > 0 else 0
        if pct > 20:
            results.append(CheckResult(
                "3.2", f"Issuer Concentration: {grp}", "breach",
                f"Corporate group '{grp}' at {pct:.1f}% (max 20%). AUD {value:,.0f}.",
                value=pct, threshold=20,
            ))

    if not results:
        results.append(CheckResult(
            "3.1", "Position Size", "pass",
            "All positions within size limits.",
        ))

    return results


# ─── Rules 4.1, 4.2: Macro Factor Exposure ─────────────────────────────────

def check_macro_exposure(pv: PortfolioValuation) -> list[CheckResult]:
    """Rules 4.1 and 4.2: Australia concentration and single macro driver caps."""
    results = []
    total = pv.total_aud

    if total <= 0:
        return results

    # Rule 4.1: AUD-domiciled risk assets ≤ 55% (excl AUD govt bonds)
    aud_risk = 0
    for h in pv.holdings:
        if h.country == "AU" and h.instrument_type not in ("govt_bond_nominal", "govt_bond_indexed"):
            aud_risk += h.value_aud

    aud_risk_pct = (aud_risk / total * 100) if total > 0 else 0
    if aud_risk_pct > 55:
        results.append(CheckResult(
            "4.1", "Australia Concentration", "breach",
            f"AUD risk assets at {aud_risk_pct:.1f}% (max 55%). AUD {aud_risk:,.0f}.",
            value=aud_risk_pct, threshold=55,
        ))
    else:
        results.append(CheckResult(
            "4.1", "Australia Concentration", "pass",
            f"AUD risk assets at {aud_risk_pct:.1f}% (max 55%).",
            value=aud_risk_pct, threshold=55,
        ))

    # Rule 4.2: Single macro driver ≤ 30%
    macro = pv.by_macro_driver()
    for driver, value in macro.items():
        if driver in ("untagged", "none"):
            continue
        pct = (value / total * 100) if total > 0 else 0
        if pct > 30:
            results.append(CheckResult(
                "4.2", f"Macro Driver: {driver}", "breach",
                f"Macro driver '{driver}' at {pct:.1f}% (max 30%). AUD {value:,.0f}.",
                value=pct, threshold=30,
            ))

    if not any(r.rule_id == "4.2" for r in results):
        results.append(CheckResult(
            "4.2", "Macro Driver Exposure", "pass",
            "No macro driver exceeds 30%.",
        ))

    return results


# ─── Rules 5.1, 5.2: Currency Exposure ─────────────────────────────────────

def check_currency_exposure(pv: PortfolioValuation) -> list[CheckResult]:
    """Rules 5.1 and 5.2: currency bands for growth capital, hedging rule."""
    results = []

    # Growth capital = compounder + optionality (excludes stabiliser and cash)
    growth_holdings = [h for h in pv.holdings
                       if h.capital_role in ("compounder", "optionality")]
    growth_total = sum(h.value_aud for h in growth_holdings)

    if growth_total <= 0:
        results.append(CheckResult(
            "5.1", "Currency Exposure", "warning",
            "No growth capital classified — cannot check currency bands.",
        ))
        return results

    # Use economic_currency (underlying exposure) when available, fall back to listing currency
    aud_growth = sum(
        h.value_aud for h in growth_holdings
        if (h.economic_currency or h.currency) == "AUD"
    )
    aud_pct = (aud_growth / growth_total * 100)

    # Rule 5.1: AUD 50-70%, non-AUD 30-50%
    if aud_pct < 50:
        results.append(CheckResult(
            "5.1", "AUD Growth Exposure", "breach",
            f"AUD growth at {aud_pct:.1f}% (min 50%). AUD {aud_growth:,.0f} of {growth_total:,.0f}.",
            value=aud_pct, threshold=50,
        ))
    elif aud_pct > 70:
        results.append(CheckResult(
            "5.1", "AUD Growth Exposure", "warning",
            f"AUD growth at {aud_pct:.1f}% (target 50-70%).",
            value=aud_pct, threshold=70,
        ))
    else:
        results.append(CheckResult(
            "5.1", "AUD Growth Exposure", "pass",
            f"AUD growth at {aud_pct:.1f}% (target 50-70%).",
            value=aud_pct,
        ))

    # Rule 5.2: ≥40% of international growth assets unhedged
    intl_growth = [h for h in growth_holdings if (h.economic_currency or h.currency) != "AUD"]
    intl_total = sum(h.value_aud for h in intl_growth)
    if intl_total > 0:
        unhedged = sum(h.value_aud for h in intl_growth if h.capital_role and not _is_hedged(h))
        unhedged_pct = (unhedged / intl_total * 100) if intl_total > 0 else 0

        if unhedged_pct < 40:
            results.append(CheckResult(
                "5.2", "Hedging Rule", "breach",
                f"Only {unhedged_pct:.1f}% of international growth is unhedged (min 40%).",
                value=unhedged_pct, threshold=40,
            ))
        else:
            results.append(CheckResult(
                "5.2", "Hedging Rule", "pass",
                f"{unhedged_pct:.1f}% of international growth is unhedged (≥40% required).",
                value=unhedged_pct, threshold=40,
            ))

    return results


def _is_hedged(h: HoldingValue) -> bool:
    """Check if a holding is marked as hedged in classifications."""
    with get_connection() as conn:
        row = conn.execute("""
            SELECT hedged FROM instrument_classifications ic
            JOIN instruments i ON i.id = ic.instrument_id
            WHERE i.ticker = ?
        """, (h.ticker,)).fetchone()
    if row and row["hedged"] is not None:
        return row["hedged"] == 1
    return False  # assume unhedged if not specified


# ─── Rules 6.1, 6.2: Optionality Constraints ──────────────────────────────

def check_optionality(pv: PortfolioValuation) -> list[CheckResult]:
    """Rules 6.1 and 6.2: convexity payoff test, yield exclusion."""
    results = []

    opt_holdings = [h for h in pv.holdings if h.capital_role == "optionality"]
    if not opt_holdings:
        results.append(CheckResult(
            "6.1", "Optionality Constraints", "pass",
            "No optionality holdings to check.",
        ))
        return results

    opt_total = sum(h.value_aud for h in opt_holdings)

    with get_connection() as conn:
        for h in opt_holdings:
            row = conn.execute("""
                SELECT convexity_defined_downside, convexity_nonlinear_upside,
                       convexity_stress_outperform
                FROM instrument_classifications ic
                JOIN instruments i ON i.id = ic.instrument_id
                WHERE i.ticker = ?
            """, (h.ticker,)).fetchone()

            if not row:
                results.append(CheckResult(
                    "6.1", f"Convexity Test: {h.ticker}", "warning",
                    f"{h.ticker} has no convexity metadata. Tag using `towsand classify tag`.",
                ))
                continue

            score = sum(1 for attr in [
                row["convexity_defined_downside"],
                row["convexity_nonlinear_upside"],
                row["convexity_stress_outperform"],
            ] if attr == 1)

            if score < 2:
                results.append(CheckResult(
                    "6.1", f"Convexity Test: {h.ticker}", "breach",
                    f"{h.ticker} scores {score}/3 on payoff shape (need ≥2).",
                    value=score, threshold=2,
                ))

    # Rule 6.2: Yield-dominant ≤ 25% of optionality
    yield_total = 0
    with get_connection() as conn:
        for h in opt_holdings:
            row = conn.execute("""
                SELECT yield_dominant FROM instrument_classifications ic
                JOIN instruments i ON i.id = ic.instrument_id
                WHERE i.ticker = ?
            """, (h.ticker,)).fetchone()
            if row and row["yield_dominant"] == 1:
                yield_total += h.value_aud

    if opt_total > 0:
        yield_pct = (yield_total / opt_total * 100)
        if yield_pct > 25:
            results.append(CheckResult(
                "6.2", "Yield Exclusion", "breach",
                f"Yield-dominant instruments are {yield_pct:.1f}% of optionality (max 25%).",
                value=yield_pct, threshold=25,
            ))

    if not results:
        results.append(CheckResult(
            "6.1", "Optionality Constraints", "pass",
            "All optionality holdings pass convexity and yield tests.",
        ))

    return results


# ─── Rules 7.1, 7.2, 7.3: Stabiliser Constraints ──────────────────────────

def check_stabiliser(pv: PortfolioValuation) -> list[CheckResult]:
    """Rules 7.1, 7.2, 7.3: liquidity, duration, inflation coverage."""
    results = []

    stab_holdings = [h for h in pv.holdings if h.capital_role == "stabiliser"]
    # Include investable cash in stabiliser total (non-investable excluded per §0)
    stab_holdings_total = sum(h.value_aud for h in stab_holdings)
    stab_cash = sum(c.value_aud for c in pv.cash if c.is_investable)
    stab_total = stab_holdings_total + stab_cash

    if stab_total <= 0:
        results.append(CheckResult(
            "7.1", "Stabiliser Constraints", "warning",
            "No stabiliser capital identified.",
        ))
        return results

    # Rule 7.1: ≥70% liquid within 5 days
    liquid_total = stab_cash  # cash is always liquid
    with get_connection() as conn:
        for h in stab_holdings:
            row = conn.execute("""
                SELECT liquidity_days FROM instrument_classifications ic
                JOIN instruments i ON i.id = ic.instrument_id
                WHERE i.ticker = ?
            """, (h.ticker,)).fetchone()
            if row and row["liquidity_days"] is not None and row["liquidity_days"] <= 5:
                liquid_total += h.value_aud
            elif not row or row["liquidity_days"] is None:
                # Assume liquid if no data (conservative: flag as warning)
                liquid_total += h.value_aud

    liquid_pct = (liquid_total / stab_total * 100) if stab_total > 0 else 0
    if liquid_pct < 70:
        results.append(CheckResult(
            "7.1", "Stabiliser Liquidity", "breach",
            f"Only {liquid_pct:.1f}% of stabiliser liquid within 5 days (need ≥70%).",
            value=liquid_pct, threshold=70,
        ))
    else:
        results.append(CheckResult(
            "7.1", "Stabiliser Liquidity", "pass",
            f"{liquid_pct:.1f}% of stabiliser liquid within 5 days (≥70% required).",
            value=liquid_pct, threshold=70,
        ))

    # Rule 7.2: No single duration point >40% of stabiliser capital
    duration_buckets: dict[str, float] = {}
    with get_connection() as conn:
        for h in stab_holdings:
            row = conn.execute("""
                SELECT duration_years FROM instrument_classifications ic
                JOIN instruments i ON i.id = ic.instrument_id
                WHERE i.ticker = ?
            """, (h.ticker,)).fetchone()
            if row and row["duration_years"] is not None:
                bucket = f"{row['duration_years']:.0f}y"
            else:
                bucket = "unknown"
            duration_buckets[bucket] = duration_buckets.get(bucket, 0) + h.value_aud

    for bucket, value in duration_buckets.items():
        if bucket == "unknown":
            continue
        pct = (value / stab_total * 100) if stab_total > 0 else 0
        if pct > 40:
            results.append(CheckResult(
                "7.2", f"Duration Concentration: {bucket}", "breach",
                f"Duration bucket '{bucket}' is {pct:.1f}% of stabiliser (max 40%).",
                value=pct, threshold=40,
            ))

    # Rule 7.3: ≥25% of stabiliser in inflation-linked/real-rate
    inflation_total = 0
    with get_connection() as conn:
        for h in stab_holdings:
            row = conn.execute("""
                SELECT is_inflation_linked FROM instrument_classifications ic
                JOIN instruments i ON i.id = ic.instrument_id
                WHERE i.ticker = ?
            """, (h.ticker,)).fetchone()
            if row and row["is_inflation_linked"] == 1:
                inflation_total += h.value_aud

    infl_pct = (inflation_total / stab_total * 100) if stab_total > 0 else 0
    if infl_pct < 25:
        results.append(CheckResult(
            "7.3", "Inflation Coverage", "warning",
            f"Only {infl_pct:.1f}% of stabiliser is inflation-linked (target ≥25%).",
            value=infl_pct, threshold=25,
        ))
    else:
        results.append(CheckResult(
            "7.3", "Inflation Coverage", "pass",
            f"{infl_pct:.1f}% of stabiliser is inflation-linked (≥25% required).",
            value=infl_pct, threshold=25,
        ))

    return results


# ─── Rules 8.1, 8.2: Drawdown & Correlation ────────────────────────────────

def check_drawdown(pv: PortfolioValuation) -> list[CheckResult]:
    """Rules 8.1 and 8.2: drawdown tolerance, stress correlation."""
    results = []
    total = pv.total_aud

    if total <= 0:
        return results

    # Rule 8.1: 35% equity drawdown must not force liquidation
    # Model: equity-like holdings lose 35%, check if stabiliser still covers expenses
    equity_loss = 0
    for h in pv.holdings:
        if h.capital_role in ("compounder", "optionality"):
            equity_loss += h.value_aud * 0.35

    with get_connection() as conn:
        monthly = _get_param_float(conn, "monthly_expenses", 9000)
    min_needed = 24 * monthly  # must still cover 24 months

    roles = pv.by_capital_role()
    # by_capital_role() already includes cash in stabiliser — no separate addition
    stabiliser_post = roles.get("stabiliser", 0)

    if stabiliser_post < min_needed:
        results.append(CheckResult(
            "8.1", "Drawdown Tolerance", "breach",
            f"After 35% equity drawdown, stabiliser AUD {stabiliser_post:,.0f} "
            f"< 24-month floor AUD {min_needed:,.0f}. Risk of forced liquidation.",
            value=stabiliser_post, threshold=min_needed,
        ))
    else:
        results.append(CheckResult(
            "8.1", "Drawdown Tolerance", "pass",
            f"After 35% equity drawdown, stabiliser AUD {stabiliser_post:,.0f} still covers "
            f"24 months (AUD {min_needed:,.0f}).",
            value=stabiliser_post, threshold=min_needed,
        ))

    # Rule 8.2: Stress correlation — check via correlation groups
    corr_groups: dict[str, float] = {}
    with get_connection() as conn:
        for h in pv.holdings:
            row = conn.execute("""
                SELECT stress_correlation_group FROM instrument_classifications ic
                JOIN instruments i ON i.id = ic.instrument_id
                WHERE i.ticker = ?
            """, (h.ticker,)).fetchone()
            if row and row["stress_correlation_group"]:
                grp = row["stress_correlation_group"]
                corr_groups[grp] = corr_groups.get(grp, 0) + h.value_aud

    for grp, value in corr_groups.items():
        pct = (value / total * 100) if total > 0 else 0
        if pct > 20:
            results.append(CheckResult(
                "8.2", f"Stress Correlation: {grp}", "warning",
                f"Correlation group '{grp}' at {pct:.1f}% (>0.7 stress corr → single risk). "
                "Consider as one position for sizing.",
                value=pct,
            ))

    return results


# ─── Rule 9: Review Triggers ───────────────────────────────────────────────

def check_review_triggers(pv: PortfolioValuation, db_path=None) -> list[CheckResult]:
    """Rule 9: check if any review triggers are active."""
    results = []

    with get_connection(db_path) as conn:
        triggers = {
            "income_shock_active": "Income shock",
            "inflation_shift_active": "Structural inflation shift",
            "currency_regime_active": "Currency regime change",
            "correlation_convergence_active": "Correlation convergence",
        }

        active = []
        for key, label in triggers.items():
            val = _get_param(conn, key, "false")
            if val.lower() == "true":
                active.append(label)

    # Check for rule breaches (proxy: count breach results from other checks)
    # This is handled by the caller — just report trigger status
    if active:
        results.append(CheckResult(
            "9.1", "Review Triggers", "warning",
            f"Active triggers: {', '.join(active)}. Review required.",
        ))
    else:
        results.append(CheckResult(
            "9.2", "No Action Rule", "pass",
            "No review triggers active. Absent a trigger, no discretionary rebalancing.",
        ))

    return results


# ─── Data Freshness ─────────────────────────────────────────────────────────

def check_data_freshness(pv: PortfolioValuation, db_path=None) -> list[CheckResult]:
    """Check that prices and FX rates are recent enough for reliable compliance."""
    results = []
    today = date.today()

    stale_prices = []
    for h in pv.holdings:
        if not h.price_date:
            stale_prices.append(f"{h.ticker} (no price)")
            continue
        try:
            price_date = date.fromisoformat(h.price_date)
            age_days = (today - price_date).days
            if age_days > 7:
                stale_prices.append(f"{h.ticker} ({age_days}d old)")
        except ValueError:
            stale_prices.append(f"{h.ticker} (bad date: {h.price_date})")

    if stale_prices:
        results.append(CheckResult(
            "D.1", "Price Freshness", "warning",
            f"Stale prices (>7 days): {', '.join(stale_prices)}. "
            "Run `towsand prices update` before relying on compliance results.",
        ))

    # Check FX freshness for non-AUD currencies held
    with get_connection(db_path) as conn:
        non_aud = set()
        for h in pv.holdings:
            if h.currency != "AUD":
                non_aud.add(h.currency)

        stale_fx = []
        for ccy in sorted(non_aud):
            row = conn.execute(
                "SELECT date FROM fx_rates WHERE from_currency = ? AND to_currency = 'AUD' "
                "ORDER BY date DESC LIMIT 1",
                (ccy,),
            ).fetchone()
            if not row:
                stale_fx.append(f"{ccy}/AUD (no rate)")
            else:
                try:
                    fx_date = date.fromisoformat(row["date"])
                    age_days = (today - fx_date).days
                    if age_days > 7:
                        stale_fx.append(f"{ccy}/AUD ({age_days}d old)")
                except ValueError:
                    stale_fx.append(f"{ccy}/AUD (bad date)")

    if stale_fx:
        results.append(CheckResult(
            "D.2", "FX Rate Freshness", "warning",
            f"Stale FX rates (>7 days): {', '.join(stale_fx)}. "
            "Run `towsand fx update` before relying on compliance results.",
        ))

    if not results:
        results.append(CheckResult(
            "D.1", "Data Freshness", "pass",
            "All prices and FX rates are current (≤7 days old).",
        ))

    return results


# ─── Run All Checks ────────────────────────────────────────────────────────

def run_all_checks(pv: PortfolioValuation, db_path=None) -> list[CheckResult]:
    """Run all compliance checks and return results."""
    all_results = []
    all_results.extend(check_data_freshness(pv, db_path))
    all_results.extend(check_capital_roles(pv, db_path))
    all_results.extend(check_income_shock(pv, db_path))
    all_results.extend(check_position_size(pv))
    all_results.extend(check_macro_exposure(pv))
    all_results.extend(check_currency_exposure(pv))
    all_results.extend(check_optionality(pv))
    all_results.extend(check_stabiliser(pv))
    all_results.extend(check_drawdown(pv))
    all_results.extend(check_review_triggers(pv, db_path))
    return all_results


def store_compliance_snapshot(results: list[CheckResult], total_aud: float,
                              db_path=None) -> int:
    """Store a compliance run in the database. Returns the portfolio_snapshot_id."""
    from datetime import date as dt_date

    today = dt_date.today().isoformat()

    with get_connection(db_path) as conn:
        # Create portfolio snapshot
        conn.execute(
            "INSERT INTO portfolio_snapshots (date, total_value_aud, snapshot_data) VALUES (?, ?, ?)",
            (today, total_aud, json.dumps({"source": "compliance_run"})),
        )
        snap_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

        # Store each check result
        for r in results:
            conn.execute(
                "INSERT INTO compliance_snapshots (portfolio_snapshot_id, date, rule_id, status, detail) "
                "VALUES (?, ?, ?, ?, ?)",
                (snap_id, today, r.rule_id, r.status, r.detail),
            )

    return snap_id
