"""Stress scenario testing — objective-level assessment.

Applies historical or synthetic drawdown scenarios to the current portfolio
and evaluates the impact against the strategy's ultimate objectives:

1. SURVIVABILITY — Am I forced to sell long-term assets?
2. INCOME BRIDGE — Can I still fund 24+ months of living expenses?
3. COMPOUNDING DAMAGE — How much long-term wealth was destroyed, and how
   long to recover at expected real returns?
4. OPTIONALITY PAYOFF — Did optionality capital perform its crisis function?
5. REAL WEALTH — What happened to total purchasing power?

Compliance rule breaches are reported as secondary evidence, not the headline.

Strategy reference: current-finances/strategy-assumptions.md
"""

import logging
from dataclasses import dataclass, field
from datetime import date

from src.db.connection import get_connection
from src.portfolio.valuation import PortfolioValuation, HoldingValue
from src.compliance.checks import run_all_checks, CheckResult

logger = logging.getLogger(__name__)

REAL_RETURN_PA = 0.065  # midpoint of Strategy §3 expectation (6–7% real)

SCENARIOS = {
    "flat35": {
        "name": "Flat 35% Equity Haircut",
        "description": "Synthetic: all compounder + optionality holdings lose 35%.",
        "type": "synthetic",
    },
    "covid2020": {
        "name": "COVID-19 Drawdown (Feb–Mar 2020)",
        "description": "Peak-to-trough drawdown during Feb 19 – Mar 23 2020.",
        "start": "2020-02-19",
        "trough": "2020-03-23",
        "type": "historical",
    },
    "gfc2008": {
        "name": "Global Financial Crisis (2007–2009)",
        "description": "Peak-to-trough drawdown during the GFC.",
        "start": "2007-10-09",
        "trough": "2009-03-09",
        "type": "historical",
    },
    "rates2022": {
        "name": "2022 Rate Shock (Jan–Oct 2022)",
        "description": "Combined equity + bond drawdown during 2022 rate tightening.",
        "start": "2022-01-03",
        "trough": "2022-10-14",
        "type": "historical",
    },
}

PROXY_DRAWDOWNS = {
    "covid2020": {
        "equity": -0.35, "etf": -0.30, "credit": -0.15,
        "listed_fund": -0.25, "govt_bond_nominal": 0.02,
        "govt_bond_indexed": 0.0, "cash": 0.0, "other": -0.20,
    },
    "gfc2008": {
        "equity": -0.55, "etf": -0.45, "credit": -0.30,
        "listed_fund": -0.40, "govt_bond_nominal": 0.10,
        "govt_bond_indexed": 0.05, "cash": 0.0, "other": -0.30,
    },
    "rates2022": {
        "equity": -0.25, "etf": -0.20, "credit": -0.10,
        "listed_fund": -0.15, "govt_bond_nominal": -0.15,
        "govt_bond_indexed": -0.10, "cash": 0.0, "other": -0.15,
    },
}


@dataclass
class HoldingStress:
    ticker: str
    capital_role: str | None
    pre_stress_aud: float
    drawdown_pct: float
    post_stress_aud: float
    source: str


@dataclass
class ObjectiveAssessment:
    """Assessment of a stress scenario against each strategy objective."""
    # 1. Survivability
    forced_liquidation: bool = False
    forced_liquidation_detail: str = ""

    # 2. Income bridge
    income_bridge_months_pre: float = 0
    income_bridge_months_post: float = 0
    income_bridge_months_lost: float = 0
    income_bridge_intact: bool = True

    # 3. Compounding damage
    compounder_pre_aud: float = 0
    compounder_post_aud: float = 0
    compounder_loss_aud: float = 0
    compounder_loss_pct: float = 0
    recovery_years: float = 0  # years at real return to recover lost compounder capital

    # 4. Optionality payoff
    optionality_pre_aud: float = 0
    optionality_post_aud: float = 0
    optionality_change_pct: float = 0
    optionality_performed: bool = False  # True if it lost less than compounders or gained

    # 5. Real wealth
    total_pre_aud: float = 0
    total_post_aud: float = 0
    wealth_loss_aud: float = 0
    wealth_loss_pct: float = 0


@dataclass
class StressResult:
    scenario_id: str
    scenario_name: str
    description: str
    objectives: ObjectiveAssessment = field(default_factory=ObjectiveAssessment)
    holding_stresses: list[HoldingStress] = field(default_factory=list)
    # Compliance kept as secondary evidence
    compliance_results: list[CheckResult] = field(default_factory=list)
    breaches: list[CheckResult] = field(default_factory=list)
    warnings: list[CheckResult] = field(default_factory=list)


def _get_historical_drawdown(
    ticker: str, exchange: str | None, start: str, trough: str, db_path=None,
) -> float | None:
    with get_connection(db_path) as conn:
        inst = conn.execute(
            "SELECT id FROM instruments WHERE ticker = ?", (ticker,)
        ).fetchone()
        if not inst:
            return None
        start_row = conn.execute(
            "SELECT close_price FROM prices WHERE instrument_id = ? AND date <= ? "
            "ORDER BY date DESC LIMIT 1",
            (inst["id"], start),
        ).fetchone()
        trough_row = conn.execute(
            "SELECT close_price FROM prices WHERE instrument_id = ? AND date <= ? "
            "ORDER BY date DESC LIMIT 1",
            (inst["id"], trough),
        ).fetchone()
    if not start_row or not trough_row or start_row["close_price"] <= 0:
        return None
    return (trough_row["close_price"] - start_row["close_price"]) / start_row["close_price"]


def _apply_drawdown(pv: PortfolioValuation, drawdowns: dict[str, float]) -> PortfolioValuation:
    stressed = PortfolioValuation()
    stressed.cash = pv.cash
    for h in pv.holdings:
        dd = drawdowns.get(h.ticker, 0.0)
        stressed.holdings.append(HoldingValue(
            ticker=h.ticker, name=h.name,
            instrument_type=h.instrument_type, exchange=h.exchange,
            currency=h.currency, country=h.country,
            account_name=h.account_name, institution_name=h.institution_name,
            quantity=h.quantity,
            price=h.price * (1 + dd) if h.price else 0,
            price_date=h.price_date,
            local_value=h.local_value * (1 + dd),
            fx_rate=h.fx_rate,
            value_aud=h.value_aud * (1 + dd),
            capital_role=h.capital_role,
            macro_drivers=h.macro_drivers,
            corporate_group=h.corporate_group,
        ))
    return stressed


def _assess_objectives(
    pv: PortfolioValuation, stressed_pv: PortfolioValuation,
    monthly_expenses: float,
) -> ObjectiveAssessment:
    """Evaluate the stressed portfolio against each strategy objective."""
    obj = ObjectiveAssessment()

    roles_pre = pv.by_capital_role()
    roles_post = stressed_pv.by_capital_role()

    stab_pre = roles_pre.get("stabiliser", 0)
    stab_post = roles_post.get("stabiliser", 0)
    comp_pre = roles_pre.get("compounder", 0)
    comp_post = roles_post.get("compounder", 0)
    opt_pre = roles_pre.get("optionality", 0)
    opt_post = roles_post.get("optionality", 0)

    min_stab = 24 * monthly_expenses

    # 1. Survivability — forced to sell long-term assets?
    obj.forced_liquidation = stab_post < min_stab
    if obj.forced_liquidation:
        shortfall = min_stab - stab_post
        obj.forced_liquidation_detail = (
            f"YES — stabiliser AUD {stab_post:,.0f} falls below 24-month floor "
            f"AUD {min_stab:,.0f}. Must sell AUD {shortfall:,.0f} of compounders/optionality "
            f"to cover living expenses. Long-term capital permanently impaired."
        )
    else:
        obj.forced_liquidation_detail = (
            f"No — stabiliser AUD {stab_post:,.0f} still covers "
            f"{stab_post / monthly_expenses:.0f} months. No forced selling."
        )

    # 2. Income bridge
    obj.income_bridge_months_pre = stab_pre / monthly_expenses if monthly_expenses else 0
    obj.income_bridge_months_post = stab_post / monthly_expenses if monthly_expenses else 0
    obj.income_bridge_months_lost = obj.income_bridge_months_pre - obj.income_bridge_months_post
    obj.income_bridge_intact = obj.income_bridge_months_post >= 24

    # 3. Compounding damage
    obj.compounder_pre_aud = comp_pre
    obj.compounder_post_aud = comp_post
    obj.compounder_loss_aud = comp_pre - comp_post
    obj.compounder_loss_pct = (
        (obj.compounder_loss_aud / comp_pre * 100) if comp_pre > 0 else 0
    )
    # Recovery time: years at real return to grow comp_post back to comp_pre
    # comp_post * (1 + r)^n = comp_pre → n = ln(comp_pre/comp_post) / ln(1+r)
    import math
    if comp_post > 0 and comp_pre > comp_post:
        obj.recovery_years = math.log(comp_pre / comp_post) / math.log(1 + REAL_RETURN_PA)
    else:
        obj.recovery_years = 0

    # 4. Optionality payoff
    obj.optionality_pre_aud = opt_pre
    obj.optionality_post_aud = opt_post
    obj.optionality_change_pct = (
        ((opt_post - opt_pre) / opt_pre * 100) if opt_pre > 0 else 0
    )
    comp_change_pct = (
        ((comp_post - comp_pre) / comp_pre * 100) if comp_pre > 0 else 0
    )
    # Optionality "performed" if it gained, or lost materially less than compounders
    obj.optionality_performed = (
        obj.optionality_change_pct > 0
        or (obj.optionality_change_pct > comp_change_pct + 10)
    )

    # 5. Real wealth
    obj.total_pre_aud = pv.total_aud
    obj.total_post_aud = stressed_pv.total_aud
    obj.wealth_loss_aud = pv.total_aud - stressed_pv.total_aud
    obj.wealth_loss_pct = (
        (obj.wealth_loss_aud / pv.total_aud * 100) if pv.total_aud > 0 else 0
    )

    return obj


def run_scenario(
    pv: PortfolioValuation, scenario_id: str, db_path=None,
) -> StressResult:
    if scenario_id not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario_id}. Available: {list(SCENARIOS.keys())}")

    scenario = SCENARIOS[scenario_id]
    result = StressResult(
        scenario_id=scenario_id,
        scenario_name=scenario["name"],
        description=scenario["description"],
    )

    drawdowns: dict[str, float] = {}
    holding_stresses: list[HoldingStress] = []

    if scenario["type"] == "synthetic":
        for h in pv.holdings:
            dd = -0.35 if h.capital_role in ("compounder", "optionality") else 0.0
            drawdowns[h.ticker] = dd
            holding_stresses.append(HoldingStress(
                ticker=h.ticker, capital_role=h.capital_role,
                pre_stress_aud=h.value_aud, drawdown_pct=dd * 100,
                post_stress_aud=h.value_aud * (1 + dd), source="synthetic",
            ))
    elif scenario["type"] == "historical":
        start, trough = scenario["start"], scenario["trough"]
        proxies = PROXY_DRAWDOWNS.get(scenario_id, {})
        for h in pv.holdings:
            historical_dd = _get_historical_drawdown(
                h.ticker, h.exchange, start, trough, db_path)
            if historical_dd is not None:
                dd, source = historical_dd, "historical"
            else:
                dd, source = proxies.get(h.instrument_type, -0.20), "proxy"
            drawdowns[h.ticker] = dd
            holding_stresses.append(HoldingStress(
                ticker=h.ticker, capital_role=h.capital_role,
                pre_stress_aud=h.value_aud, drawdown_pct=dd * 100,
                post_stress_aud=h.value_aud * (1 + dd), source=source,
            ))

    result.holding_stresses = holding_stresses
    stressed_pv = _apply_drawdown(pv, drawdowns)

    with get_connection(db_path) as conn:
        monthly = float(conn.execute(
            "SELECT value FROM parameters WHERE key = 'monthly_expenses'"
        ).fetchone()["value"] or "9000")

    result.objectives = _assess_objectives(pv, stressed_pv, monthly)

    # Compliance as secondary evidence
    result.compliance_results = run_all_checks(stressed_pv, db_path)
    result.breaches = [r for r in result.compliance_results if r.status == "breach"]
    result.warnings = [r for r in result.compliance_results if r.status == "warning"]

    return result


def run_all_scenarios(pv: PortfolioValuation, db_path=None) -> list[StressResult]:
    results = []
    for scenario_id in SCENARIOS:
        try:
            results.append(run_scenario(pv, scenario_id, db_path))
        except Exception as exc:
            logger.warning("Scenario %s failed: %s", scenario_id, exc)
    return results
