"""Portfolio valuation engine.

Computes market value in AUD for every holding and cash balance,
using the latest prices and FX rates from the database.
"""

import logging
from dataclasses import dataclass, field

from src.db.connection import get_connection

logger = logging.getLogger(__name__)


@dataclass
class HoldingValue:
    """A single holding with its current valuation."""
    ticker: str
    name: str
    instrument_type: str
    exchange: str | None
    currency: str
    country: str | None
    account_name: str
    institution_name: str
    quantity: float
    price: float
    price_date: str
    local_value: float   # quantity * price in local currency
    fx_rate: float       # to AUD (1.0 if already AUD)
    value_aud: float     # local_value * fx_rate
    capital_role: str | None = None
    macro_drivers: str | None = None
    corporate_group: str | None = None
    asset_class: str | None = None
    economic_currency: str | None = None


@dataclass
class CashValue:
    """A single cash balance with AUD conversion."""
    account_name: str
    institution_name: str
    currency: str
    balance: float
    fx_rate: float
    value_aud: float
    as_of_date: str
    is_investable: bool = True  # False for receivables, credit card liabilities


@dataclass
class PortfolioValuation:
    """Complete portfolio snapshot."""
    holdings: list[HoldingValue] = field(default_factory=list)
    cash: list[CashValue] = field(default_factory=list)

    @property
    def total_holdings_aud(self) -> float:
        return sum(h.value_aud for h in self.holdings)

    @property
    def total_cash_aud(self) -> float:
        return sum(c.value_aud for c in self.cash)

    @property
    def investable_cash_aud(self) -> float:
        """Cash included in investable assets (excludes receivables, credit liabilities)."""
        return sum(c.value_aud for c in self.cash if c.is_investable)

    @property
    def non_investable_cash_aud(self) -> float:
        """Cash excluded from investable assets (receivables, credit liabilities)."""
        return sum(c.value_aud for c in self.cash if not c.is_investable)

    @property
    def total_aud(self) -> float:
        """Total investable assets (holdings + investable cash). Used as the denominator
        for all percentage-based compliance rules. See portfolio-management-rules.md §0."""
        return self.total_holdings_aud + self.investable_cash_aud

    def by_capital_role(self) -> dict[str, float]:
        """Aggregate AUD value by capital role (stabiliser/compounder/optionality/unclassified).

        Cash balances are allocated to stabiliser: cash satisfies every stabiliser
        criterion (liquid, short duration, yield-bearing) and its optionality value
        is a portfolio-level strategic property, not an instrument payoff shape.
        """
        result: dict[str, float] = {}
        for h in self.holdings:
            role = h.capital_role or "unclassified"
            result[role] = result.get(role, 0) + h.value_aud
        # Investable cash → stabiliser: liquid, short-duration, yield-bearing capital
        # Non-investable (receivables, credit liabilities) excluded per §0.
        inv_cash = sum(c.value_aud for c in self.cash if c.is_investable)
        if inv_cash:
            result["stabiliser"] = result.get("stabiliser", 0) + inv_cash
        return result

    def by_instrument_type(self) -> dict[str, float]:
        """Aggregate AUD value by instrument type."""
        result: dict[str, float] = {}
        for h in self.holdings:
            result[h.instrument_type] = result.get(h.instrument_type, 0) + h.value_aud
        return result

    def by_currency(self) -> dict[str, float]:
        """Aggregate AUD value by original currency (holdings + investable cash)."""
        result: dict[str, float] = {}
        for h in self.holdings:
            result[h.currency] = result.get(h.currency, 0) + h.value_aud
        for c in self.cash:
            if c.is_investable:
                result[c.currency] = result.get(c.currency, 0) + c.value_aud
        return result

    def by_country(self) -> dict[str, float]:
        """Aggregate AUD value by country domicile (holdings only)."""
        result: dict[str, float] = {}
        for h in self.holdings:
            country = h.country or "Unknown"
            result[country] = result.get(country, 0) + h.value_aud
        return result

    def by_institution(self) -> dict[str, float]:
        """Aggregate AUD value by institution (holdings + investable cash)."""
        result: dict[str, float] = {}
        for h in self.holdings:
            result[h.institution_name] = result.get(h.institution_name, 0) + h.value_aud
        for c in self.cash:
            if c.is_investable:
                result[c.institution_name] = result.get(c.institution_name, 0) + c.value_aud
        return result

    def by_account(self) -> dict[str, float]:
        """Aggregate AUD value by account (holdings + investable cash)."""
        result: dict[str, float] = {}
        for h in self.holdings:
            result[h.account_name] = result.get(h.account_name, 0) + h.value_aud
        for c in self.cash:
            if c.is_investable:
                result[c.account_name] = result.get(c.account_name, 0) + c.value_aud
        return result

    def by_macro_driver(self) -> dict[str, float]:
        """Aggregate AUD value by macro driver (an instrument may have multiple)."""
        import json
        result: dict[str, float] = {}
        for h in self.holdings:
            drivers = []
            if h.macro_drivers:
                try:
                    drivers = json.loads(h.macro_drivers)
                except (json.JSONDecodeError, TypeError):
                    pass
            if not drivers:
                drivers = ["untagged"]
            for d in drivers:
                result[d] = result.get(d, 0) + h.value_aud
        return result


def project_valuation(
    pv: "PortfolioValuation",
    trades: list[dict],
    db_path=None,
) -> "PortfolioValuation":
    """Apply hypothetical trades to produce a projected portfolio.

    Args:
        pv: Current portfolio valuation.
        trades: List of trade dicts, each with:
            - ticker (str): instrument ticker
            - delta_aud (float): AUD amount change (+buy, -sell)
            - capital_role (str, optional): override role for new instruments
            - currency (str, optional): override listing currency (default AUD)
            - instrument_type (str, optional): override type for new instruments
            - asset_class (str, optional): economic asset class (equity/credit/govt_bond_nominal/etc.)
            - economic_currency (str, optional): currency of economic exposure
        db_path: Optional database path override.

    Returns:
        A new PortfolioValuation with trades applied.

    For existing holdings, scales the position proportionally.
    For new instruments (not in current holdings), looks up classification
    data from the database and creates a new holding entry.
    Net cash impact (sum of sells minus buys) adjusts investable cash.
    """
    from copy import deepcopy

    projected = PortfolioValuation()
    projected.cash = deepcopy(pv.cash)

    trade_map: dict[str, float] = {}
    for t in trades:
        ticker = t["ticker"]
        trade_map[ticker] = trade_map.get(ticker, 0) + t["delta_aud"]

    # Apply deltas to existing holdings
    seen_tickers: set[str] = set()
    for h in pv.holdings:
        delta = trade_map.get(h.ticker, 0)
        new_value = h.value_aud + delta
        seen_tickers.add(h.ticker)

        if new_value <= 0:
            continue  # fully sold

        scale = new_value / h.value_aud if h.value_aud > 0 else 0
        projected.holdings.append(HoldingValue(
            ticker=h.ticker,
            name=h.name,
            instrument_type=h.instrument_type,
            exchange=h.exchange,
            currency=h.currency,
            country=h.country,
            account_name=h.account_name,
            institution_name=h.institution_name,
            quantity=h.quantity * scale,
            price=h.price,
            price_date=h.price_date,
            local_value=h.local_value * scale,
            fx_rate=h.fx_rate,
            value_aud=new_value,
            capital_role=h.capital_role,
            macro_drivers=h.macro_drivers,
            corporate_group=h.corporate_group,
            asset_class=h.asset_class,
            economic_currency=h.economic_currency,
        ))

    # Build a lookup of per-ticker overrides from trade dicts
    trade_overrides: dict[str, dict] = {}
    for t in trades:
        ticker = t["ticker"]
        trade_overrides[ticker] = t

    # Add new instruments not currently held
    new_tickers = {t: d for t, d in trade_map.items() if t not in seen_tickers and d > 0}
    if new_tickers:
        from src.db.connection import get_connection
        with get_connection(db_path) as conn:
            for ticker, amount_aud in new_tickers.items():
                overrides = trade_overrides.get(ticker, {})

                row = conn.execute("""
                    SELECT i.ticker, i.name, i.instrument_type, i.exchange,
                           i.currency, i.country_domicile,
                           ic.capital_role, ic.macro_drivers, ic.corporate_group,
                           ic.asset_class, ic.economic_currency
                    FROM instruments i
                    LEFT JOIN instrument_classifications ic ON ic.instrument_id = i.id
                    WHERE i.ticker = ?
                """, (ticker,)).fetchone()

                if row:
                    currency = overrides.get("currency", row["currency"])
                    fx_rate = _get_fx_rate(conn, currency) or 1.0
                    local_value = amount_aud / fx_rate
                    price_row = conn.execute("""
                        SELECT close_price, date FROM prices p
                        JOIN instruments i ON i.id = p.instrument_id
                        WHERE i.ticker = ? ORDER BY p.date DESC LIMIT 1
                    """, (ticker,)).fetchone()
                    price = price_row["close_price"] if price_row else 0
                    price_date = price_row["date"] if price_row else ""
                    quantity = local_value / price if price > 0 else 0

                    projected.holdings.append(HoldingValue(
                        ticker=row["ticker"],
                        name=row["name"] or ticker,
                        instrument_type=overrides.get("instrument_type", row["instrument_type"]),
                        exchange=row["exchange"],
                        currency=currency,
                        country=row["country_domicile"],
                        account_name="(projected)",
                        institution_name="(projected)",
                        quantity=quantity,
                        price=price,
                        price_date=price_date,
                        local_value=local_value,
                        fx_rate=fx_rate,
                        value_aud=amount_aud,
                        capital_role=overrides.get("capital_role", row["capital_role"]),
                        macro_drivers=row["macro_drivers"],
                        corporate_group=overrides.get("corporate_group", row["corporate_group"]),
                        asset_class=overrides.get("asset_class", row["asset_class"]),
                        economic_currency=overrides.get("economic_currency", row["economic_currency"]),
                    ))
                else:
                    logger.warning(
                        "Instrument %s not in database — using trade-spec metadata for projection",
                        ticker,
                    )
                    currency = overrides.get("currency", "AUD")
                    projected.holdings.append(HoldingValue(
                        ticker=ticker, name=ticker,
                        instrument_type=overrides.get("instrument_type", "etf"),
                        exchange=None,
                        currency=currency, country=None,
                        account_name="(projected)", institution_name="(projected)",
                        quantity=0, price=0, price_date="",
                        local_value=amount_aud, fx_rate=1.0, value_aud=amount_aud,
                        capital_role=overrides.get("capital_role"),
                        macro_drivers=overrides.get("macro_drivers"),
                        corporate_group=overrides.get("corporate_group"),
                        asset_class=overrides.get("asset_class"),
                        economic_currency=overrides.get("economic_currency", currency),
                    ))

    # Adjust investable cash by net trade flow (sells add, buys consume)
    net_cash_delta = -sum(trade_map.values())  # negative delta_aud = sell = cash in
    if net_cash_delta != 0 and projected.cash:
        # Apply to the first investable cash balance
        for cv in projected.cash:
            if cv.is_investable:
                cv.balance += net_cash_delta / cv.fx_rate
                cv.value_aud += net_cash_delta
                break

    return projected


def _get_fx_rate(conn, from_currency: str, to_currency: str = "AUD") -> float | None:
    """Get the latest FX rate for a currency pair."""
    if from_currency == to_currency:
        return 1.0
    row = conn.execute(
        "SELECT rate FROM fx_rates "
        "WHERE from_currency = ? AND to_currency = ? "
        "ORDER BY date DESC LIMIT 1",
        (from_currency, to_currency),
    ).fetchone()
    return row["rate"] if row else None


def compute_valuation(db_path=None) -> PortfolioValuation:
    """Compute the full portfolio valuation.

    For each holding: latest price * quantity * FX rate → AUD.
    For each cash balance: balance * FX rate → AUD.
    Includes classification data (capital_role, macro_drivers, corporate_group).
    """
    pv = PortfolioValuation()

    with get_connection(db_path) as conn:
        # Holdings with latest prices and classifications
        rows = conn.execute("""
            SELECT
                i.ticker, i.name, i.instrument_type, i.exchange, i.currency,
                i.country_domicile,
                a.name AS account_name,
                inst.name AS institution_name,
                h.quantity,
                p.close_price, p.date AS price_date,
                ic.capital_role, ic.macro_drivers, ic.corporate_group,
                ic.asset_class, ic.economic_currency
            FROM holdings h
            JOIN instruments i ON i.id = h.instrument_id
            JOIN accounts a ON a.id = h.account_id
            JOIN institutions inst ON inst.id = a.institution_id
            LEFT JOIN prices p ON p.instrument_id = i.id
                AND p.date = (SELECT MAX(p2.date) FROM prices p2 WHERE p2.instrument_id = i.id)
            LEFT JOIN instrument_classifications ic ON ic.instrument_id = i.id
            ORDER BY i.ticker
        """).fetchall()

        for r in rows:
            price = r["close_price"] or 0
            quantity = r["quantity"]
            local_value = quantity * price
            fx_rate = _get_fx_rate(conn, r["currency"]) or 1.0
            value_aud = local_value * fx_rate

            if price == 0:
                logger.warning("No price for %s — valued at 0", r["ticker"])

            pv.holdings.append(HoldingValue(
                ticker=r["ticker"],
                name=r["name"] or "",
                instrument_type=r["instrument_type"],
                exchange=r["exchange"],
                currency=r["currency"],
                country=r["country_domicile"],
                account_name=r["account_name"],
                institution_name=r["institution_name"],
                quantity=quantity,
                price=price,
                price_date=r["price_date"] or "",
                local_value=local_value,
                fx_rate=fx_rate,
                value_aud=value_aud,
                capital_role=r["capital_role"],
                macro_drivers=r["macro_drivers"],
                corporate_group=r["corporate_group"],
                asset_class=r["asset_class"],
                economic_currency=r["economic_currency"],
            ))

        # Cash balances
        # Determine excluded accounts (receivables, credit liabilities)
        exclude_param = conn.execute(
            "SELECT value FROM parameters WHERE key = 'exclude_account_ids'"
        ).fetchone()
        if exclude_param:
            import json
            exclude_ids = set(json.loads(exclude_param["value"]))
        else:
            # Default: exclude credit-type accounts
            exclude_ids = set()
            for row in conn.execute("SELECT id FROM accounts WHERE account_type = 'credit'"):
                exclude_ids.add(row["id"])

        cash_rows = conn.execute("""
            SELECT
                a.id AS account_id,
                a.name AS account_name,
                inst.name AS institution_name,
                cb.currency, cb.balance, cb.as_of_date
            FROM cash_balances cb
            JOIN accounts a ON a.id = cb.account_id
            JOIN institutions inst ON inst.id = a.institution_id
            WHERE (cb.account_id, cb.currency, cb.as_of_date) IN (
                SELECT account_id, currency, MAX(as_of_date)
                FROM cash_balances
                GROUP BY account_id, currency
            )
            ORDER BY inst.name, a.name, cb.currency
        """).fetchall()

        for r in cash_rows:
            fx_rate = _get_fx_rate(conn, r["currency"]) or 1.0
            value_aud = r["balance"] * fx_rate
            investable = r["account_id"] not in exclude_ids

            pv.cash.append(CashValue(
                account_name=r["account_name"],
                institution_name=r["institution_name"],
                currency=r["currency"],
                balance=r["balance"],
                fx_rate=fx_rate,
                value_aud=value_aud,
                as_of_date=r["as_of_date"],
                is_investable=investable,
            ))

    return pv
