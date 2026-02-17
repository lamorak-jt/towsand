"""Initialise the Towsand SQLite schema.

Run directly: python -m src.db.init_schema
Or via CLI:   towsand init
"""

from src.db.connection import get_connection

SCHEMA_VERSION = 1

TABLES = [
    # --- Reference data ---
    """
    CREATE TABLE IF NOT EXISTS institutions (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        name            TEXT    NOT NULL UNIQUE,
        institution_type TEXT   NOT NULL CHECK(institution_type IN ('broker','bank','fintech','other')),
        base_currency   TEXT    NOT NULL DEFAULT 'AUD',
        notes           TEXT,
        created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS accounts (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        institution_id  INTEGER NOT NULL REFERENCES institutions(id),
        name            TEXT    NOT NULL,
        account_type    TEXT    NOT NULL CHECK(account_type IN ('trading','savings','everyday','credit','other')),
        currency        TEXT    NOT NULL DEFAULT 'AUD',
        notes           TEXT,
        created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
        UNIQUE(institution_id, name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS instruments (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker          TEXT    NOT NULL UNIQUE,
        name            TEXT,
        instrument_type TEXT    NOT NULL CHECK(instrument_type IN (
            'equity','etf','govt_bond_nominal','govt_bond_indexed',
            'credit','listed_fund','cash','other'
        )),
        exchange        TEXT,
        currency        TEXT    NOT NULL,
        country_domicile TEXT,
        is_speculative  INTEGER NOT NULL DEFAULT 0,
        notes           TEXT,
        created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
    )
    """,

    # --- Portfolio data ---
    """
    CREATE TABLE IF NOT EXISTS holdings (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id      INTEGER NOT NULL REFERENCES accounts(id),
        instrument_id   INTEGER NOT NULL REFERENCES instruments(id),
        quantity        REAL    NOT NULL,
        cost_basis      REAL,
        cost_basis_currency TEXT,
        date_acquired   TEXT,
        notes           TEXT,
        updated_at      TEXT    NOT NULL DEFAULT (datetime('now')),
        UNIQUE(account_id, instrument_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS cash_balances (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id      INTEGER NOT NULL REFERENCES accounts(id),
        currency        TEXT    NOT NULL,
        balance         REAL    NOT NULL,
        as_of_date      TEXT    NOT NULL DEFAULT (date('now')),
        notes           TEXT,
        UNIQUE(account_id, currency, as_of_date)
    )
    """,

    # --- Market data ---
    """
    CREATE TABLE IF NOT EXISTS prices (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        instrument_id   INTEGER NOT NULL REFERENCES instruments(id),
        date            TEXT    NOT NULL,
        close_price     REAL    NOT NULL,
        currency        TEXT    NOT NULL,
        source          TEXT,
        UNIQUE(instrument_id, date)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS fx_rates (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        from_currency   TEXT    NOT NULL,
        to_currency     TEXT    NOT NULL,
        date            TEXT    NOT NULL,
        rate            REAL    NOT NULL,
        source          TEXT,
        UNIQUE(from_currency, to_currency, date)
    )
    """,

    # --- Classification & tagging ---
    """
    CREATE TABLE IF NOT EXISTS instrument_classifications (
        id                      INTEGER PRIMARY KEY AUTOINCREMENT,
        instrument_id           INTEGER NOT NULL UNIQUE REFERENCES instruments(id),
        capital_role            TEXT    CHECK(capital_role IN ('stabiliser','compounder','optionality')),
        macro_drivers           TEXT    DEFAULT '[]',
        corporate_group         TEXT,
        stress_correlation_group TEXT,
        liquidity_days          INTEGER,
        duration_years          REAL,
        is_inflation_linked     INTEGER NOT NULL DEFAULT 0,
        hedged                  INTEGER,
        convexity_defined_downside    INTEGER,
        convexity_nonlinear_upside    INTEGER,
        convexity_stress_outperform   INTEGER,
        yield_dominant          INTEGER NOT NULL DEFAULT 0,
        notes                   TEXT,
        updated_at              TEXT    NOT NULL DEFAULT (datetime('now'))
    )
    """,

    # --- System parameters ---
    """
    CREATE TABLE IF NOT EXISTS parameters (
        key             TEXT    PRIMARY KEY,
        value           TEXT    NOT NULL,
        description     TEXT,
        updated_at      TEXT    NOT NULL DEFAULT (datetime('now'))
    )
    """,

    # --- Snapshots & compliance ---
    """
    CREATE TABLE IF NOT EXISTS portfolio_snapshots (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        date            TEXT    NOT NULL,
        total_value_aud REAL    NOT NULL,
        snapshot_data   TEXT    NOT NULL,
        created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS compliance_snapshots (
        id                      INTEGER PRIMARY KEY AUTOINCREMENT,
        portfolio_snapshot_id   INTEGER REFERENCES portfolio_snapshots(id),
        date                    TEXT    NOT NULL,
        rule_id                 TEXT    NOT NULL,
        status                  TEXT    NOT NULL CHECK(status IN ('pass','warning','breach')),
        detail                  TEXT,
        created_at              TEXT    NOT NULL DEFAULT (datetime('now'))
    )
    """,

    # --- Decision log ---
    """
    CREATE TABLE IF NOT EXISTS decisions (
        id                      INTEGER PRIMARY KEY AUTOINCREMENT,
        date                    TEXT    NOT NULL DEFAULT (date('now')),
        decision_type           TEXT    NOT NULL CHECK(decision_type IN (
            'rebalance','classification_change','parameter_change',
            'trade','rule_override','review'
        )),
        trigger                 TEXT    NOT NULL CHECK(trigger IN (
            'rule_breach','income_shock','inflation_shift',
            'currency_regime','correlation_convergence','discretionary'
        )),
        summary                 TEXT    NOT NULL,
        rationale               TEXT    NOT NULL,
        linked_rule_ids         TEXT    DEFAULT '[]',
        linked_action_ids       TEXT    DEFAULT '[]',
        compliance_snapshot_id  INTEGER REFERENCES compliance_snapshots(id),
        outcome_notes           TEXT,
        recorded_by             TEXT,
        created_at              TEXT    NOT NULL DEFAULT (datetime('now'))
    )
    """,

    # --- Action queue (for recommendations) ---
    """
    CREATE TABLE IF NOT EXISTS actions (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        date_proposed   TEXT    NOT NULL DEFAULT (date('now')),
        action_type     TEXT    NOT NULL CHECK(action_type IN ('buy','sell','rebalance','classify','other')),
        description     TEXT    NOT NULL,
        instrument_id   INTEGER REFERENCES instruments(id),
        quantity        REAL,
        rationale       TEXT,
        status          TEXT    NOT NULL DEFAULT 'proposed' CHECK(status IN ('proposed','approved','executed','skipped')),
        decision_id     INTEGER REFERENCES decisions(id),
        resolved_at     TEXT,
        created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
    )
    """,
]

INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_holdings_account ON holdings(account_id)",
    "CREATE INDEX IF NOT EXISTS idx_holdings_instrument ON holdings(instrument_id)",
    "CREATE INDEX IF NOT EXISTS idx_prices_instrument_date ON prices(instrument_id, date)",
    "CREATE INDEX IF NOT EXISTS idx_fx_rates_pair_date ON fx_rates(from_currency, to_currency, date)",
    "CREATE INDEX IF NOT EXISTS idx_compliance_date ON compliance_snapshots(date)",
    "CREATE INDEX IF NOT EXISTS idx_decisions_date ON decisions(date)",
    "CREATE INDEX IF NOT EXISTS idx_actions_status ON actions(status)",
]


def init_db(db_path=None):
    """Create all tables and indexes. Safe to run repeatedly (IF NOT EXISTS)."""
    with get_connection(db_path) as conn:
        for ddl in TABLES:
            conn.execute(ddl)
        for idx in INDEXES:
            conn.execute(idx)
        conn.execute(
            "INSERT OR IGNORE INTO parameters (key, value, description) VALUES (?, ?, ?)",
            ("schema_version", str(SCHEMA_VERSION), "Current database schema version"),
        )
    return True


if __name__ == "__main__":
    init_db()
    print("Database initialised at default path.")
