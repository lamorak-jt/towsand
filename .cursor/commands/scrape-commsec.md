---
description: Scrape CommSec portfolio holdings from the browser and import into the database
alwaysApply: false
---

# Scrape CommSec

Extract current holdings from a logged-in CommSec session in the Cursor browser and import them into the Towsand database.

**Command Format**: `/scrape-commsec`

**Prerequisite**: User must be logged into CommSec in a Cursor browser tab.

---

## Process

### 1. Verify login state

- Use `browser_tabs` (action: list) to find a tab on `commsec.com.au`.
- If no tab found, tell the user: "Please open CommSec in the Cursor browser and log in, then run this command again."
- Take a snapshot to confirm the user is logged in (look for portfolio/account elements, not a login form).

### 2. Navigate to Holdings

**Do NOT navigate directly to a URL** — deep links return 404.

Instead:
1. Navigate to the CommSec home page: `https://www2.commsec.com.au/`
2. Take a snapshot to see the page structure.
3. Look for and click a "View Holdings" link, "Portfolio" menu item, or similar navigation element.
4. Wait for the holdings page to load.

### 3. Extract holdings data

**Important: `browser_snapshot` does not reliably show table cell values.** The structure (headers, buttons, links) is visible but data in table cells may be missing.

**Extraction strategy — use `browser_search`:**

1. First, take a snapshot to identify the table structure. The columns are typically:
   `CODE | AVAIL UNITS | PURCHASE $ | LAST $ | MKT VALUE $`

2. Use `browser_search` with the "$" character or known ticker codes to locate data rows. The search results include screenshot image descriptions that contain the actual cell values.

3. For each holding, extract:
   - **Code/Ticker** (ASX code, e.g. "GSBG27", "CBA")
   - **Available Units** (quantity held)
   - **Purchase $** (cost basis per unit)
   - **Last $** (current market price)
   - **Market Value $** (current total value)

4. Company/fund names may NOT be visible on the holdings page — just the ticker code. That's fine; names can be looked up later.

5. If `browser_search` doesn't capture all rows, try searching for specific text patterns: individual ticker codes, or scrolling down and re-searching.

### 4. Import into database

Use the scraper module to import extracted data:

```python
from src.market_data.commsec_scraper import import_scraped_holdings

holdings = [
    {
        "ticker": "GSBG27",
        "quantity": 1742,
        "purchase_price": 103.726,
        "market_price": 102.250,
    },
    # ... more holdings
]

results = import_scraped_holdings(holdings)
```

The module handles:
- Adding `.AX` suffix to tickers
- Upserting instruments (creating if new)
- Upserting holdings with cost basis (purchase_price × quantity)
- Storing current market prices
- All within a single database transaction

### 5. Report results

Print a summary table:

```
Ticker        Qty    Purchase $    Last $    Mkt Value $
GSBG27.AX   1,742      103.73    102.25     178,119.50
GSBG33.AX     349      103.51    101.57      35,447.93
```

Then: total number of holdings imported, total market value, any new instruments created.

### Known issues

- **Deep links don't work**: CommSec requires navigation from the home page.
- **Table data not in DOM snapshots**: Must use `browser_search` or `browser_take_screenshot` to read values.
- **No company names**: Only ticker codes are shown on the holdings page. Names can be filled in later via yfinance or manual entry.
- **Ticker format**: CommSec shows codes like "GSBG 27" (with space) or "GSBG27". Clean up spaces before importing.

### Safety

- This is READ-ONLY from CommSec — no trading, no account modifications.
- Do not click any trade/order buttons.
- Do not navigate away from Portfolio/Holdings pages.
- If the page structure is unexpected, STOP and describe what you see.
