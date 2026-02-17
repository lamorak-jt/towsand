"""Import CommSec portfolio holdings scraped from the browser into the Towsand database.

This module handles importing holdings data extracted from the CommSec portfolio page.
"""

import logging
from datetime import date

from src.db.connection import get_connection
from src.market_data.commsec_importer import _ensure_commsec_account

logger = logging.getLogger(__name__)


def import_scraped_holdings(holdings: list[dict], db_path=None) -> dict:
    """Import scraped holdings data into the database.

    Args:
        holdings: List of dicts, each containing:
            - ticker: ASX code (e.g., "GSBG27")
            - name: Company/fund name (optional)
            - quantity: Number of units held
            - purchase_price: Average purchase price per unit
            - market_price: Current market price per unit
            - market_value: Current market value (optional, calculated if not provided)
        db_path: Optional database path

    Returns:
        Summary dict with counts: {"instruments": int, "holdings": int, "prices": int, "skipped": int}
    """
    today = date.today().isoformat()
    stats = {"instruments": 0, "holdings": 0, "prices": 0, "skipped": 0}

    with get_connection(db_path) as conn:
        account_id = _ensure_commsec_account(conn)

        for holding in holdings:
            raw_ticker = str(holding.get("ticker", "")).strip().upper()
            if not raw_ticker:
                stats["skipped"] += 1
                logger.warning("Skipping holding with no ticker: %s", holding)
                continue

            # Ensure .AX suffix for ASX stocks
            ticker = raw_ticker if raw_ticker.endswith(".AX") else f"{raw_ticker}.AX"
            name = str(holding.get("name", "")).strip()
            quantity = float(holding.get("quantity", 0))

            if quantity <= 0:
                stats["skipped"] += 1
                logger.warning("Skipping holding with invalid quantity: %s", holding)
                continue

            # Calculate cost basis from purchase price
            purchase_price = holding.get("purchase_price")
            cost_basis = None
            if purchase_price is not None:
                try:
                    cost_basis = float(purchase_price) * quantity
                except (ValueError, TypeError):
                    logger.warning("Invalid purchase_price for %s: %s", ticker, purchase_price)

            # Get market price
            market_price = holding.get("market_price")
            if market_price is not None:
                try:
                    market_price = float(market_price)
                except (ValueError, TypeError):
                    market_price = None
                    logger.warning("Invalid market_price for %s: %s", ticker, holding.get("market_price"))

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
                    "VALUES (?, ?, ?, 'AUD', 'commsec_scrape')",
                    (instrument_id, today, market_price),
                )
                stats["prices"] += 1

    logger.info("CommSec scrape import complete: %s", stats)
    return stats
