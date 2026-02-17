"""Fetch instrument prices and FX rates from yfinance.

Handles:
  - ASX tickers (already .AX suffixed in DB)
  - US tickers (no suffix needed)
  - LSE tickers (DB stores 'UKW', yfinance needs 'UKW.L'; prices returned in pence)
  - FX rates via yfinance currency pairs (e.g. USDAUD=X)
"""

import logging
from datetime import date, timedelta

import pandas as pd
import yfinance as yf

from src.db.connection import get_connection

logger = logging.getLogger(__name__)

# LSE prices are in pence; divide by 100 to get GBP
PENCE_EXCHANGES = {"LSE"}

# Map DB exchange codes to yfinance suffixes for tickers that need one
EXCHANGE_SUFFIX_MAP = {
    "LSE": ".L",
}


def _yf_ticker(db_ticker: str, exchange: str | None) -> str:
    """Convert a DB ticker to a yfinance-compatible ticker."""
    if exchange and exchange.upper() in EXCHANGE_SUFFIX_MAP:
        suffix = EXCHANGE_SUFFIX_MAP[exchange.upper()]
        if not db_ticker.endswith(suffix):
            return f"{db_ticker}{suffix}"
    return db_ticker


def _is_pence(exchange: str | None) -> bool:
    """Check if the exchange quotes in pence (need /100 for GBP)."""
    return exchange is not None and exchange.upper() in PENCE_EXCHANGES


def fetch_prices(db_path=None) -> dict:
    """Fetch latest prices for all held instruments and store in the prices table.

    Returns summary: {"updated": int, "failed": list[str], "unchanged": int}
    """
    with get_connection(db_path) as conn:
        instruments = conn.execute("""
            SELECT DISTINCT i.id, i.ticker, i.exchange, i.currency
            FROM instruments i
            JOIN holdings h ON h.instrument_id = i.id
            ORDER BY i.ticker
        """).fetchall()

    if not instruments:
        logger.info("No held instruments to fetch prices for.")
        return {"updated": 0, "failed": [], "unchanged": 0}

    today = date.today().isoformat()
    stats = {"updated": 0, "failed": [], "unchanged": 0}

    for inst in instruments:
        db_ticker = inst["ticker"]
        yf_ticker = _yf_ticker(db_ticker, inst["exchange"])

        try:
            tk = yf.Ticker(yf_ticker)
            hist = tk.history(period="5d")
            if hist.empty:
                logger.warning("No price data for %s", yf_ticker)
                stats["failed"].append(db_ticker)
                continue

            close = float(hist["Close"].iloc[-1])
            price_date = hist.index[-1].strftime("%Y-%m-%d")

            if _is_pence(inst["exchange"]):
                close = close / 100.0

            with get_connection(db_path) as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO prices (instrument_id, date, close_price, currency, source) "
                    "VALUES (?, ?, ?, ?, 'yfinance')",
                    (inst["id"], price_date, close, inst["currency"]),
                )

            logger.info("%s: %.4f %s (%s)", db_ticker, close, inst["currency"], price_date)
            stats["updated"] += 1

        except Exception as exc:
            logger.warning("Failed to fetch %s: %s", yf_ticker, exc)
            stats["failed"].append(db_ticker)

    return stats


def fetch_price_history(ticker: str, days: int = 365 * 5, db_path=None) -> dict:
    """Backfill historical daily prices for a single instrument.

    Args:
        ticker: DB ticker (e.g. 'BHP.AX', 'UKW')
        days: Number of calendar days to backfill (default 5 years)

    Returns summary: {"ticker": str, "rows": int}
    """
    with get_connection(db_path) as conn:
        inst = conn.execute(
            "SELECT id, ticker, exchange, currency FROM instruments WHERE ticker = ?",
            (ticker,),
        ).fetchone()

    if inst is None:
        raise ValueError(f"Instrument not found: {ticker}")

    yf_ticker = _yf_ticker(inst["ticker"], inst["exchange"])
    start = (date.today() - timedelta(days=days)).isoformat()
    end = date.today().isoformat()

    logger.info("Fetching history for %s (%s) from %s to %s", ticker, yf_ticker, start, end)
    tk = yf.Ticker(yf_ticker)
    hist = tk.history(start=start, end=end)

    if hist.empty:
        logger.warning("No historical data for %s", yf_ticker)
        return {"ticker": ticker, "rows": 0}

    is_pence = _is_pence(inst["exchange"])
    rows = 0

    with get_connection(db_path) as conn:
        for idx, row in hist.iterrows():
            price_date = idx.strftime("%Y-%m-%d")
            close = float(row["Close"])
            if is_pence:
                close = close / 100.0
            conn.execute(
                "INSERT OR REPLACE INTO prices (instrument_id, date, close_price, currency, source) "
                "VALUES (?, ?, ?, ?, 'yfinance')",
                (inst["id"], price_date, close, inst["currency"]),
            )
            rows += 1

    logger.info("Stored %d price rows for %s", rows, ticker)
    return {"ticker": ticker, "rows": rows}


def fetch_fx_rates(db_path=None) -> dict:
    """Fetch latest FX rates for all currencies held in the portfolio.

    Determines which currency pairs are needed from the instruments and cash_balances
    tables, then fetches rates to AUD via yfinance.

    Returns summary: {"updated": int, "failed": list[str]}
    """
    with get_connection(db_path) as conn:
        base_row = conn.execute(
            "SELECT value FROM parameters WHERE key = 'base_currency'"
        ).fetchone()
        base = base_row["value"] if base_row else "AUD"

        currencies = set()
        for r in conn.execute("SELECT DISTINCT currency FROM instruments"):
            currencies.add(r["currency"])
        for r in conn.execute("SELECT DISTINCT currency FROM cash_balances"):
            currencies.add(r["currency"])
        currencies.discard(base)

    if not currencies:
        return {"updated": 0, "failed": []}

    today = date.today().isoformat()
    stats = {"updated": 0, "failed": []}

    for ccy in sorted(currencies):
        # yfinance format: XXXYYY=X (e.g. USDAUD=X means 1 USD in AUD)
        pair = f"{ccy}{base}=X"
        try:
            tk = yf.Ticker(pair)
            hist = tk.history(period="5d")
            if hist.empty:
                logger.warning("No FX data for %s", pair)
                stats["failed"].append(pair)
                continue

            rate = float(hist["Close"].iloc[-1])
            rate_date = hist.index[-1].strftime("%Y-%m-%d")

            with get_connection(db_path) as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO fx_rates (from_currency, to_currency, date, rate, source) "
                    "VALUES (?, ?, ?, ?, 'yfinance')",
                    (ccy, base, rate_date, rate),
                )

            logger.info("%s/%s: %.6f (%s)", ccy, base, rate, rate_date)
            stats["updated"] += 1

        except Exception as exc:
            logger.warning("Failed to fetch %s: %s", pair, exc)
            stats["failed"].append(pair)

    return stats


def fetch_fx_history(from_currency: str, to_currency: str = "AUD",
                     days: int = 365 * 5, db_path=None) -> dict:
    """Backfill historical FX rates for a currency pair.

    Returns summary: {"pair": str, "rows": int}
    """
    pair = f"{from_currency}{to_currency}=X"
    start = (date.today() - timedelta(days=days)).isoformat()
    end = date.today().isoformat()

    logger.info("Fetching FX history for %s from %s to %s", pair, start, end)
    tk = yf.Ticker(pair)
    hist = tk.history(start=start, end=end)

    if hist.empty:
        logger.warning("No FX history for %s", pair)
        return {"pair": pair, "rows": 0}

    rows = 0
    with get_connection(db_path) as conn:
        for idx, row in hist.iterrows():
            rate_date = idx.strftime("%Y-%m-%d")
            rate = float(row["Close"])
            conn.execute(
                "INSERT OR REPLACE INTO fx_rates (from_currency, to_currency, date, rate, source) "
                "VALUES (?, ?, ?, ?, 'yfinance')",
                (from_currency, to_currency, rate_date, rate),
            )
            rows += 1

    logger.info("Stored %d FX rate rows for %s", rows, pair)
    return {"pair": pair, "rows": rows}
