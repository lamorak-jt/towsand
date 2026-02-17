---
description: Scrape Wise multi-currency balances from the browser and update the database
alwaysApply: false
---

# Scrape Wise

Extract current balances from a logged-in Wise session in the Cursor browser and update the Towsand database.

**Command Format**: `/scrape-wise`

**Prerequisite**: User must be logged into Wise. Account ID: `jacob@lamorak.net`. If no tab is found, the command will navigate to the login page automatically.

---

## Account mapping

The DB account names (from `current-finances/accounts.md`):
- `Wise EUR` (EUR balance)
- `Wise USD` (USD balance)
- `Wise GBP` (GBP balance)

Additional currencies may appear — report them so they can be added to the DB.

## Process

### 1. Verify login state

- Use `browser_tabs` (action: list) to find a tab on `wise.com`.
- If no tab found, navigate to `https://wise.com/login` and wait for user to log in.
- Take a snapshot to confirm the user is logged in (look for account balances, not login form).

### 2. Navigate to home page

- Navigate to `https://wise.com/home` — this page shows all currency balances.
- **Do not use `wise.com/balances`** — it redirects to login.
- The home page displays balances as links with format: "EUR. 3,928.70 EUR. Account details ending in..."
- Take a snapshot to see the page structure.

### 3. Extract balances

**The `browser_snapshot` contains balance data in link text.** Parse directly from snapshot:

1. Look for links with format: `"<CURRENCY>. <amount> <CURRENCY>. Account details ending in..."`
2. Each currency balance appears as a separate link (e.g., "EUR. 3,928.70 EUR.", "USD. 2,562.47 USD.")
3. Extract currency code and balance amount from the link text
4. If snapshot doesn't show values clearly, use `browser_search` with currency codes ("EUR", "USD") to get image descriptions

For each currency balance, extract:
- **Currency code** (EUR, USD, GBP, AUD, etc.)
- **Balance amount** (parse from link text like "3,928.70")

### 4. Update database

```python
from src.db.connection import get_connection
from datetime import date

WISE_CURRENCY_MAP = {
    "EUR": "Wise EUR",
    "USD": "Wise USD",
    "GBP": "Wise GBP",
}

with get_connection() as conn:
    today = date.today().isoformat()
    for currency, balance in extracted_balances:
        account_name = WISE_CURRENCY_MAP.get(currency)
        if account_name is None:
            print(f"NOTE: Found Wise {currency} balance ({balance:,.2f}) — no DB account mapped.")
            print(f"  Add to seed.py and accounts.md if this should be tracked.")
            continue
        acct = conn.execute("SELECT id FROM accounts WHERE name = ?", (account_name,)).fetchone()
        if acct is None:
            print(f"WARNING: Account '{account_name}' not found in DB — skipping")
            continue
        old = conn.execute(
            "SELECT balance FROM cash_balances WHERE account_id = ? AND currency = ? "
            "ORDER BY as_of_date DESC LIMIT 1", (acct["id"], currency)
        ).fetchone()
        old_val = f"{currency} {old['balance']:,.2f}" if old else "none"
        conn.execute(
            "INSERT OR REPLACE INTO cash_balances (account_id, currency, balance, as_of_date) "
            "VALUES (?, ?, ?, ?)",
            (acct["id"], currency, balance, today),
        )
        print(f"  {account_name}: {old_val} → {currency} {balance:,.2f}")
```

### 5. Report results

Print: each balance with old → new value, date, any new currencies found that aren't mapped.

### Safety

- This is READ-ONLY — no transfers, no conversions, no payments.
- Do not click any send/convert/transfer buttons.
- If the page structure is unexpected, STOP and describe what you see.
