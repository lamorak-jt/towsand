# Portfolio Report — 2026-02-17

All monetary values are in **AUD** unless stated otherwise.

## Executive Summary

- **Investable assets:** **1,781,774.17**
  - **Holdings:** 1,239,868.57
  - **Investable cash (allocated to stabiliser per Rule 1.1a):** 541,905.61
  - **Non-investable (excluded from investable-assets denominator, Rule 0):** 59,307.50
- **Compliance:** **10 pass, 4 warning, 3 breach**
  - **Breaches:** **[1.1-C]** compounder band, **[3.1-eq]** single-security cap (FLBL), **[6.1]** convexity test (GHY.AX)
  - **Key warnings:** **[1.1-S]** stabiliser overweight, **[7.3]** inflation coverage gap, **[8.2]** credit-spread correlation cluster
- **Key finding:** Portfolio is materially **underdeployed**: stabiliser is **54.6%** (target 15–25%) driven by **541.9k investable cash**, while compounder is **45.0%** (min 50%).
- **Top actions:**
  - **Deploy ~527.6k** from stabiliser (cash) into compounders/optionality to move stabiliser back toward the **25% cap** (Rule 1.1).
  - **Trim FLBL by ~60.8k** to bring it back under the **10%** single-security cap (Rule 3.1).
  - Add **inflation-linked stabiliser** exposure to reach **≥25%** of stabiliser (Rule 7.3), e.g. Australian Treasury Indexed Bonds (GSBI series).

## Portfolio Composition

### Holdings (market value)

| Ticker | Type | Ccy | Qty | Price | AUD Value | Role | Price date |
|--------|------|-----|-----|-------|-----------|------|------------|
| AGL.AX | equity | AUD | 6,550.00 | 10.3400 | 67,727.00 | compounder | 2026-02-17 |
| AGVT.AX | etf | AUD | 2,300.00 | 41.5100 | 95,473.00 | stabiliser | 2026-02-17 |
| BHP.AX | equity | AUD | 3,200.00 | 53.0300 | 169,696.00 | compounder | 2026-02-17 |
| CRED.AX | etf | AUD | 5,440.00 | 23.3200 | 126,860.80 | compounder | 2026-02-17 |
| FLBL | etf | USD | 7,300.00 | 23.1100 | 239,018.42 | compounder | 2026-02-13 |
| GHY.AX | equity | AUD | 20,522.00 | 0.3550 | 7,285.31 | optionality | 2026-02-17 |
| GSBG27.AX | govt_bond_nominal | AUD | 1,742.00 | 102.2500 | 178,119.50 | stabiliser | 2026-02-17 |
| GSBG33.AX | govt_bond_nominal | AUD | 349.00 | 101.5700 | 35,447.93 | stabiliser | 2026-02-17 |
| JPST | etf | USD | 1,700.00 | 50.7100 | 122,138.08 | stabiliser | 2026-02-13 |
| ORG.AX | equity | AUD | 1,500.00 | 11.7600 | 17,640.00 | compounder | 2026-02-17 |
| SOL.AX | equity | AUD | 2,000.00 | 37.1500 | 74,300.00 | compounder | 2026-02-17 |
| TCPC | equity | USD | 8,000.00 | 4.8000 | 54,405.12 | compounder | 2026-02-13 |
| UKW | listed_fund | GBP | 28,464.00 | 0.9425 | 51,757.41 | compounder | 2026-02-16 |
| **Holdings total** | | | | | **1,239,868.57** | | |

### Cash balances

#### Investable cash (included in investable assets; allocated to stabiliser per Rule 1.1a)

| Account | Ccy | Balance | AUD Value | As of |
|---------|-----|---------:|----------:|-------|
| Jacob ANZ Savings | AUD | 3,032.39 | 3,032.39 | 2026-02-17 |
| Jacob RACQ Bonus Saver | AUD | 80,557.22 | 80,557.22 | 2026-02-17 |
| Jacob RACQ Everyday | AUD | 8,872.24 | 8,872.24 | 2026-02-17 |
| Darlene RACQ Everyday | AUD | 6,122.03 | 6,122.03 | 2026-02-17 |
| IB Trading AUD | AUD | 134,186.36 | 134,186.36 | 2026-02-17 |
| IB Trading AUD | GBP | 2,211.66 | 4,266.91 | 2026-02-17 |
| IB Trading AUD | USD | 198,084.54 | 280,646.18 | 2026-02-17 |
| N26 Darlene | EUR | 3,108.00 | 5,216.28 | 2026-02-17 |
| N26 Jacob | EUR | 1,535.68 | 2,577.39 | 2026-02-17 |
| Isepankur - Bondora | EUR | 2,041.00 | 3,425.49 | 2026-02-17 |
| Wise EUR | EUR | 3,928.70 | 6,593.69 | 2026-02-17 |
| Wise GBP | GBP | 235.17 | 453.71 | 2026-02-17 |
| Wise USD | USD | 2,562.47 | 3,630.51 | 2026-02-17 |
| Cash AUD | AUD | 200.00 | 200.00 | 2026-02-17 |
| Cash USD | USD | 1,500.00 | 2,125.20 | 2026-02-17 |
| **Investable cash total** | | | **541,905.61** | |

#### Non-investable (excluded from investable-assets denominator; shown for completeness)

| Account | Ccy | Balance | AUD Value | As of | Note |
|---------|-----|---------:|----------:|-------|------|
| Jacob ANZ Credit Card | AUD | -692.50 | -692.50 | 2026-02-17 | excluded (Rule 0) |
| Eroza Owed | AUD | 60,000.00 | 60,000.00 | 2026-02-17 | excluded (Rule 0) |
| **Non-investable total** | | | **59,307.50** | | |

### Role allocation (Rule 1.1; denominator = investable assets)

| Role | AUD Value | % | Target band | Status |
|------|----------:|---:|------------|--------|
| Stabiliser | 973,084.11 | 54.6% | 15–25% | ⚠ Warning ([1.1-S]) |
| Compounder | 801,404.76 | 45.0% | 50–65% | ✗ Breach ([1.1-C]) |
| Optionality | 7,285.31 | 0.4% | 10–20% | ⚠ Warning ([1.1-O]) |

## Compliance Status

| Rule | Status | Detail |
|------|--------|--------|
| [D.1] Data Freshness | ✓ Pass | All prices and FX rates are current (≤7 days old). |
| [2.1] Income Substitution | ✓ Pass | Stabiliser covers **108.1 months** of expenses (≥24 required). |
| [1.1-S] Stabiliser Band | ⚠ Warning | Stabiliser at **54.6%** (target 15–25%), includes **541,906** investable cash. Over by **527,641**. |
| [1.1-C] Compounder Band | ✗ Breach | Compounder at **45.0%** (min 50%). |
| [1.1-O] Optionality Band | ⚠ Warning | Optionality at **0.4%** (target 10–20%). |
| [2.2] Income Shock | ✓ Pass | No income shock active. |
| [3.1-eq] Single Equity Cap | ✗ Breach | FLBL at **13.4%** (max 10%). |
| [4.1] Australia Concentration | ✓ Pass | AUD risk assets at **31.4%** (max 55%). |
| [4.2] Macro Driver Exposure | ✓ Pass | No macro driver exceeds 30%. |
| [5.1] AUD Growth Exposure | ✓ Pass | AUD growth at **57.3%** (target 50–70%). |
| [5.2] Hedging Rule | ✓ Pass | 100.0% of international growth is unhedged (≥40% required). |
| [6.1] Convexity Test | ✗ Breach | GHY.AX scores **0/3** on payoff shape (need ≥2). |
| [7.1] Stabiliser Liquidity | ✓ Pass | 100.0% liquid within 5 days (≥70% required). |
| [7.3] Inflation Coverage | ⚠ Warning | 0.0% of stabiliser is inflation-linked (target ≥25%). |
| [8.1] Drawdown Tolerance | ✓ Pass | After 35% equity drawdown, stabiliser still covers 24 months (216,000). |
| [8.2] Stress Correlation | ⚠ Warning | Correlation group `credit_spread` at **23.6%** (treat as one risk in stress). |
| [9.2] No Action Rule | ✓ Pass | No review triggers active. |

### What the warnings/breaches mean (plain language)

- **[1.1-S] / [1.1-C] role bands:** You have far more stabiliser than required once Rule 2.1 is satisfied, and correspondingly too little compounder. Per Rule 1.1 breach action, this should be corrected within 30 days unless it’s purely small market drift (<10% moves).
- **[3.1-eq] FLBL sizing:** FLBL is one line item exceeding the explicit 10% cap.
- **[6.1] optionality convexity:** As currently classified, GHY.AX does not meet the “true optionality” requirements (Strategy §5; Rule 6.1).
- **[7.3] inflation coverage:** Stabiliser has no explicit inflation-linked instruments, leaving the “survivability” bucket exposed to inflation shocks.
- **[8.2] correlation stress:** Credit exposures behave like one position in stress; treat `CRED.AX + FLBL + TCPC` as a single risk cluster when sizing and when deploying new cash.

## Risk Analysis

### Position Concentration

- **Single-security cap (Rule 3.1):** FLBL is **239,018.42** = **13.4%** of investable assets.
  - 10% cap = 178,177.42 ⇒ **trim required ≈ 60,841** (before costs) to bring FLBL to ≤10%.

### Macro Driver Exposure

From `towsand portfolio exposures` (total = investable assets **1,781,774.17**):

| Macro driver | AUD | % |
|-------------|----:|--:|
| au_interest_rates | 435,901.22 | 24.5% |
| global_credit_spreads | 420,284.34 | 23.6% |
| us_interest_rates | 361,156.50 | 20.3% |
| bulk_commodities | 243,996.00 | 13.7% |
| china_demand | 169,696.00 | 9.5% |
| au_domestic_demand | 159,667.00 | 9.0% |
| au_energy | 85,367.00 | 4.8% |
| energy_transition | 59,042.72 | 3.3% |
| us_private_credit | 54,405.12 | 3.1% |
| uk_inflation | 51,757.41 | 2.9% |

### Corporate Group Concentration

From `towsand portfolio exposures`:

| Corporate group | AUD | % |
|----------------|----:|--:|
| AU Government | 309,040.43 | 17.3% |
| US Senior Loans | 239,018.42 | 13.4% |
| BHP Group | 169,696.00 | 9.5% |
| AU IG Corporate | 126,860.80 | 7.1% |
| US Short Duration | 122,138.08 | 6.9% |
| Soul Pattinson | 74,300.00 | 4.2% |
| AGL Energy | 67,727.00 | 3.8% |
| BlackRock TCP Capital | 54,405.12 | 3.1% |
| Greencoat Capital | 51,757.41 | 2.9% |
| Origin Energy | 17,640.00 | 1.0% |
| Gold Hydrogen | 7,285.31 | 0.4% |

### Currency Exposure

From `towsand portfolio summary`:

- **AUD:** 56.4%
- **USD:** 39.4%
- **GBP:** 3.2%
- **EUR:** 1.0%

Hedging status (from `towsand classify list`): international growth is **100% unhedged**, satisfying Rule 5.2 (≥40% unhedged).

## Stabiliser Assessment

- **Liquidity (Rule 7.1):** pass (100% liquid within 5 days).
- **Expense coverage (Rule 2.1):** pass (108.1 months).
  - Implied monthly core expenses ≈ \(973,084.11 / 108.1\) ≈ **9,000**.
- **Inflation coverage (Rule 7.3):** warning (0% inflation-linked).
  - On current stabiliser size, 25% target implies ~**243k** inflation-linked stabiliser. (Note: this number should be recalculated after stabiliser is resized via deployment.)

## Key Concerns & Recommended Actions

1. **Deploy excess stabiliser cash to restore role bands** (Rule 1.1)
   - Stabiliser is over the 25% cap by **~527.6k**; compounder is under the 50% floor.
   - Action: deploy cash systematically into compounders (and some true optionality) over the next 30 days per Rule 1.1 breach action.

2. **Fix the FLBL sizing breach** (Rule 3.1)
   - Action: trim **~60.8k** from FLBL (or otherwise restructure holdings) so the position is ≤10% of investable assets.
   - While doing (1), avoid re-inflating the `credit_spread` correlation cluster (Rule 8.2).

3. **Add explicit inflation protection to stabiliser** (Rule 7.3)
   - Action: introduce Treasury Indexed Bonds (e.g. ASX GSBI series) sized to reach ≥25% inflation-linked stabiliser **after** stabiliser is resized.

## Appendix: Raw Data

### FX (key pairs used)

| Pair | Rate | Date | Source |
|------|------|------|--------|
| USD/AUD | 1.416800 | 2026-02-17 | yfinance |
| GBP/AUD | 1.929280 | 2026-02-17 | yfinance |
| EUR/AUD | 1.678340 | 2026-02-17 | yfinance |

### Latest prices (with dates)

| Ticker | Price | Ccy | Date | Source |
|--------|------:|-----|------|--------|
| AGL.AX | 10.3400 | AUD | 2026-02-17 | yfinance |
| AGVT.AX | 41.5100 | AUD | 2026-02-17 | yfinance |
| BHP.AX | 53.0300 | AUD | 2026-02-17 | yfinance |
| CRED.AX | 23.3200 | AUD | 2026-02-17 | yfinance |
| FLBL | 23.1100 | USD | 2026-02-13 | yfinance |
| GHY.AX | 0.3550 | AUD | 2026-02-17 | yfinance |
| GSBG27.AX | 102.2500 | AUD | 2026-02-17 | yfinance |
| GSBG33.AX | 101.5700 | AUD | 2026-02-17 | yfinance |
| JPST | 50.7100 | USD | 2026-02-13 | yfinance |
| ORG.AX | 11.7600 | AUD | 2026-02-17 | yfinance |
| SOL.AX | 37.1500 | AUD | 2026-02-17 | yfinance |
| TCPC | 4.8000 | USD | 2026-02-13 | yfinance |
| UKW | 0.9425 | GBP | 2026-02-16 | yfinance |

# Portfolio Report — 2026-02-17

## Executive Summary

- **Total Portfolio Value:** AUD 1,841,081.67
  - Holdings: AUD 1,239,868.57 (67.3%)
  - Cash: AUD 601,213.11 (32.7%, allocated to stabiliser)

- **Compliance Status:** 9 pass, 4 warning, 3 breach
  - Critical breaches: Stabiliser over-allocated (56.1% vs 15-25%), Compounder under-allocated (43.5% vs 50-65%), FLBL position exceeds 10% cap (13.0%)

- **Key Finding:** Portfolio is significantly underdeployed with excess stabiliser capital (AUD 572,121 over target). Large cash allocation (AUD 601k) is driving stabiliser overweight, while compounder allocation is below minimum threshold.

- **Top Action:** Deploy AUD ~570k from stabiliser (cash) into compounder positions to restore role allocation bands. Address FLBL position size breach (trim or reclassify). Add inflation-linked bonds to stabiliser (currently 0% vs 25% requirement).

---

## Portfolio Composition

### Holdings Summary

| Ticker | Type | Currency | Quantity | Price | AUD Value | Role | Date |
|--------|------|----------|----------|-------|-----------|------|------|
| FLBL | etf | USD | 7,300.00 | 23.1100 | 239,018.42 | compounder | 2026-02-13 |
| BHP.AX | equity | AUD | 3,200.00 | 53.0300 | 169,696.00 | compounder | 2026-02-17 |
| GSBG27.AX | govt_bond_nominal | AUD | 1,742.00 | 102.2500 | 178,119.50 | stabiliser | 2026-02-17 |
| CRED.AX | etf | AUD | 5,440.00 | 23.3200 | 126,860.80 | compounder | 2026-02-17 |
| AGVT.AX | etf | AUD | 2,300.00 | 41.5100 | 95,473.00 | stabiliser | 2026-02-17 |
| SOL.AX | equity | AUD | 2,000.00 | 37.1500 | 74,300.00 | compounder | 2026-02-17 |
| AGL.AX | equity | AUD | 6,550.00 | 10.3400 | 67,727.00 | compounder | 2026-02-17 |
| JPST | etf | USD | 1,700.00 | 50.7100 | 122,138.08 | stabiliser | 2026-02-13 |
| GSBG33.AX | govt_bond_nominal | AUD | 349.00 | 101.5700 | 35,447.93 | stabiliser | 2026-02-17 |
| TCPC | equity | USD | 8,000.00 | 4.8000 | 54,405.12 | compounder | 2026-02-13 |
| UKW | listed_fund | GBP | 28,464.00 | 0.9425 | 51,757.41 | compounder | 2026-02-16 |
| ORG.AX | equity | AUD | 1,500.00 | 11.7600 | 17,640.00 | compounder | 2026-02-17 |
| GHY.AX | equity | AUD | 20,522.00 | 0.3550 | 7,285.31 | optionality | 2026-02-17 |
| **Total Holdings** | | | | | **1,239,868.57** | | |

### Cash Balances

| Account | Currency | Balance | AUD Value | As Of |
|---------|----------|---------|-----------|-------|
| IB Trading AUD (USD) | USD | 198,084.54 | 280,646.18 | 2026-02-17 |
| IB Trading AUD (AUD) | AUD | 134,186.36 | 134,186.36 | 2026-02-17 |
| Jacob RACQ Bonus Saver | AUD | 80,557.22 | 80,557.22 | 2026-02-17 |
| Eroza Owed | AUD | 60,000.00 | 60,000.00 | 2026-02-17 |
| IB Trading AUD (GBP) | GBP | 2,211.66 | 4,266.91 | 2026-02-17 |
| Jacob RACQ Everyday | AUD | 8,872.24 | 8,872.24 | 2026-02-17 |
| Darlene RACQ Everyday | AUD | 6,122.03 | 6,122.03 | 2026-02-17 |
| Wise EUR | EUR | 3,928.70 | 6,593.69 | 2026-02-17 |
| N26 Darlene | EUR | 3,108.00 | 5,216.28 | 2026-02-17 |
| Isepankur - Bondora | EUR | 2,041.00 | 3,425.49 | 2026-02-17 |
| Wise USD | USD | 2,562.47 | 3,630.51 | 2026-02-17 |
| N26 Jacob | EUR | 1,535.68 | 2,577.39 | 2026-02-17 |
| Cash USD | USD | 1,500.00 | 2,125.20 | 2026-02-17 |
| Wise GBP | GBP | 235.17 | 453.71 | 2026-02-17 |
| Cash AUD | AUD | 200.00 | 200.00 | 2026-02-17 |
| Jacob ANZ Savings | AUD | 3,032.39 | 3,032.39 | 2026-02-17 |
| Jacob ANZ Credit Card | AUD | -692.50 | -692.50 | 2026-02-17 |
| **Total Cash** | | | **601,213.11** | |

### Role Allocation

| Role | AUD Value | % of Portfolio | Target Band | Status |
|------|-----------|----------------|-------------|--------|
| Stabiliser | 1,032,391.61 | 56.1% | 15-25% | **BREACH** (over by AUD 572,121) |
| Compounder | 801,404.76 | 43.5% | 50-65% | **BREACH** (under by AUD 118,595) |
| Optionality | 7,285.31 | 0.4% | 10-20% | **WARNING** (under by AUD 177,000-361,000) |

**Note:** All cash balances are allocated to Stabiliser Capital per Rule 1.1a. Cash satisfies stabiliser criteria (liquid, short duration, yield-bearing) but does not meet optionality convexity requirements.

### Portfolio Breakdown

**By Instrument Type:**
- ETF: AUD 583,490.29 (31.7%)
- Equity: AUD 391,053.43 (21.2%)
- Government Bonds (Nominal): AUD 213,567.43 (11.6%)
- Listed Fund: AUD 51,757.41 (2.8%)

**By Currency:**
- AUD: AUD 1,064,827.28 (57.8%)
- USD: AUD 701,963.51 (38.1%)
- GBP: AUD 56,478.03 (3.1%)
- EUR: AUD 17,812.86 (1.0%)

**By Country:**
- Australia: AUD 772,549.53 (42.0%)
- United States: AUD 415,561.62 (22.6%)
- United Kingdom: AUD 51,757.41 (2.8%)

**By Institution:**
- Interactive Brokers: AUD 1,445,400.59 (78.5%)
- CommSec: AUD 213,567.43 (11.6%)
- RACQ: AUD 95,551.49 (5.2%)
- Eroza: AUD 60,000.00 (3.3%)
- Wise: AUD 10,677.91 (0.6%)
- N26: AUD 7,793.67 (0.4%)
- Bondora: AUD 3,425.49 (0.2%)
- ANZ: AUD 2,339.89 (0.1%)
- Physical Cash: AUD 2,325.20 (0.1%)

---

## Compliance Status

| Rule | Status | Detail |
|------|--------|--------|
| [2.1] Income Substitution | ✓ PASS | Stabiliser covers 114.7 months of expenses (≥24 required). |
| [1.1-S] Stabiliser Band | ⚠ WARNING | Stabiliser at 56.1% (target 15-25%). Over-allocated by AUD 572,121. Driven by large cash allocation (AUD 601k). Consider deploying into compounders/optionality. |
| [1.1-C] Compounder Band | ✗ BREACH | Compounder at 43.5% (min 50%). Under-allocated by AUD 118,595. Mirror of stabiliser overweight. |
| [1.1-O] Optionality Band | ⚠ WARNING | Optionality at 0.4% (target 10-20%). Under-allocated by AUD 177,000-361,000. Only GHY.AX position. |
| [2.2] Income Shock | ✓ PASS | No income shock active. |
| [3.1-eq] Single Equity Cap | ✗ BREACH | FLBL at 13.0% (max 10%). AUD 239,018 exceeds cap by AUD 33,000. FLBL is a diversified ETF (300+ loans) but still breaches rule. |
| [4.1] Australia Concentration | ✓ PASS | AUD risk assets at 30.4% (max 55%). |
| [4.2] Macro Driver Exposure | ✓ PASS | No macro driver exceeds 30%. Highest is global_credit_spreads at 22.8%. |
| [5.1] AUD Growth Exposure | ✓ PASS | AUD growth at 57.3% (target 50-70%). |
| [5.2] Hedging Rule | ✓ PASS | 100.0% of international growth is unhedged (≥40% required). |
| [6.1] Convexity Test | ✗ BREACH | GHY.AX scores 0/3 on payoff shape (need ≥2). Requires explicit convexity flags in classification. |
| [7.1] Stabiliser Liquidity | ✓ PASS | 100.0% of stabiliser liquid within 5 days (≥70% required). |
| [7.3] Inflation Coverage | ⚠ WARNING | Only 0.0% of stabiliser is inflation-linked (target ≥25%). No Treasury Indexed Bonds (GSBI series) held. |
| [8.1] Drawdown Tolerance | ✓ PASS | After 35% equity drawdown, stabiliser AUD 1,032,392 still covers 24 months (AUD 216,000). |
| [8.2] Stress Correlation | ⚠ WARNING | Correlation group 'credit_spread' at 22.8% (>0.7 stress corr → single risk). CRED.AX, FLBL, TCPC should be treated as one position for sizing. |
| [9.2] No Action Rule | ✓ PASS | No review triggers active. Absent a trigger, no discretionary rebalancing. |

### Compliance Explanation

**Rule 1.1-S (Stabiliser Band) — WARNING:** The stabiliser allocation is 56.1%, more than double the upper bound of 25%. This is driven by the large cash allocation (AUD 601k), which is correctly classified as stabiliser per Rule 1.1a. However, Rule 1.1 specifies that stabiliser should be 15-25% once the absolute expense-coverage requirement (Rule 2.1) is met. With 114.7 months of expense coverage, the portfolio has excess stabiliser capital that should be deployed into compounder or optionality roles.

**Rule 1.1-C (Compounder Band) — BREACH:** At 43.5%, compounder allocation is below the minimum 50% threshold. This is the mirror image of the stabiliser overweight. The portfolio is underdeployed relative to its growth objectives. Approximately AUD 118k-570k should be shifted from stabiliser (cash) to compounder positions.

**Rule 1.1-O (Optionality Band) — WARNING:** Optionality allocation is only 0.4% (AUD 7,285), well below the 10-20% target band. Only GHY.AX is classified as optionality, and it fails the convexity test (Rule 6.1). The portfolio lacks meaningful asymmetric/convex exposure.

**Rule 3.1-eq (Single Equity Cap) — BREACH:** FLBL represents 13.0% of total portfolio value (AUD 239,018), exceeding the 10% single-position cap. While FLBL is a diversified ETF (300+ senior loans), Rule 3.1 applies to all single securities. Options: (1) trim FLBL position by AUD ~55k to bring it under 10%, (2) reclassify FLBL if the rule intent is to limit idiosyncratic risk (which is lower for diversified ETFs), or (3) accept the breach if FLBL's diversification justifies the exception.

**Rule 6.1 (Convexity Test) — BREACH:** GHY.AX fails the convexity test, scoring 0/3 on payoff shape characteristics. The system requires explicit convexity flags in the classification data. GHY.AX is conceptually optionality (binary outcome, small size caps downside) but lacks the formal flags needed to pass Rule 6.1.

**Rule 7.3 (Inflation Coverage) — WARNING:** Zero percent of stabiliser is in inflation-linked instruments, versus the 25% requirement. All stabiliser holdings are nominal bonds (AGVT.AX, GSBG27.AX, GSBG33.AX, JPST) or cash. Consider adding ASX-listed Treasury Indexed Bonds (GSBI series) to meet this requirement.

**Rule 8.2 (Stress Correlation) — WARNING:** The credit_spread correlation group (CRED.AX, FLBL, TCPC) represents 22.8% of total portfolio. Under Rule 8.2, assets with >0.7 correlation in stress periods should be treated as one risk for sizing purposes. This group exceeds 20% and should be considered a concentrated risk position.

---

## Risk Analysis

### Position Concentration

**Single Position Sizing:**
- FLBL: 13.0% (BREACH — exceeds 10% cap)
- BHP.AX: 9.2% (within limit)
- GSBG27.AX: 9.7% (within limit)
- CRED.AX: 6.9% (within limit)

**Corporate Group Concentration:**
- AU Government: 16.8% (within 20% limit)
- US Senior Loans (FLBL): 13.0% (within 20% limit)
- BHP Group: 9.2% (within limit)

All corporate group concentrations are within the 20% limit per Rule 3.2.

### Macro Driver Exposure

| Macro Driver | AUD Value | % of Portfolio | Limit | Status |
|--------------|-----------|----------------|-------|--------|
| au_interest_rates | 435,901.22 | 23.7% | 30% | OK |
| global_credit_spreads | 420,284.34 | 22.8% | 30% | OK |
| us_interest_rates | 361,156.50 | 19.6% | 30% | OK |
| bulk_commodities | 243,996.00 | 13.3% | 30% | OK |
| china_demand | 169,696.00 | 9.2% | 30% | OK |
| au_domestic_demand | 159,667.00 | 8.7% | N/A | OK |
| au_energy | 85,367.00 | 4.6% | N/A | OK |
| energy_transition | 59,042.72 | 3.2% | N/A | OK |
| us_private_credit | 54,405.12 | 3.0% | N/A | OK |
| uk_inflation | 51,757.41 | 2.8% | N/A | OK |

All Rule 4.2 named drivers (bulk_commodities, china_demand, global_credit_spreads, Australian housing) are within the 30% limit. Global credit spreads at 22.8% is the highest concentration and approaches the cap.

### Correlation Groups

**Credit Spread Group (Rule 8.2):**
- CRED.AX: AUD 126,860.80
- FLBL: AUD 239,018.42
- TCPC: AUD 54,405.12
- **Total:** AUD 420,284.34 (22.8% of portfolio)

These instruments have >0.7 correlation in stress periods and should be treated as one risk position. At 22.8%, this represents a concentrated risk exposure.

**Other Correlation Groups:**
- au_equity_beta: BHP.AX, AGL.AX, ORG.AX, SOL.AX (AUD 328,363)
- au_govt_bond: AGVT.AX, GSBG27.AX, GSBG33.AX (AUD 309,040)
- us_short_duration: JPST (AUD 122,138)

### Currency Exposure

**Growth Capital Currency Split:**
- AUD: AUD 463,000 (57.3% of growth capital) — within 50-70% band
- International (unhedged): AUD 467,300 (42.7% of growth capital) — 100% unhedged, exceeds 40% minimum

**Currency Risk:**
- USD exposure: AUD 701,964 (38.1% of total portfolio)
- GBP exposure: AUD 56,478 (3.1%)
- EUR exposure: AUD 17,813 (1.0%)

All international exposure is unhedged, providing regime insurance but exposing the portfolio to currency volatility. This is compliant with Rule 5.2 but represents a significant FX exposure.

---

## Stabiliser Assessment

### Expense Coverage

- **Stabiliser Capital:** AUD 1,032,391.61
- **Monthly Expenses:** AUD 9,000 (assumed)
- **Coverage:** 114.7 months (9.6 years)
- **Requirement:** 24 months minimum
- **Status:** ✓ PASS (well above requirement)

### Liquidity

- **Liquid within 5 days:** 100.0% of stabiliser
- **Requirement:** ≥70%
- **Status:** ✓ PASS

**Breakdown:**
- AGVT.AX: 1 day
- GSBG27.AX: 2 days
- GSBG33.AX: 2 days
- JPST: 1 day
- Cash: Instant

### Duration Distribution

| Duration Bucket | Instruments | AUD Value | % of Stabiliser |
|----------------|-------------|-----------|-----------------|
| Ultra-short (<1yr) | JPST, Cash | ~723,000 | ~70% |
| Short (1-2yr) | GSBG27.AX | 178,120 | 17% |
| Medium (5-6yr) | AGVT.AX | 95,473 | 9% |
| Long (7yr+) | GSBG33.AX | 35,448 | 3% |

**Rule 7.2 Check:** No single duration point exceeds 40% of stabiliser capital. The ultra-short bucket is large (70%) but includes cash, which has zero duration.

### Inflation Coverage

- **Inflation-linked instruments:** 0.0% of stabiliser
- **Requirement:** ≥25%
- **Status:** ⚠ WARNING

**Gap:** AUD ~258,000 of inflation-linked bonds needed (25% of AUD 1,032,392 stabiliser).

**Recommendation:** Add ASX-listed Treasury Indexed Bonds (GSBI series) to stabiliser allocation. These provide CPI-linked returns and protect purchasing power.

---

## Key Concerns & Recommended Actions

### 1. **URGENT: Deploy Excess Stabiliser Capital** (Rule 1.1-S, 1.1-C)

**Issue:** Stabiliser is over-allocated by AUD 572,121 (56.1% vs 15-25% target), while compounder is under-allocated by AUD 118,595 (43.5% vs 50-65% minimum). This is driven by large cash balances (AUD 601k).

**Action:**
- Deploy AUD ~570k from cash into compounder positions to restore role allocation bands
- Target compounder allocation: 50-65% (currently 43.5%)
- This will reduce stabiliser from 56.1% to ~25% (upper bound)
- Consider deploying into existing compounder positions or new opportunities

**Priority:** High — this is a structural allocation issue affecting portfolio growth objectives.

---

### 2. **URGENT: Address FLBL Position Size Breach** (Rule 3.1-eq)

**Issue:** FLBL represents 13.0% of portfolio (AUD 239,018), exceeding the 10% single-position cap by AUD 33,000.

**Options:**
- **Option A:** Trim FLBL by AUD ~55k to bring it under 10% cap
- **Option B:** Reclassify FLBL if Rule 3.1 intent is to limit idiosyncratic risk (FLBL is a diversified ETF with 300+ loans, so idiosyncratic risk is lower)
- **Option C:** Accept breach if FLBL's diversification justifies exception (document rationale)

**Recommendation:** Option A — trim FLBL to 10% (AUD ~184k) and redeploy excess into other compounder positions for diversification.

**Priority:** High — active compliance breach requiring resolution.

---

### 3. **HIGH: Add Inflation-Linked Bonds to Stabiliser** (Rule 7.3)

**Issue:** Zero percent of stabiliser is inflation-linked, versus 25% requirement. This leaves the portfolio exposed to inflation risk in the stabiliser bucket.

**Action:**
- Add AUD ~258k of ASX-listed Treasury Indexed Bonds (GSBI series) to stabiliser
- This represents 25% of current stabiliser allocation (AUD 1,032k)
- Consider GSBI bonds with maturities matching the income bridge horizon (2027-2033)

**Priority:** High — addresses inflation protection gap in stabiliser.

---

### 4. **MEDIUM: Build Optionality Allocation** (Rule 1.1-O)

**Issue:** Optionality allocation is only 0.4% (AUD 7,285), well below the 10-20% target band. GHY.AX fails the convexity test.

**Action:**
- Increase optionality allocation to 10-20% (AUD 184k-368k)
- Add instruments with convex payoff profiles (limited downside, asymmetric upside)
- Consider: options strategies, structured products, or other instruments satisfying Rule 6.1 convexity test
- Fix GHY.AX classification if it conceptually meets optionality criteria

**Priority:** Medium — important for portfolio asymmetry but not urgent given current compliance status.

---

### 5. **MEDIUM: Monitor Credit Spread Correlation Group** (Rule 8.2)

**Issue:** Credit spread correlation group (CRED.AX, FLBL, TCPC) represents 22.8% of portfolio. Under Rule 8.2, these should be treated as one risk position.

**Action:**
- Monitor credit spread exposure — avoid adding more credit instruments that would increase this concentration
- Consider reducing credit exposure if it approaches 30% (Rule 4.2 macro driver limit)
- Diversify into non-credit compounder positions when deploying cash

**Priority:** Medium — currently within limits but requires monitoring.

---

### 6. **LOW: Review Currency Hedging Strategy** (Rule 5.2)

**Issue:** 100% of international exposure is unhedged. While compliant (≥40% required), this represents significant FX exposure.

**Action:**
- Consider whether 100% unhedged is intentional for regime insurance
- If desired, maintain current approach
- If concerned about FX volatility, consider hedging a portion (maintain ≥40% unhedged minimum)

**Priority:** Low — compliant and may be intentional per strategy.

---

## Deployment Opportunities

With AUD ~570k excess stabiliser (cash) available for deployment:

**Recommended Deployment Strategy:**

1. **Address FLBL breach:** Trim FLBL by AUD ~55k (reduce from 13.0% to 10%)
2. **Add inflation-linked bonds:** Deploy AUD ~258k into GSBI Treasury Indexed Bonds (meets Rule 7.3)
3. **Increase compounder allocation:** Deploy remaining AUD ~257k into compounder positions
   - Consider: additional BHP.AX, CRED.AX, or new opportunities
   - Target: bring compounder from 43.5% to ~50-55%
4. **Build optionality:** Allocate AUD ~50-100k to optionality positions (bring from 0.4% to ~3-5% as first step)

**Total Deployment:** AUD ~570k
- Inflation-linked bonds: AUD 258k
- Compounder positions: AUD 257k
- Optionality: AUD 55k (from FLBL trim)

This would restore role allocation bands while addressing compliance breaches.

---

## Appendix: Raw Data

### FX Rates (as of 2026-02-17)

| Pair | Rate | Date | Source |
|------|------|------|--------|
| USD/AUD | 1.4168 | 2026-02-17 | yfinance |
| GBP/AUD | 1.9293 | 2026-02-17 | yfinance |
| EUR/AUD | 1.6783 | 2026-02-17 | yfinance |

**Data Freshness:** USD/AUD and GBP/AUD rates are current (2026-02-17). EUR/AUD rate is from 2026-02-17. Most IB Flex rates are from 2026-02-13 (4 days old).

### Price Dates

| Ticker | Price Date | Days Old | Source |
|--------|------------|----------|--------|
| AGL.AX | 2026-02-17 | 0 | yfinance |
| AGVT.AX | 2026-02-17 | 0 | yfinance |
| BHP.AX | 2026-02-17 | 0 | yfinance |
| CRED.AX | 2026-02-17 | 0 | yfinance |
| FLBL | 2026-02-13 | 4 | yfinance |
| GHY.AX | 2026-02-17 | 0 | yfinance |
| GSBG27.AX | 2026-02-17 | 0 | yfinance |
| GSBG33.AX | 2026-02-17 | 0 | yfinance |
| JPST | 2026-02-13 | 4 | yfinance |
| ORG.AX | 2026-02-17 | 0 | yfinance |
| SOL.AX | 2026-02-17 | 0 | yfinance |
| TCPC | 2026-02-13 | 4 | yfinance |
| UKW | 2026-02-16 | 1 | yfinance |

**Data Freshness:** Most prices are current (0-1 days old). FLBL, JPST, and TCPC prices are 4 days old (from 2026-02-13). These are US-listed instruments; prices may be stale if markets were closed. No action required unless prices remain stale >5 trading days.

### Monthly Expenses Assumption

- **Assumed:** AUD 9,000/month
- **24-month floor:** AUD 216,000
- **Current stabiliser:** AUD 1,032,392 (114.7 months coverage)

### Classification Status

All instruments are classified with roles, macro drivers, corporate groups, and correlation groups per the classification recommendations document. GHY.AX requires convexity flags to pass Rule 6.1.

---

**Report Generated:** 2026-02-17  
**Portfolio Value:** AUD 1,841,081.67  
**Compliance:** 9 pass, 4 warning, 3 breach
