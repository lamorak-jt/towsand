"""Import Interactive Brokers data from Flex reports into the Towsand database.

Maps IB Open Positions, Cash Report, and FX rates to the local schema.
"""

import logging
import re
from datetime import date

import pandas as pd

from src.db.connection import get_connection
from src.market_data.flex_report import ParsedFlexReport

logger = logging.getLogger(__name__)


def _normalize_date(d: str) -> str:
    """Ensure a date string is in ISO format (YYYY-MM-DD)."""
    d = str(d).strip()[:10]
    if re.match(r"^\d{8}$", d):
        return f"{d[:4]}-{d[4:6]}-{d[6:8]}"
    return d

# IB assetCategory → our instrument_type
ASSET_TYPE_MAP = {
    "STK": "equity",
    "ETF": "etf",
    "BOND": "govt_bond_nominal",
    "BILL": "govt_bond_nominal",
    "FUND": "listed_fund",
    "CASH": "cash",
    "WAR": "other",
    "OPT": "other",
    "FUT": "other",
    "FOP": "other",
}

# IB exchange codes that indicate ASX
ASX_EXCHANGES = {"ASX", "CXA", "ASXCEN"}

IB_ACCOUNT_NAME = "IB Trading AUD"


def _map_instrument_type(asset_category: str, sub_category: str = "",
                          description: str = "") -> str:
    """Map IB asset category + subCategory to our instrument_type enum."""
    sub = str(sub_category).upper()
    if sub == "ETF":
        return "etf"
    if sub in ("CLOSED-END FUND", "CLOSED-END"):
        return "listed_fund"

    mapped = ASSET_TYPE_MAP.get(str(asset_category).upper(), "other")
    desc_lower = str(description).lower()
    if mapped == "equity" and ("etf" in desc_lower or "ishares" in desc_lower
                               or "vanguard" in desc_lower or "betashares" in desc_lower):
        return "etf"
    return mapped


def _guess_country(currency: str, exchange: str = "") -> str:
    """Guess country domicile from currency and exchange."""
    if str(exchange).upper() in ASX_EXCHANGES:
        return "AU"
    country_map = {"AUD": "AU", "USD": "US", "EUR": "DE", "GBP": "GB", "JPY": "JP", "HKD": "HK", "CAD": "CA"}
    return country_map.get(str(currency).upper(), "")


def _ensure_ib_account(conn) -> int:
    """Get or verify the IB Trading account exists; return its id."""
    row = conn.execute("SELECT id FROM accounts WHERE name = ?", (IB_ACCOUNT_NAME,)).fetchone()
    if row is None:
        raise RuntimeError(
            f"Account '{IB_ACCOUNT_NAME}' not found. Run 'towsand init' first."
        )
    return row["id"]


def _upsert_instrument(conn, ticker: str, name: str, instrument_type: str,
                        exchange: str, currency: str, country: str) -> int:
    """Insert or update an instrument; return its id."""
    row = conn.execute("SELECT id FROM instruments WHERE ticker = ?", (ticker,)).fetchone()
    if row:
        conn.execute(
            "UPDATE instruments SET name=?, instrument_type=?, exchange=?, currency=?, country_domicile=? "
            "WHERE id=?",
            (name, instrument_type, exchange, currency, country, row["id"]),
        )
        return row["id"]
    conn.execute(
        "INSERT INTO instruments (ticker, name, instrument_type, exchange, currency, country_domicile) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (ticker, name, instrument_type, exchange, currency, country),
    )
    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def _upsert_holding(conn, account_id: int, instrument_id: int, quantity: float,
                     cost_basis: float | None, cost_basis_currency: str | None,
                     date_acquired: str | None) -> None:
    """Insert or update a holding."""
    row = conn.execute(
        "SELECT id FROM holdings WHERE account_id = ? AND instrument_id = ?",
        (account_id, instrument_id),
    ).fetchone()
    if row:
        conn.execute(
            "UPDATE holdings SET quantity=?, cost_basis=?, cost_basis_currency=?, "
            "date_acquired=?, updated_at=datetime('now') WHERE id=?",
            (quantity, cost_basis, cost_basis_currency, date_acquired, row["id"]),
        )
    else:
        conn.execute(
            "INSERT INTO holdings (account_id, instrument_id, quantity, cost_basis, "
            "cost_basis_currency, date_acquired) VALUES (?, ?, ?, ?, ?, ?)",
            (account_id, instrument_id, quantity, cost_basis, cost_basis_currency, date_acquired),
        )


def _upsert_price(conn, instrument_id: int, price_date: str, close_price: float,
                   currency: str) -> None:
    """Insert or update a price record."""
    conn.execute(
        "INSERT OR REPLACE INTO prices (instrument_id, date, close_price, currency, source) "
        "VALUES (?, ?, ?, ?, 'ib_flex')",
        (instrument_id, price_date, close_price, currency),
    )


def import_positions(report: ParsedFlexReport, db_path=None) -> dict:
    """Import open positions from a Flex report into the database.

    Returns a summary dict with counts.
    """
    df = report.open_positions()
    if df.empty:
        return {"instruments": 0, "holdings": 0, "prices": 0, "skipped": 0}

    # Filter to summary-level rows only (avoid lot-level duplicates)
    if "levelOfDetail" in df.columns:
        df = df[df["levelOfDetail"] == "SUMMARY"]

    today = date.today().isoformat()
    stats = {"instruments": 0, "holdings": 0, "prices": 0, "skipped": 0}

    with get_connection(db_path) as conn:
        account_id = _ensure_ib_account(conn)

        for _, row in df.iterrows():
            symbol = str(row.get("symbol", "")).strip()
            if not symbol:
                stats["skipped"] += 1
                continue

            asset_cat = str(row.get("assetCategory", ""))
            sub_cat = str(row.get("subCategory", ""))
            description = str(row.get("description", ""))
            currency = str(row.get("currency", "AUD"))
            exchange = str(row.get("listingExchange", row.get("exchange", "")))
            quantity = float(row.get("position", row.get("quantity", 0)))
            mark_price = row.get("markPrice")
            cost_basis_money = row.get("costBasisMoney")
            open_date = str(row.get("openDateTime", ""))[:10] or None

            # Build a ticker consistent with yfinance conventions
            instrument_type = _map_instrument_type(asset_cat, sub_cat, description)
            country = _guess_country(currency, exchange)
            ticker = symbol
            if country == "AU" and not ticker.endswith(".AX"):
                ticker = f"{symbol}.AX"

            instrument_id = _upsert_instrument(
                conn, ticker, description, instrument_type, exchange, currency, country
            )
            stats["instruments"] += 1

            _upsert_holding(
                conn, account_id, instrument_id, quantity,
                float(cost_basis_money) if cost_basis_money is not None else None,
                currency, open_date,
            )
            stats["holdings"] += 1

            if mark_price is not None and float(mark_price) > 0:
                report_date = _normalize_date(str(row.get("reportDate", today)))
                _upsert_price(conn, instrument_id, report_date, float(mark_price), currency)
                stats["prices"] += 1

    logger.info("Import positions complete: %s", stats)
    return stats


def import_cash(report: ParsedFlexReport, db_path=None) -> dict:
    """Import IB cash balances from a Flex report.

    The Cash Report section shows balances by currency.
    """
    df = report.cash_report()
    if df.empty:
        return {"balances": 0}

    # Filter to per-currency rows (exclude the base summary row)
    if "levelOfDetail" in df.columns:
        df = df[df["levelOfDetail"] == "Currency"]

    stats = {"balances": 0}

    with get_connection(db_path) as conn:
        account_id = _ensure_ib_account(conn)
        today = date.today().isoformat()

        for _, row in df.iterrows():
            currency = str(row.get("currency", "")).strip()
            if not currency or currency in ("BASE_SUMMARY", "BaseCurrency"):
                continue
            ending_cash = row.get("endingCash", row.get("endingSettledCash", 0))
            if ending_cash is None:
                continue

            conn.execute(
                "INSERT OR REPLACE INTO cash_balances (account_id, currency, balance, as_of_date) "
                "VALUES (?, ?, ?, ?)",
                (account_id, currency, float(ending_cash), today),
            )
            stats["balances"] += 1

    logger.info("Import cash complete: %s", stats)
    return stats


def import_fx_rates(report: ParsedFlexReport, db_path=None) -> dict:
    """Import FX rates from the Flex report.

    Tries the ConversionRate topic first (available when 'Include Currency Rates? Yes'
    is set in query config). Falls back to extracting fxRateToBase from positions.
    """
    # Try ConversionRate topic first (proper FX table with 39+ currency pairs)
    df = report.raw_df("ConversionRate")

    if not df.empty and "fromCurrency" in df.columns:
        return _import_conversion_rates(df, db_path)

    # Fallback: extract rates from position-level fxRateToBase
    df = report.fx_rates_from_positions()
    if df.empty:
        return {"rates": 0}
    return _import_fx_from_positions(df, db_path)


def _import_conversion_rates(df: pd.DataFrame, db_path=None) -> dict:
    """Import from the ConversionRate topic (fromCurrency, toCurrency, rate, reportDate)."""
    stats = {"rates": 0}

    with get_connection(db_path) as conn:
        for _, row in df.iterrows():
            from_curr = str(row.get("fromCurrency", "")).strip()
            to_curr = str(row.get("toCurrency", "")).strip()
            rate = row.get("rate")
            report_date = str(row.get("reportDate", ""))

            if not from_curr or not to_curr or rate is None or float(rate) == 0:
                continue

            conn.execute(
                "INSERT OR REPLACE INTO fx_rates (from_currency, to_currency, date, rate, source) "
                "VALUES (?, ?, ?, ?, 'ib_flex')",
                (from_curr, to_curr, _normalize_date(report_date), float(rate)),
            )
            stats["rates"] += 1

    logger.info("Import FX rates (ConversionRate) complete: %s", stats)
    return stats


def _import_fx_from_positions(df: pd.DataFrame, db_path=None) -> dict:
    """Fallback: extract fxRateToBase from open positions."""
    stats = {"rates": 0}
    today = date.today().isoformat()

    with get_connection(db_path) as conn:
        base_row = conn.execute(
            "SELECT value FROM parameters WHERE key = 'base_currency'"
        ).fetchone()
        base = base_row["value"] if base_row else "AUD"

        for _, row in df.iterrows():
            from_curr = str(row.get("currency", "")).strip()
            rate = row.get("fxRateToBase")
            report_date = str(row.get("reportDate", today))[:10]

            if not from_curr or rate is None or float(rate) == 0:
                continue

            conn.execute(
                "INSERT OR REPLACE INTO fx_rates (from_currency, to_currency, date, rate, source) "
                "VALUES (?, ?, ?, ?, 'ib_flex')",
                (from_curr, base, _normalize_date(report_date), float(rate)),
            )
            stats["rates"] += 1

    logger.info("Import FX rates (fxRateToBase fallback) complete: %s", stats)
    return stats


def import_all(report: ParsedFlexReport, db_path=None) -> dict:
    """Run all importers on a Flex report. Returns combined stats."""
    results = {}
    results["positions"] = import_positions(report, db_path)
    results["cash"] = import_cash(report, db_path)
    results["fx"] = import_fx_rates(report, db_path)
    return results
