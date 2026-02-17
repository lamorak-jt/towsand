"""Wrapper around ib_async.FlexReport for fetching and parsing IB Flex statements.

Supports two modes:
  1. Download from IB using token + queryId
  2. Load from a previously saved XML file

Usage:
    report = fetch_flex_report(token="...", query_id="...")
    # or
    report = load_flex_report("/path/to/saved_report.xml")

    positions = report.open_positions()
    cash = report.cash_report()
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
from ib_async import FlexReport

logger = logging.getLogger(__name__)


class FlexReportError(Exception):
    """Raised when a Flex report cannot be fetched or parsed."""


@dataclass
class ParsedFlexReport:
    """Parsed Flex report with convenient accessors for portfolio-relevant topics."""

    _report: FlexReport = field(repr=False)

    @property
    def available_topics(self) -> set[str]:
        return self._report.topics()

    def open_positions(self) -> pd.DataFrame:
        """Extract open positions as a DataFrame.

        Key columns: symbol, description, currency, assetCategory, quantity,
        markPrice, positionValue, costBasisMoney, costBasisPrice, openDateTime,
        isin, conid, fxRateToBase.
        """
        df = self._report.df("OpenPosition")
        if df.empty:
            logger.warning("No OpenPosition data found in report.")
            return df
        return df

    def cash_report(self) -> pd.DataFrame:
        """Extract cash balances by currency.

        IB uses 'CashReportCurrency' or 'CashReport' depending on report version.
        """
        for topic in ("CashReportCurrency", "CashReport"):
            if topic in self.available_topics:
                df = self._report.df(topic)
                if not df.empty:
                    return df
        logger.warning("No cash report data found in report.")
        return pd.DataFrame()

    def trades(self) -> pd.DataFrame:
        """Extract executed trades."""
        df = self._report.df("Trade")
        if df.empty:
            logger.warning("No Trade data found in report.")
        return df

    def dividends(self) -> pd.DataFrame:
        """Extract dividend accruals / payments."""
        for topic in ("ChangeInDividendAccrual", "OpenDividendAccrual"):
            if topic in self.available_topics:
                return self._report.df(topic)
        logger.warning("No dividend data found in report.")
        return pd.DataFrame()

    def fx_rates_from_positions(self) -> pd.DataFrame:
        """Extract FX rates from the fxRateToBase attribute on open positions.

        IB Flex reports include fxRateToBase on each position row when
        "Include Currency Rates?" is set to Yes in the query config.
        Returns a DataFrame with columns: currency, fxRateToBase, reportDate.
        """
        df = self.open_positions()
        if df.empty or "fxRateToBase" not in df.columns:
            logger.warning("No fxRateToBase data found on positions.")
            return pd.DataFrame()
        rate_cols = ["currency", "fxRateToBase"]
        if "reportDate" in df.columns:
            rate_cols.append("reportDate")
        rates = df[rate_cols].drop_duplicates(subset=["currency"])
        return rates

    def nav_summary(self) -> pd.DataFrame:
        """Extract Net Asset Value summary."""
        df = self._report.df("EquitySummaryByReportDateInBase")
        if df.empty:
            logger.warning("No NAV summary data found in report.")
        return df

    def raw_df(self, topic: str) -> pd.DataFrame:
        """Extract any topic as a DataFrame for exploration."""
        return self._report.df(topic)

    def save(self, path: str | Path) -> None:
        """Save the raw XML report to file for offline use."""
        self._report.save(str(path))
        logger.info("Report saved to %s", path)


def fetch_flex_report(token: str, query_id: str) -> ParsedFlexReport:
    """Download a Flex report from IB's web service.

    Requires:
      - A Flex Web Service token (Settings → Configure Flex Web Service → Generate Token)
      - A Flex Query ID (Settings → Flex Queries → create a query including Open Positions,
        Cash Report, Trades, and optionally Dividends and Conversion Rates)
    """
    logger.info("Downloading Flex report (query_id=%s)...", query_id)
    try:
        report = FlexReport(token=token, queryId=query_id)
    except Exception as exc:
        raise FlexReportError(f"Failed to download Flex report: {exc}") from exc
    logger.info("Report downloaded. Available topics: %s", report.topics())
    return ParsedFlexReport(_report=report)


def load_flex_report(path: str | Path) -> ParsedFlexReport:
    """Load a previously saved Flex report from an XML file."""
    path = Path(path)
    if not path.exists():
        raise FlexReportError(f"Report file not found: {path}")
    logger.info("Loading Flex report from %s", path)
    report = FlexReport(path=str(path))
    logger.info("Report loaded. Available topics: %s", report.topics())
    return ParsedFlexReport(_report=report)
