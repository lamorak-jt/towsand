"""Seed the Towsand database with institutions, accounts, cash balances, and parameters.

Data source: current-finances/institutions.md
"""

from src.db.connection import get_connection

# (name, institution_type, base_currency, notes)
INSTITUTIONS = [
    ("Interactive Brokers", "broker", "AUD", None),
    ("CommSec", "broker", "AUD", None),
    ("RACQ", "bank", "AUD", None),
    ("ANZ", "bank", "AUD", None),
    ("Wise", "fintech", "AUD", "Multi-currency"),
    ("N26", "bank", "EUR", None),
    ("Bondora", "fintech", "EUR", "Isepankur/Bondora P2P — below the line"),
    ("Physical Cash", "other", "AUD", "Notes and coins held"),
    ("Eroza", "other", "AUD", "Receivable — treatment TBD (see open items)"),
]

# (institution_name, account_name, account_type, currency, notes)
ACCOUNTS = [
    ("Interactive Brokers", "IB Trading AUD", "trading", "AUD", None),
    ("CommSec", "CommSec Trading", "trading", "AUD", None),
    ("RACQ", "Jacob RACQ Bonus Saver", "savings", "AUD", None),
    ("RACQ", "Jacob RACQ Everyday", "everyday", "AUD", None),
    ("RACQ", "Darlene RACQ Everyday", "everyday", "AUD", None),
    ("ANZ", "Jacob ANZ Savings", "savings", "AUD", None),
    ("ANZ", "Jacob ANZ Credit Card", "credit", "AUD", "Liability — treatment TBD"),
    ("Wise", "Wise EUR", "other", "EUR", None),
    ("Wise", "Wise USD", "other", "USD", "Below the line"),
    ("Wise", "Wise GBP", "other", "GBP", None),
    ("N26", "N26 Darlene", "everyday", "EUR", None),
    ("N26", "N26 Jacob", "everyday", "EUR", "Below the line"),
    ("Bondora", "Isepankur - Bondora", "other", "EUR", "Below the line"),
    ("Physical Cash", "Cash USD", "other", "USD", "Below the line"),
    ("Physical Cash", "Cash AUD", "other", "AUD", "Below the line"),
    ("Eroza", "Eroza Owed", "other", "AUD", "Receivable $60,000 — treatment TBD"),
]

# (account_name, currency, balance)
# Trading accounts (IB, CommSec) hold securities — cash component unknown until holdings imported
CASH_BALANCES = [
    ("Jacob RACQ Bonus Saver", "AUD", 80_001.19),
    ("Jacob RACQ Everyday", "AUD", 31_776.64),
    ("Darlene RACQ Everyday", "AUD", 6_122.03),
    ("Jacob ANZ Savings", "AUD", 3_032.39),
    ("Jacob ANZ Credit Card", "AUD", -692.50),
    ("Wise EUR", "EUR", 6_035.85),
    ("Wise USD", "USD", 2_552.15),
    ("N26 Darlene", "EUR", 3_108.00),
    ("N26 Jacob", "EUR", 1_535.68),
    ("Isepankur - Bondora", "EUR", 2_041.00),
    ("Cash USD", "USD", 1_500.00),
    ("Cash AUD", "AUD", 200.00),
    ("Eroza Owed", "AUD", 60_000.00),
]

PARAMETERS = [
    ("monthly_expenses", "9000", "Core family living expenses per month (AUD)"),
    ("income_amount", "11000", "Net employment income per month (AUD)"),
    ("income_visibility_months", "12", "Forward income visibility in months — USER TO CONFIRM"),
    ("stabiliser_months", "24", "Months of expenses the stabiliser must cover (Rule 2.1)"),
    ("stabiliser_band_low", "0.15", "Stabiliser minimum as fraction of portfolio (Rule 1.1)"),
    ("stabiliser_band_high", "0.25", "Stabiliser maximum as fraction of portfolio (Rule 1.1)"),
    ("compounder_band_low", "0.50", "Compounder minimum as fraction of portfolio (Rule 1.1)"),
    ("compounder_band_high", "0.65", "Compounder maximum as fraction of portfolio (Rule 1.1)"),
    ("optionality_band_low", "0.10", "Optionality minimum as fraction of portfolio (Rule 1.1)"),
    ("optionality_band_high", "0.20", "Optionality maximum as fraction of portfolio (Rule 1.1)"),
    ("max_single_equity_pct", "0.10", "Max single listed equity position (Rule 3.1)"),
    ("max_single_credit_pct", "0.07", "Max single credit instrument position (Rule 3.1)"),
    ("max_speculative_single_pct", "0.01", "Max single speculative position (Rule 3.1)"),
    ("max_speculative_aggregate_pct", "0.03", "Max aggregate speculative positions (Rule 3.1)"),
    ("max_issuer_concentration_pct", "0.20", "Max exposure to single corporate group (Rule 3.2)"),
    ("max_aud_risk_assets_pct", "0.55", "Max AUD-domiciled risk assets excl govt bonds (Rule 4.1)"),
    ("max_single_macro_driver_pct", "0.30", "Max exposure to single macro driver (Rule 4.2)"),
    ("aud_currency_band_low", "0.50", "AUD exposure minimum of growth capital (Rule 5.1)"),
    ("aud_currency_band_high", "0.70", "AUD exposure maximum of growth capital (Rule 5.1)"),
    ("min_unhedged_international_pct", "0.40", "Min unhedged fraction of international growth (Rule 5.2)"),
    ("min_stabiliser_liquid_pct", "0.70", "Min liquid fraction of stabiliser capital (Rule 7.1)"),
    ("max_stabiliser_single_duration_pct", "0.40", "Max single duration point in stabiliser (Rule 7.2)"),
    ("min_stabiliser_inflation_linked_pct", "0.25", "Min inflation-linked fraction of stabiliser (Rule 7.3)"),
    ("drawdown_tolerance_pct", "0.35", "Equity drawdown scenario for stress test (Rule 8.1)"),
    ("stress_correlation_threshold", "0.70", "Correlation above which assets = one risk (Rule 8.2)"),
    ("income_shock_threshold_pct", "0.30", "Income drop that triggers shock rule (Rule 2.2)"),
    ("income_shock_active", "0", "1 if income shock trigger is currently active"),
    ("base_currency", "AUD", "Portfolio base currency for all valuations"),
]


def seed_institutions_and_accounts(db_path=None):
    """Insert institutions and accounts. Idempotent (INSERT OR IGNORE)."""
    with get_connection(db_path) as conn:
        for name, itype, currency, notes in INSTITUTIONS:
            conn.execute(
                "INSERT OR IGNORE INTO institutions (name, institution_type, base_currency, notes) "
                "VALUES (?, ?, ?, ?)",
                (name, itype, currency, notes),
            )

        for inst_name, acct_name, acct_type, currency, notes in ACCOUNTS:
            row = conn.execute(
                "SELECT id FROM institutions WHERE name = ?", (inst_name,)
            ).fetchone()
            if row is None:
                raise ValueError(f"Institution not found: {inst_name}")
            conn.execute(
                "INSERT OR IGNORE INTO accounts (institution_id, name, account_type, currency, notes) "
                "VALUES (?, ?, ?, ?, ?)",
                (row["id"], acct_name, acct_type, currency, notes),
            )


def seed_cash_balances(db_path=None):
    """Insert initial cash balances. Idempotent per (account, currency, date)."""
    with get_connection(db_path) as conn:
        for acct_name, currency, balance in CASH_BALANCES:
            row = conn.execute(
                "SELECT id FROM accounts WHERE name = ?", (acct_name,)
            ).fetchone()
            if row is None:
                raise ValueError(f"Account not found: {acct_name}")
            conn.execute(
                "INSERT OR IGNORE INTO cash_balances (account_id, currency, balance) "
                "VALUES (?, ?, ?)",
                (row["id"], currency, balance),
            )


def seed_parameters(db_path=None):
    """Insert default parameters. Existing values are NOT overwritten."""
    with get_connection(db_path) as conn:
        for key, value, description in PARAMETERS:
            conn.execute(
                "INSERT OR IGNORE INTO parameters (key, value, description) VALUES (?, ?, ?)",
                (key, value, description),
            )
