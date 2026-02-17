# Towsand Project Task List

**Objective:** Build a local Python + SQLite system that tracks the Townsend family portfolio, enforces portfolio management rules, and recommends buy/sell actions to maximise risk-adjusted returns.

**Core living expenses:** $9,000/month → Stabiliser floor = max($216,000, 15–25% of portfolio).

**Instrument universe:** Publicly traded instruments available to non-sophisticated investors (equities, ETFs, government bonds nominal & indexed, credit instruments, listed funds). No options, warrants, or private assets.

**Interfaces:** CLI scripts, lightweight web UI, Cursor `/` commands for AI agent workflows. Manual invocation.

---

## Phase 1 — Project Foundation & Data Schema

### 1.1 Python project setup
- [x] Create `pyproject.toml` with dependencies (sqlite3 stdlib, click for CLI, yfinance or similar for market data, pandas, flask/fastapi for lightweight UI)
- [x] Create virtual environment and `requirements.txt` lock file
- [x] Establish directory structure: `src/`, `src/db/`, `src/market_data/`, `src/compliance/`, `src/recommendations/`, `src/cli/`, `src/ui/`, `tests/`
- [ ] Add `.cursor/commands/` stubs for AI agent workflows *(go-now.md created; remaining commands deferred to Phase 7.3)*

### 1.2 SQLite schema design
- [x] `institutions` — name, type (broker/bank/fintech/other), base_currency
- [x] `accounts` — institution_id, name, account_type (trading/savings/everyday/credit/other), currency
- [x] `holdings` — account_id, instrument_id, quantity, cost_basis, cost_basis_currency, date_acquired
- [x] `instruments` — ticker, name, instrument_type (equity/etf/govt_bond_nominal/govt_bond_indexed/credit/listed_fund/cash/other), exchange, currency, country_domicile, is_speculative
- [x] `prices` — instrument_id, date, close_price, currency, source
- [x] `fx_rates` — from_currency, to_currency, date, rate, source
- [x] `cash_balances` — account_id, currency, balance, as_of_date
- [x] `instrument_classifications` — instrument_id, capital_role, macro_drivers, corporate_group, stress_correlation_group, liquidity_days, duration_years, is_inflation_linked, hedged, convexity fields, yield_dominant
- [x] `parameters` — key/value store for config (29 parameters seeded, covering all rules)
- [x] `compliance_snapshots` — date, rule_id, status (pass/breach/warning), detail, portfolio_snapshot_id
- [x] `portfolio_snapshots` — id, date, total_value_aud, snapshot_data
- [x] `decisions` — id, date, decision_type, trigger, summary, rationale, linked_rule_ids, linked_action_ids, compliance_snapshot_id, outcome_notes, recorded_by
- [x] `actions` — id, action_type, description, instrument_id, quantity, rationale, status, decision_id *(added: action queue table)*
- [x] Write migration/init script: `src/db/init_schema.py`

### 1.3 Seed current data
- [x] Import institutions and accounts from `current-finances/institutions.md` *(9 institutions, 15 accounts)*
- [ ] Import IB holdings via Flex report → **`towsand ib import-flex --token <T> --query-id <Q>`** or **`towsand ib import-file <xml>`** *(importer built — awaiting user's Flex token + query ID)*
- [ ] Import CommSec holdings via CSV → **`towsand commsec import <csv>`** *(importer built — awaiting user's CSV export)*
- [x] Import cash balances for non-trading accounts *(13 balances seeded)*
- [x] Set initial parameters: monthly_expenses=9000, income_amount=11000, income_visibility_months=12 (USER TO CONFIRM)

---

## Phase 2 — Market Data Pipeline

### 2.0 Broker data import *(added)*
- [x] Add `ib_async` dependency for IB API + Flex Web Service access
- [x] Build Flex report fetcher/parser (`src/market_data/flex_report.py`) — download or load XML, extract positions/cash/FX/trades/dividends
- [x] Build IB importer (`src/market_data/ib_importer.py`) — maps Flex Open Positions to instruments + holdings + prices; imports cash balances and FX rates
- [x] Build CommSec CSV importer (`src/market_data/commsec_importer.py`) — flexible column matching for CommSec portfolio exports
- [x] CLI: `towsand ib import-flex --token T --query-id Q [--save-xml path]` — download and import live
- [x] CLI: `towsand ib import-file <xml>` — import from saved XML
- [x] CLI: `towsand ib topics <xml>` / `towsand ib preview <xml> <topic>` — explore report contents
- [x] CLI: `towsand commsec import <csv>` — import CommSec CSV
- [x] User action: configure IB Flex Query (Open Positions, Cash Report, Financial Instrument Info, Trades, Open Dividend Accruals + Include Currency Rates) and generate token
- [x] User action: first IB Flex import complete *(11 holdings, 3 cash balances, 39 FX rates)*
- [ ] User action: export CommSec CSV and run import, OR use `/scrape-commsec`

### 2.0a Browser-based data capture *(added)*
- [x] Create `current-finances/accounts.md` — structured account reference with IDs, URLs, DB names
- [x] `/scrape-commsec` — AI agent extracts CommSec holdings from logged-in browser session → imports to DB
- [x] `/scrape-racq` — AI agent extracts RACQ balances from logged-in browser session → updates cash_balances
- [x] `/scrape-wise` — AI agent extracts Wise multi-currency balances from logged-in browser session → updates cash_balances
- [x] CLI: `towsand cash update <account> <balance>` — manual balance update with fuzzy account matching
- [x] CLI: `towsand cash list` — show all cash balances
- [ ] User action: fill in account numbers/IDs in `current-finances/accounts.md`

### 2.1 Price fetching ✓
- [x] Build price fetcher using yfinance — `src/market_data/price_fetcher.py`
- [x] Support ASX tickers (`.AX`), US tickers, LSE tickers (`.L` suffix, pence→GBP conversion)
- [x] Fetch and store daily close prices in `prices` table
- [x] Command: `towsand prices update` — fetch latest prices for all held instruments (13/13 OK)
- [x] Command: `towsand prices history <ticker> [--days N]` — backfill historical data
- [x] Command: `towsand prices history-all [--days N]` — backfill all held instruments
- [x] Command: `towsand prices list` — show latest price per held instrument with value

### 2.2 FX rate fetching ✓
- [x] Fetch USD/AUD, EUR/AUD, GBP/AUD rates from yfinance (XXXAUD=X pairs)
- [x] Store in `fx_rates` table with ISO dates
- [x] Command: `towsand fx update` — fetch latest FX rates for portfolio currencies
- [x] Command: `towsand fx history <from_currency> [--to AUD] [--days N]` — backfill FX
- [x] Command: `towsand fx history-all [--days N]` — backfill all currency pairs
- [x] Command: `towsand fx list` — show latest FX rates
- [x] Fixed IB importer date format normalization (compact→ISO)

### 2.3 Historical data for analytics ✓
- [x] Backfill 5 years of daily prices for all 13 held instruments (15,883 rows)
- [x] Backfill 5 years of FX rates for USD, EUR, GBP → AUD (3,894 rows)
- [ ] Store Australian CPI / inflation data (for real return calculation) — source: ABS or RBA

---

## Phase 3 — Portfolio Valuation & Classification

### 3.1 Portfolio valuation engine ✓
- [x] Calculate current market value per holding (quantity × latest price × FX to AUD) — `src/portfolio/valuation.py`
- [x] Aggregate by account, institution, instrument type, currency, country
- [x] Command: `towsand portfolio value` — full portfolio with AUD conversion, prices, FX rates
- [x] Command: `towsand portfolio summary` — allocation breakdown by role, type, currency, country, institution

### 3.2 Capital role classification ✓
- [x] CLI workflow: `towsand classify role <ticker> <stabiliser|compounder|optionality>`
- [x] Command: `towsand classify list` — show all held instruments with classification status
- [x] Unclassified instruments shown as `---` (compliance engine will flag these)
- [ ] **User action**: classify all 13 held instruments using `towsand classify role`

### 3.3 Macro driver & exposure tagging ✓
- [x] `towsand classify tag <ticker> --macro <drivers> --group <corp_group> --corr-group <group> --duration <yrs> --liquidity <days> --hedged/--unhedged --inflation-linked/--no-inflation-linked`
- [x] Command: `towsand portfolio exposures` — show macro driver & corporate group exposure
- [ ] **User action**: tag all 13 instruments with macro drivers and corporate groups

---

## Phase 4 — Compliance Engine ✓

All rules from `portfolio-management-rules.md` implemented as discrete checks in `src/compliance/checks.py`. Each returns pass / warning / breach + detail.

### 4.1 Capital role allocation (Rules 1.1, 2.1) ✓
- [x] Rule 2.1 (absolute, primary): stabiliser ≥ 24 × monthly_expenses
- [x] Rule 1.1 (percentage, conditional): if 2.1 met, stabiliser 15–25% of investable assets; if 24-month floor binds above 25%, this is "floor binding" not a breach
- [x] Compounder band: 50–65% of investable assets
- [x] Optionality band: 10–20% of investable assets
- [x] Unclassified holdings flagged as warning

### 4.2 Income dependency (Rule 2.2) ✓
- [x] Check income_shock_active parameter; if triggered: optionality ≤10%

### 4.3 Position size (Rules 3.1, 3.2) ✓
- [x] Single listed equity/ETF ≤ 10%, credit ≤ 7%, speculative ≤ 1%/3% aggregate
- [x] Issuer concentration ≤ 20% per corporate group

### 4.4 Macro factor exposure (Rules 4.1, 4.2) ✓
- [x] AUD-**domiciled** risk assets ≤ 55% of investable assets (uses `country_domicile`, excl AUD govt bonds)
- [x] Single macro driver ≤ 30% of investable assets

### 4.5 Currency exposure (Rules 5.1, 5.2) ✓
- [x] AUD 50–70% of **growth capital** (compounder + optionality holdings only)
- [x] ≥40% of **international** growth assets must be unhedged (denominator = non-AUD growth holdings)

### 4.6 Optionality constraints (Rules 6.1, 6.2) ✓
- [x] 2-of-3 convexity payoff shape test; yield-dominant ≤ 25%

### 4.7 Stabiliser constraints (Rules 7.1, 7.2, 7.3) ✓
- [x] ≥70% liquid in 5 days, duration no single point >40%, ≥25% inflation-linked

### 4.8 Drawdown & correlation (Rules 8.1, 8.2) ✓
- [x] 35% equity drawdown modelling, stress correlation group checks

### 4.9 Review trigger detection (Rule 9) ✓
- [x] Parameter-driven triggers; no-action-needed default

### 4.10 Compliance dashboard command ✓
- [x] `towsand compliance` — summary (warnings/breaches only)
- [x] `towsand compliance --detail` — full detail per rule with coloured output
- [x] Each run stored as portfolio_snapshot + compliance_snapshot

---

## Phase 5 — Analytics & Risk

### 5.1 Return calculation
- [ ] Holding-level return (total return incl. dividends if tracked, else price return)
- [ ] Portfolio-level weighted return
- [ ] Real return (adjust for CPI)
- [ ] Command: `towsand returns [--period 1y|3y|5y|ytd]`

### 5.2 Correlation analysis
- [ ] Calculate rolling pairwise correlation matrix (e.g. 60-day, 252-day)
- [ ] Identify stress-period correlations (periods where equity index drawdown >15%)
- [ ] Flag pairs with stress correlation >0.7
- [ ] Command: `towsand correlations [--stress-only]`

### 5.3 Drawdown simulation
- [ ] Scenario: apply −35% to equity holdings, model stabiliser drawdown, check if long-term assets need liquidation
- [ ] Scenario: AUD ±20% move
- [ ] Scenario: credit spread widening (proxy via relevant ETF/bond price moves)
- [ ] Command: `towsand stress [--scenario equity_crash|aud_shock|credit_widen]`

### 5.4 Concentration & exposure reports
- [ ] Top 10 holdings by weight
- [ ] Exposure by: country, currency, sector, macro driver, corporate group
- [ ] Command: `towsand exposures --by [country|currency|sector|macro|group]`

---

## Phase 6 — Recommendation Engine

This is the primary value layer. Given the current portfolio state, compliance status, and strategy targets, recommend specific actions.

**Critical constraint — Rule 9.2 gating:** The recommendation engine must only produce actions when (a) a compliance breach exists, (b) a review trigger is active (income shock, inflation shift, currency regime change, correlation convergence), or (c) a breach has persisted >30 days. Absent a trigger, no discretionary rebalancing. "Optimise" recommendations are not permitted outside these gates.

### 6.1 Gap analysis
- [ ] Compare current allocation (by role, currency, macro) to target bands from rules
- [ ] Quantify the dollar gap for each dimension (e.g. "Stabiliser is $42,000 below the 24-month floor")
- [ ] Identify which gaps are breaches vs. warnings vs. within tolerance
- [ ] Denominator = investable assets (see `portfolio-management-rules.md §0`)
- [ ] Command: `towsand gaps`

### 6.2 Rebalancing recommendations
- [ ] Given gaps, recommend specific sells (overweight positions) and buys (underweight roles)
- [ ] **Gate behind Rule 9.2**: only recommend when breach exists or trigger is active
- [ ] Respect all position-size and concentration constraints in recommendations
- [ ] Prioritise: fix breaches first, then trigger-driven concerns
- [ ] Factor in tax implications flag (note: not model tax, but flag "this is a taxable event")
- [ ] Command: `towsand rebalance` — show recommended trades with rationale

### 6.3 Instrument screening
- [ ] For underweight roles, screen candidate instruments from a watchlist or universe
- [ ] Filter by: role eligibility, currency exposure needs, macro diversification value
- [ ] Rank candidates by contribution to portfolio improvement (reduces a gap, improves diversification)
- [ ] Command: `towsand screen <role> [--currency AUD|USD|EUR] [--macro-gap <driver>]`

### 6.4 Optionality evaluation
- [ ] For Optionality bucket: score candidates on 2-of-3 convexity test
- [ ] Estimate payoff asymmetry (historical max drawdown vs. max gain in stress)
- [ ] Command: `towsand optionality score <ticker>`

### 6.5 Action queue
- [ ] Persist recommended actions with status (proposed/approved/executed/skipped)
- [ ] Command: `towsand actions` — list pending recommendations
- [ ] Command: `towsand actions approve <id>` / `towsand actions skip <id>`
- [ ] After execution, user records the trade → updates holdings

### 6.6 Decision logging
- [ ] Every material action (trade, rebalance, classification change, parameter change, rule override) requires a decision record
- [ ] Each decision links to: the trigger that prompted it, the compliance state at the time, the specific rules involved, and a rationale
- [ ] Command: `towsand decide <type> --trigger <trigger> --rationale "<text>"` — record a decision with structured metadata
- [ ] Command: `towsand decisions [--since <date>] [--type <type>] [--trigger <trigger>]` — query decision history
- [ ] Command: `towsand decide review` — show decisions that lack outcome notes (for periodic follow-up)
- [ ] Approved actions from 6.5 automatically generate a linked decision record
- [ ] Rule 9.2 (no-action rule) is auditable: absence of decisions between triggers is the proof

---

## Phase 7 — Interfaces

### 7.1 CLI (click-based)
- [ ] `towsand` as the root command group
- [ ] All commands listed above under their respective phases
- [ ] `towsand status` — one-screen overview: portfolio value, compliance summary, top gaps, pending actions
- [ ] `towsand init` — first-time setup wizard (create DB, seed parameters, import institutions)

### 7.2 Lightweight web UI
- [ ] Flask/FastAPI app serving a single-page dashboard
- [ ] Panels: portfolio value & allocation pie, compliance status (green/amber/red per rule), top recommendations, recent decisions & pending outcome reviews
- [ ] Read-only — all mutations via CLI
- [ ] Command: `towsand ui` — start local web server

### 7.3 Cursor `/` commands ✓
- [x] `/portfolio-report` — AI agent runs full analysis (valuation, compliance, risk, exposures) and writes a dated report to `reports/`
- [x] `/compliance-check` — AI agent runs compliance, explains breaches in plain language, suggests prioritised fixes
- [x] `/recommend` — AI agent generates specific buy/sell recommendations with amounts, anchored to strategy docs and rules
- [x] `/what-if <description>` — AI agent models a hypothetical trade and shows before/after compliance impact
- [x] `/log-decision` — AI agent walks through structured decision recording with triggers, rules, rationale
- [ ] `/classify` — AI agent helps classify untagged instruments by analysing their characteristics

---

## Phase 8 — Data Integrity & Ongoing Operations

### 8.1 Data quality *(partially done)*
- [x] Stale data warnings: prices >7 days and FX rates >7 days flagged in compliance (check D.1, D.2)
- [x] Unclassified holdings produce warnings (compliance runs with available data — "provisional compliance")
- [ ] Validation: prices must be <5 trading days old for compliance results to be marked "current" vs "provisional"

### 8.2 Backup & history
- [ ] SQLite DB file stored at `data/towsand.db` — **excluded from git** (see `.gitignore`)
- [ ] `towsand snapshot` — save a timestamped compliance + portfolio snapshot
- [ ] Periodic `sqlite3 .dump` or CSV/JSON export for history (not git-tracked DB)

### 8.3 Documentation
- [ ] `README.md` in project root with setup instructions
- [ ] `project/rules/` — copy of management rules in machine-readable form (or reference to `current-finances/`)
- [ ] Each Cursor `/` command documented with examples

---

## Dependency Order

```
Phase 1 (Foundation)
  └─► Phase 2 (Market Data)
        └─► Phase 3 (Valuation & Classification)
              ├─► Phase 4 (Compliance Engine)
              │     └─► Phase 6 (Recommendations) ◄── primary value
              └─► Phase 5 (Analytics & Risk)
                    └─► Phase 6 (Recommendations)
Phase 7 (Interfaces) can begin after Phase 3, grows with each phase
Phase 8 (Operations) runs in parallel from Phase 1 onward
```

---

## Open Items (Require User Input)

1. **Holding-level detail** — Need ticker-by-ticker breakdown of Interactive Brokers and CommSec accounts to seed the database. Export from broker (CSV/PDF) or manual list.
2. **Income visibility** — How many months of forward income visibility do you currently have? (Drives Rule 2.2 assessment.)
3. **Instrument watchlist** — For the screening/recommendation engine: do you have a universe of candidate instruments in mind, or should we build one?
4. **Dividend tracking** — Do you want to track dividend income, or is price return sufficient for now?
5. **Eroza owed ($60,000)** — How should this be treated? Receivable with expected date? Exclude from investable assets?
6. **Below-the-line accounts** — The items below the `---` line in institutions.md (Wise USD, Bondora, Cash USD, N26, Cash AUD, ANZ credit card) — are these in-scope for portfolio management or purely operational?
7. **Credit card balance ($692.50)** — Treat as a liability to net off, or ignore?
