---
description: Scrape RACQ Bank account balances from the browser and update the database
alwaysApply: false
---

# Scrape RACQ

Extract current account balances from a logged-in RACQ Bank session in the Cursor browser and update the Towsand database.

**Command Format**: `/scrape-racq`

**Prerequisite**: User must be logged into RACQ internet banking. If no tab is found, the command will navigate to the login page automatically.

---

## Account mapping

The DB account names to match against (from `current-finances/accounts.md`):
- `Jacob RACQ Bonus Saver` (savings)
- `Jacob RACQ Everyday` (everyday)
- `Darlene RACQ Everyday` (everyday)

## Process

### 1. Verify login state

- Use `browser_tabs` (action: list) to find a tab on `banking.racqbank.com.au` or `banking.racq.com.au`.
- If no tab found, navigate directly to: `https://banking.racqbank.com.au/#/login`
- Take a snapshot to confirm the user is logged in (look for account summary, not a login form).
- If still on login page, wait for user to complete login before proceeding.

### 2. Navigate to accounts summary

- The main dashboard after login (`#/dashboard`) typically shows all accounts with current balances.
- The snapshot will show listitems with text like: "1830751 EVERYDAY ACCOUNT $ 8,872.24"
- If accounts are not visible, look for an "Accounts" or "Overview" navigation link and click it.
- **Do not rely on direct URL navigation** — it may not work after auth.

### 3. Extract balances

**The `browser_snapshot` contains account data in listitem text.** Parse directly from snapshot:

1. Look for listitems under "Transaction Accounts" section
2. Each account appears as: `"<account_number> <ACCOUNT_TYPE> $ <balance>"`
3. Extract: account number, account type, and balance from the listitem text
4. If snapshot doesn't show values clearly, use `browser_search` with "$" to get image descriptions

For each account, extract:
- **Account number** (e.g., 1830751, 1830752) — save to `accounts.md` if not already present
- **Account type** (EVERYDAY ACCOUNT, BONUS SAVER ACCOUNT)
- **Current balance** (available balance)

Match displayed accounts to DB names flexibly:
- "BONUS SAVER ACCOUNT" → `Jacob RACQ Bonus Saver`
- "EVERYDAY ACCOUNT" → if only one found, assume `Jacob RACQ Everyday` (same Bank ID)
- If multiple "Everyday" accounts found, match by account number or owner name if visible
- Note: Darlene's account may not be visible if accessed via different Bank ID/login

### 4. Update database and account numbers

```python
from src.db.connection import get_connection
from datetime import date

with get_connection() as conn:
    today = date.today().isoformat()
    for account_name, balance, account_number in matched_balances:
        acct = conn.execute("SELECT id FROM accounts WHERE name = ?", (account_name,)).fetchone()
        if acct is None:
            print(f"WARNING: Account '{account_name}' not found in DB — skipping")
            continue
        
        # Update account number in accounts.md if provided and not already present
        if account_number:
            # Check if account number needs to be saved (implementation: update accounts.md)
            pass
        
        old = conn.execute(
            "SELECT balance FROM cash_balances WHERE account_id = ? AND currency = 'AUD' "
            "ORDER BY as_of_date DESC LIMIT 1", (acct["id"],)
        ).fetchone()
        old_val = f"AUD {old['balance']:,.2f}" if old else "none"
        conn.execute(
            "INSERT OR REPLACE INTO cash_balances (account_id, currency, balance, as_of_date) "
            "VALUES (?, 'AUD', ?, ?)",
            (acct["id"], balance, today),
        )
        print(f"  {account_name} ({account_number or 'N/A'}): {old_val} → AUD {balance:,.2f}")
```

**Note:** If account numbers are extracted and not already in `accounts.md`, update the file to save them for future reference.

### 5. Report results

Print: each account with account number (if available), old → new balance, date of update, any unmatched accounts, and note if Darlene's account was not found.

### Safety

- This is READ-ONLY — no transfers, no payments, no account modifications.
- Do not click any transfer/pay/settings buttons.
- If the page structure is unexpected, STOP and describe what you see.
