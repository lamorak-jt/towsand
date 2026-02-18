"""Sensitivity analysis — objective-level fragility.

Instead of asking "how close is each rule to breaching?", this asks:

1. How far from INCOME BRIDGE FAILURE? What equity decline wipes out
   the 24-month expense floor?
2. How far from FORCED LIQUIDATION? What move forces selling compounders
   to meet near-term needs?
3. How much COMPOUNDING CAPITAL IS AT RISK per 10% equity decline?
4. What market move WEAKENS AUD LIABILITY MATCHING (currency exposure)?

Rule-level constraint buffers are reported as supporting detail.

Strategy reference: current-finances/strategy-assumptions.md
"""

import logging
import math
from dataclasses import dataclass, field

from src.db.connection import get_connection
from src.portfolio.valuation import PortfolioValuation

logger = logging.getLogger(__name__)

REAL_RETURN_PA = 0.065


@dataclass
class ObjectiveSensitivity:
    """Sensitivity of a single strategic objective to market moves."""
    objective: str           # which objective this tests
    headline: str            # one-sentence finding
    current_state: str       # where we are now
    trigger_move: str        # what market move causes failure
    consequence: str         # what happens if it triggers
    severity: str            # "safe", "watch", "fragile", "critical"


@dataclass
class RuleBuffer:
    """Supporting detail: a single rule's distance from breach."""
    rule_id: str
    description: str
    current_value: float
    limit: float
    buffer_pct: float
    breach_move: str


@dataclass
class SensitivityReport:
    """Full sensitivity report — objectives first, rules second."""
    objectives: list[ObjectiveSensitivity] = field(default_factory=list)
    rule_buffers: list[RuleBuffer] = field(default_factory=list)


def analyse_sensitivity(pv: PortfolioValuation, db_path=None) -> SensitivityReport:
    """Analyse portfolio fragility against strategy objectives."""
    report = SensitivityReport()
    total = pv.total_aud
    if total <= 0:
        return report

    with get_connection(db_path) as conn:
        monthly = float(conn.execute(
            "SELECT value FROM parameters WHERE key = 'monthly_expenses'"
        ).fetchone()["value"] or "9000")

    roles = pv.by_capital_role()
    stabiliser = roles.get("stabiliser", 0)
    compounder = roles.get("compounder", 0)
    optionality = roles.get("optionality", 0)

    _assess_income_bridge(report, pv, stabiliser, compounder, optionality, monthly)
    _assess_forced_liquidation(report, pv, stabiliser, compounder, optionality, monthly)
    _assess_compounding_damage(report, pv, compounder, total)
    _assess_currency_liability(report, pv)
    _assess_optionality_weight(report, pv, optionality, total)
    _collect_rule_buffers(report, pv, total, db_path)

    return report


def _assess_income_bridge(
    report: SensitivityReport, pv: PortfolioValuation,
    stabiliser: float, compounder: float, optionality: float, monthly: float,
) -> None:
    """How far from income bridge failure?"""
    months_covered = stabiliser / monthly if monthly > 0 else 0
    excess_months = months_covered - 24

    # Stabiliser doesn't move much in equity stress (it's bonds + cash).
    # But stabiliser *instruments* can lose value (e.g., bond price decline in rate shock).
    # Compute: what % decline in stabiliser assets breaks the 24-month floor?
    stab_holdings = sum(h.value_aud for h in pv.holdings if h.capital_role == "stabiliser")
    min_stab = 24 * monthly

    if stabiliser <= 0:
        severity = "critical"
        headline = "No stabiliser capital identified — income bridge undefined."
        trigger = "N/A"
        consequence = "Cannot fund living expenses from portfolio."
    elif stabiliser < min_stab:
        severity = "critical"
        headline = (
            f"Income bridge ALREADY BROKEN — covers {months_covered:.0f} months, "
            f"need 24."
        )
        trigger = "Already failed."
        consequence = "Must fund gap from employment income or sell growth assets."
    elif stab_holdings > 0:
        excess_aud = stabiliser - min_stab
        stab_cash = stabiliser - stab_holdings
        # Cash doesn't decline in market stress, so only holdings can lose value.
        # If cash alone covers the floor, a 100% wipeout of holdings won't break it.
        floor_unbreakable = stab_cash >= min_stab
        max_decline_pct = min((excess_aud / stab_holdings) * 100, 100.0) if stab_holdings > 0 else 100.0

        if floor_unbreakable:
            severity = "safe"
            headline = (
                f"Income bridge covers {months_covered:.0f} months "
                f"({excess_months:.0f} months excess). Cash alone "
                f"(AUD {stab_cash:,.0f}) exceeds the 24-month floor — "
                f"market declines in stabiliser holdings cannot break the bridge."
            )
            trigger = (
                f"Stabiliser holdings AUD {stab_holdings:,.0f} could go to zero "
                f"and cash AUD {stab_cash:,.0f} still covers "
                f"{stab_cash / monthly:.0f} months."
            )
        else:
            if max_decline_pct > 50:
                severity = "safe"
            elif max_decline_pct > 20:
                severity = "watch"
            elif max_decline_pct > 10:
                severity = "fragile"
            else:
                severity = "critical"

            headline = (
                f"Income bridge covers {months_covered:.0f} months "
                f"({excess_months:.0f} months excess over 24-month floor)."
            )
            trigger = (
                f"A {max_decline_pct:.0f}% decline in stabiliser holdings "
                f"(AUD {stab_holdings:,.0f}) would break the 24-month floor."
            )

        consequence = (
            f"Below 24 months: must sell compounders to fund living expenses. "
            f"Each month of shortfall = AUD {monthly:,.0f} of compounding capital destroyed."
        )
    else:
        severity = "safe"
        headline = (
            f"Income bridge covers {months_covered:.0f} months. "
            f"Stabiliser is entirely cash — immune to market declines."
        )
        trigger = "Cash-only stabiliser cannot be impaired by market moves."
        consequence = "N/A"

    report.objectives.append(ObjectiveSensitivity(
        objective="Income Bridge",
        headline=headline,
        current_state=f"Stabiliser AUD {stabiliser:,.0f} = {months_covered:.0f} months of expenses",
        trigger_move=trigger,
        consequence=consequence,
        severity=severity,
    ))


def _assess_forced_liquidation(
    report: SensitivityReport, pv: PortfolioValuation,
    stabiliser: float, compounder: float, optionality: float, monthly: float,
) -> None:
    """What equity decline forces selling compounders to meet expenses?"""
    risk_capital = compounder + optionality
    min_stab = 24 * monthly
    stab_excess = stabiliser - min_stab

    if stab_excess < 0:
        severity = "critical"
        headline = "Already below income bridge floor — forced liquidation risk is NOW."
        trigger = "No additional decline needed."
        consequence = (
            f"Shortfall of AUD {abs(stab_excess):,.0f}. "
            f"Must sell growth assets to cover near-term needs."
        )
    elif risk_capital <= 0:
        severity = "safe"
        headline = "No risk capital — nothing to force-sell."
        trigger = "N/A"
        consequence = "N/A"
    else:
        # Stabiliser excess absorbs losses. But in stress, stabiliser instruments
        # can also lose value. Worst case: stabiliser holdings fall AND compounders
        # need selling. The true forced-liquidation threshold is complex, but the
        # key metric is: how large is the stabiliser excess relative to total portfolio?
        excess_pct = stab_excess / pv.total_aud * 100

        if excess_pct > 20:
            severity = "safe"
        elif excess_pct > 10:
            severity = "watch"
        elif excess_pct > 5:
            severity = "fragile"
        else:
            severity = "critical"

        headline = (
            f"Stabiliser excess of AUD {stab_excess:,.0f} "
            f"({excess_pct:.1f}% of portfolio) buffers against forced liquidation."
        )
        trigger = (
            f"Forced liquidation requires stabiliser to fall below AUD {min_stab:,.0f}. "
            f"Current excess: AUD {stab_excess:,.0f}."
        )
        consequence = (
            "If triggered: must sell compounders at distressed prices to fund "
            "living expenses. Permanently impairs long-term wealth."
        )

    report.objectives.append(ObjectiveSensitivity(
        objective="Forced Liquidation",
        headline=headline,
        current_state=(
            f"Stabiliser AUD {stabiliser:,.0f}, floor AUD {min_stab:,.0f}, "
            f"excess AUD {max(stab_excess, 0):,.0f}"
        ),
        trigger_move=trigger,
        consequence=consequence,
        severity=severity,
    ))


def _assess_compounding_damage(
    report: SensitivityReport, pv: PortfolioValuation,
    compounder: float, total: float,
) -> None:
    """How much compounding capital is at risk per 10% equity decline?"""
    if compounder <= 0:
        report.objectives.append(ObjectiveSensitivity(
            objective="Compounding Capital",
            headline="No compounder capital allocated.",
            current_state="AUD 0 in compounders",
            trigger_move="N/A",
            consequence="No long-term compounding is occurring.",
            severity="critical",
        ))
        return

    loss_per_10pct = compounder * 0.10
    recovery_for_10pct = math.log(1 / 0.9) / math.log(1 + REAL_RETURN_PA)
    loss_per_35pct = compounder * 0.35
    recovery_for_35pct = math.log(1 / 0.65) / math.log(1 + REAL_RETURN_PA)

    comp_pct = compounder / total * 100

    if comp_pct < 30:
        severity = "critical"
    elif comp_pct < 50:
        severity = "fragile"
    elif comp_pct <= 65:
        severity = "safe"
    else:
        severity = "watch"

    headline = (
        f"Compounder capital AUD {compounder:,.0f} ({comp_pct:.0f}% of portfolio). "
        f"A 35% drawdown destroys AUD {loss_per_35pct:,.0f} and "
        f"costs {recovery_for_35pct:.1f} years of recovery."
    )
    trigger = (
        f"Per 10% equity decline: AUD {loss_per_10pct:,.0f} lost, "
        f"{recovery_for_10pct:.1f} years to recover at {REAL_RETURN_PA*100:.0f}% real. "
        f"Per 35% decline: AUD {loss_per_35pct:,.0f} lost, "
        f"{recovery_for_35pct:.1f} years to recover."
    )
    consequence = (
        f"Lost compounding is permanent until recovered. "
        f"AUD {loss_per_10pct:,.0f} not compounding for "
        f"{recovery_for_10pct:.1f} years is "
        f"~AUD {loss_per_10pct * recovery_for_10pct * REAL_RETURN_PA:,.0f} "
        f"of foregone real growth."
    )

    report.objectives.append(ObjectiveSensitivity(
        objective="Compounding Capital",
        headline=headline,
        current_state=f"AUD {compounder:,.0f} at {comp_pct:.0f}% of portfolio",
        trigger_move=trigger,
        consequence=consequence,
        severity=severity,
    ))


def _assess_currency_liability(report: SensitivityReport, pv: PortfolioValuation) -> None:
    """What market move weakens AUD liability matching?"""
    growth = [h for h in pv.holdings if h.capital_role in ("compounder", "optionality")]
    growth_total = sum(h.value_aud for h in growth)
    if growth_total <= 0:
        return

    # Use economic_currency (underlying exposure), not listing currency
    aud_growth = sum(h.value_aud for h in growth if (h.economic_currency or h.currency) == "AUD")
    non_aud_growth = growth_total - aud_growth
    aud_pct = aud_growth / growth_total * 100

    if non_aud_growth <= 0 or aud_growth <= 0:
        return

    # What % rally in non-AUD pushes AUD growth below 50%?
    x = aud_growth / non_aud_growth - 1
    x_pct = x * 100

    non_aud_tickers = sorted(
        [h for h in growth if (h.economic_currency or h.currency) != "AUD"],
        key=lambda h: -h.value_aud)
    top = ", ".join(h.ticker for h in non_aud_tickers[:3])

    if aud_pct < 50:
        severity = "critical"
        headline = (
            f"AUD liability matching already under-weight at {aud_pct:.1f}%. "
            f"Living expenses are AUD-denominated but growth capital is tilted offshore."
        )
    elif x_pct < 5:
        severity = "fragile"
        headline = (
            f"AUD growth at {aud_pct:.1f}% — only a {x_pct:.1f}% rally in non-AUD ({top}) "
            f"weakens AUD liability matching below 50%."
        )
    elif x_pct < 15:
        severity = "watch"
        headline = (
            f"AUD growth at {aud_pct:.1f}%. A {x_pct:.1f}% non-AUD outperformance "
            f"would weaken AUD liability matching."
        )
    else:
        severity = "safe"
        headline = f"AUD growth at {aud_pct:.1f}% — comfortable buffer for liability matching."

    report.objectives.append(ObjectiveSensitivity(
        objective="AUD Liability Matching",
        headline=headline,
        current_state=(
            f"AUD growth: AUD {aud_growth:,.0f} ({aud_pct:.1f}%), "
            f"Non-AUD: AUD {non_aud_growth:,.0f} ({100-aud_pct:.1f}%)"
        ),
        trigger_move=(
            f"A {x_pct:.1f}% rally in non-AUD growth assets ({top}) relative to AUD growth "
            f"pushes below 50%."
        ),
        consequence=(
            "Below 50%: living expenses (AUD) are increasingly mismatched with "
            "growth capital (foreign). AUD weakness helps; AUD strength hurts."
        ),
        severity=severity,
    ))


def _assess_optionality_weight(
    report: SensitivityReport, pv: PortfolioValuation,
    optionality: float, total: float,
) -> None:
    """Is optionality capital large enough to matter in a crisis?"""
    opt_pct = optionality / total * 100 if total > 0 else 0

    if opt_pct < 2:
        severity = "critical"
        headline = (
            f"Optionality is {opt_pct:.1f}% of portfolio (AUD {optionality:,.0f}). "
            f"Too small to provide meaningful crisis insurance."
        )
        consequence = (
            "In a crisis, optionality should offset compounder losses. "
            f"At {opt_pct:.1f}%, even a 100% gain adds only AUD {optionality:,.0f} — "
            "negligible against a 35% compounder drawdown."
        )
    elif opt_pct < 10:
        severity = "fragile"
        headline = (
            f"Optionality at {opt_pct:.1f}% — below the 10% target band. "
            f"Crisis insurance is under-funded."
        )
        consequence = (
            f"With AUD {optionality:,.0f}, optionality can partially offset losses "
            f"but cannot meaningfully change portfolio outcomes in severe stress."
        )
    else:
        severity = "safe"
        headline = (
            f"Optionality at {opt_pct:.1f}% (AUD {optionality:,.0f}). "
            f"Sized to provide meaningful crisis insurance."
        )
        consequence = (
            "If optionality instruments perform as designed (convex payoff, "
            "stress outperformance), this allocation can materially offset losses."
        )

    report.objectives.append(ObjectiveSensitivity(
        objective="Optionality as Crisis Insurance",
        headline=headline,
        current_state=f"AUD {optionality:,.0f} = {opt_pct:.1f}% of portfolio",
        trigger_move="Optionality must be sized before the crisis — cannot be added during stress.",
        consequence=consequence,
        severity=severity,
    ))


def _collect_rule_buffers(
    report: SensitivityReport, pv: PortfolioValuation,
    total: float, db_path=None,
) -> None:
    """Collect rule-level constraint buffers as supporting detail."""
    equity_types = {"equity", "etf", "listed_fund"}
    credit_types = {"credit"}

    # Position caps — use asset_class for determining which cap applies
    equity_classes = {"equity", "infrastructure"}
    credit_classes = {"credit"}

    for h in pv.holdings:
        pct = h.value_aud / total * 100
        ac = h.asset_class or h.instrument_type

        if ac in credit_classes:
            cap = 7.0
        elif ac in equity_classes or h.instrument_type in equity_types:
            cap = 10.0
        else:
            continue

        buf = cap - pct
        if buf < 3.0:
            rule_id = "3.1-cr" if ac in credit_classes else "3.1-eq"
            cap_label = "credit" if ac in credit_classes else "equity"

            if buf < 0:
                breach_move = (
                    f"ALREADY IN BREACH: {h.ticker} at {pct:.1f}% "
                    f"(cap {cap:.0f}%), over by {abs(buf):.1f}pp"
                )
            else:
                move = (cap/100 * total - h.value_aud) / (h.value_aud * (1 - cap/100)) * 100 \
                    if h.value_aud > 0 else 0
                breach_move = f"{h.ticker} rallies {move:.0f}% (rest flat)"

            report.rule_buffers.append(RuleBuffer(
                rule_id=rule_id, description=f"{h.ticker} {cap_label} cap",
                current_value=pct, limit=cap, buffer_pct=buf,
                breach_move=breach_move,
            ))

    # Issuer concentration
    groups: dict[str, float] = {}
    for h in pv.holdings:
        if h.corporate_group:
            groups[h.corporate_group] = groups.get(h.corporate_group, 0) + h.value_aud
    for grp, value in groups.items():
        pct = value / total * 100
        buf = 20.0 - pct
        if buf < 5.0:
            report.rule_buffers.append(RuleBuffer(
                rule_id="3.2", description=f"Issuer: {grp}",
                current_value=pct, limit=20.0, buffer_pct=buf,
                breach_move=f"{grp} group assets outperform rest",
            ))

    # Duration concentration
    stab_holdings = [h for h in pv.holdings if h.capital_role == "stabiliser"]
    stab_cash = sum(c.value_aud for c in pv.cash if c.is_investable)
    stab_total = sum(h.value_aud for h in stab_holdings) + stab_cash
    if stab_total > 0:
        buckets: dict[str, float] = {}
        with get_connection(db_path) as conn:
            for h in stab_holdings:
                row = conn.execute("""
                    SELECT duration_years FROM instrument_classifications ic
                    JOIN instruments i ON i.id = ic.instrument_id
                    WHERE i.ticker = ?
                """, (h.ticker,)).fetchone()
                bucket = f"{row['duration_years']:.0f}y" if row and row["duration_years"] is not None else "unknown"
                buckets[bucket] = buckets.get(bucket, 0) + h.value_aud
        for bucket, value in buckets.items():
            if bucket == "unknown":
                continue
            pct = value / stab_total * 100
            buf = 40.0 - pct
            if buf < 5.0:
                report.rule_buffers.append(RuleBuffer(
                    rule_id="7.2", description=f"Duration bucket {bucket}",
                    current_value=pct, limit=40.0, buffer_pct=buf,
                    breach_move="Other stabiliser assets decline in value",
                ))

    report.rule_buffers.sort(key=lambda r: r.buffer_pct)
