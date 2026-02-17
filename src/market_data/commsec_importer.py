"""Import CommSec portfolio data from CSV export into the Towsand database.

CommSec CSV exports typically contain columns like:
  Code, Company, Qty/Quantity, Avg Price/Purchase Price, Market Price, Value, Gain/Loss

This importer uses flexible column matching to handle variations in export format.
"""

import logging
from datetime import date
from pathlib import Path

import pandas as pd

from src.db.connection import get_connection

logger = logging.getLogger(__name__)

COMMSEC_ACCOUNT_NAME = "CommSec Trading"

# Flexible column name matching — maps our internal names to possible CSV header variations
COLUMN_ALIASES = {
    "ticker": ["code", "asx code", "symbol", "ticker", "stock code"],
    "name": ["company", "name", "description", "security", "stock name"],
    "quantity": ["qty", "quantity", "units", "holding", "shares"],
    "cost_price": ["avg price", "average price", "purchase price", "cost price", "cost basis"],
    "market_price": ["market price", "last price", "price", "current price", "close"],
    "market_value": ["value", "market value", "current value", "total value"],
}


def _find_column(df: pd.DataFrame, aliases: list[str]) -> str | None:
    """Find a DataFrame column matching one of the given aliases (case-insensitive)."""
    df_cols_lower = {c.strip().lower(): c for c in df.columns}
    for alias in aliases:
        if alias.lower() in df_cols_lower:
            return df_cols_lower[alias.lower()]
    return None


def _resolve_columns(df: pd.DataFrame) -> dict[str, str | None]:
    """Map our internal column names to actual CSV column names."""
    resolved = {}
    for key, aliases in COLUMN_ALIASES.items():
        resolved[key] = _find_column(df, aliases)
    return resolved


def _ensure_commsec_account(conn) -> int:
    """Get the CommSec Trading account id."""
    row = conn.execute("SELECT id FROM accounts WHERE name = ?", (COMMSEC_ACCOUNT_NAME,)).fetchone()
    if row is None:
        raise RuntimeError(
            f"Account '{COMMSEC_ACCOUNT_NAME}' not found. Run 'towsand init' first."
        )
    return row["id"]


def import_commsec_csv(csv_path: str | Path, db_path=None) -> dict:
    """Import a CommSec CSV portfolio export.

    The CSV is expected to have at minimum: a ticker/code column and a quantity column.
    Cost basis and market price columns are used if present.

    Returns a summary dict with counts.
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    cols = _resolve_columns(df)
    logger.info("Resolved columns: %s", {k: v for k, v in cols.items() if v})

    if cols["ticker"] is None:
        raise ValueError(
            f"Cannot find a ticker/code column. Available columns: {list(df.columns)}. "
            f"Expected one of: {COLUMN_ALIASES['ticker']}"
        )
    if cols["quantity"] is None:
        raise ValueError(
            f"Cannot find a quantity column. Available columns: {list(df.columns)}. "
            f"Expected one of: {COLUMN_ALIASES['quantity']}"
        )

    today = date.today().isoformat()
    stats = {"instruments": 0, "holdings": 0, "prices": 0, "skipped": 0}

    with get_connection(db_path) as conn:
        account_id = _ensure_commsec_account(conn)

        for _, row in df.iterrows():
            raw_ticker = str(row[cols["ticker"]]).strip().upper()
            if not raw_ticker or raw_ticker == "NAN":
                stats["skipped"] += 1
                continue

            ticker = raw_ticker if raw_ticker.endswith(".AX") else f"{raw_ticker}.AX"
            name = str(row[cols["name"]]).strip() if cols["name"] else ""
            quantity = float(row[cols["quantity"]])

            cost_basis = None
            if cols["cost_price"] is not None:
                try:
                    cost_basis = float(row[cols["cost_price"]]) * quantity
                except (ValueError, TypeError):
                    pass

            market_price = None
            if cols["market_price"] is not None:
                try:
                    market_price = float(row[cols["market_price"]])
                except (ValueError, TypeError):
                    pass

            # Upsert instrument
            existing = conn.execute("SELECT id FROM instruments WHERE ticker = ?", (ticker,)).fetchone()
            if existing:
                instrument_id = existing["id"]
                if name:
                    conn.execute("UPDATE instruments SET name=? WHERE id=?", (name, instrument_id))
            else:
                conn.execute(
                    "INSERT INTO instruments (ticker, name, instrument_type, exchange, currency, country_domicile) "
                    "VALUES (?, ?, 'equity', 'ASX', 'AUD', 'AU')",
                    (ticker, name),
                )
                instrument_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            stats["instruments"] += 1

            # Upsert holding
            existing_holding = conn.execute(
                "SELECT id FROM holdings WHERE account_id = ? AND instrument_id = ?",
                (account_id, instrument_id),
            ).fetchone()
            if existing_holding:
                conn.execute(
                    "UPDATE holdings SET quantity=?, cost_basis=?, cost_basis_currency='AUD', "
                    "updated_at=datetime('now') WHERE id=?",
                    (quantity, cost_basis, existing_holding["id"]),
                )
            else:
                conn.execute(
                    "INSERT INTO holdings (account_id, instrument_id, quantity, cost_basis, cost_basis_currency) "
                    "VALUES (?, ?, ?, ?, 'AUD')",
                    (account_id, instrument_id, quantity, cost_basis),
                )
            stats["holdings"] += 1

            # Store market price if available
            if market_price is not None and market_price > 0:
                conn.execute(
                    "INSERT OR REPLACE INTO prices (instrument_id, date, close_price, currency, source) "
                    "VALUES (?, ?, ?, 'AUD', 'commsec_csv')",
                    (instrument_id, today, market_price),
                )
                stats["prices"] += 1

    logger.info("CommSec import complete: %s", stats)
    return stats
