# Recommendation Report v3 — 2026-02-18

Supersedes `initial-recommendation-report-260218_0947.md` (v2). Changes from v2 are documented at the end.

All monetary values are in **AUD** unless stated otherwise.

---

## Rule 9.2 Gate

| Check | Result |
|-------|--------|
| Breaches exist? | **Yes** — 4 active (see below) |
| Active triggers? | No |
| Action required? | **Yes** — mandatory rebalance within 30 days |

---

## Current Compliance Summary

| Rule | Status | Detail |
|------|--------|--------|
| [D.1] Data Freshness | ✓ Pass | All prices ≤7 days old |
| [2.1] Income Substitution | ✓ Pass | 108.1 months coverage |
| [1.1-S] Stabiliser Band | ⚠ Warning | 54.6% (target 15–25%) |
| **[1.1-C] Compounder Band** | **✗ Breach** | 45.0% (min 50%) |
| [1.1-O] Optionality Band | ⚠ Warning | 0.4% (target 10–20%) |
| [2.2] Income Shock | ✓ Pass | Not active |
| **[3.1-cr] FLBL Credit Cap** | **✗ Breach** | 13.4% (max 7%) |
| **[3.1-cr] CRED.AX Credit Cap** | **✗ Breach** | 7.1% (max 7%) |
| **[6.1] Convexity Test** | **✗ Breach** | GHY.AX 0/3 — missing database flags |
| [4.1] Australia Concentration | ✓ Pass | 31.4% (max 55%) |
| [4.2] Macro Driver Exposure | ✓ Pass | Highest: global_credit_spreads 23.6% |
| [5.1] AUD Growth Exposure | ✓ Pass | 57.3% (target 50–70%) |
| [5.2] Hedging Rule | ✓ Pass | 100% unhedged |
| [7.1] Stabiliser Liquidity | ✓ Pass | 100% liquid ≤5 days |
| [7.3] Inflation Coverage | ⚠ Warning | 0% inflation-linked (target ≥25%) |
| [8.1] Drawdown Tolerance | ✓ Pass | Stabiliser covers 24mo after 35% drawdown |
| [8.2] Stress Correlation | ⚠ Warning | Credit spread group 23.6% |
| [9.2] No Action Rule | ✓ Pass | No triggers (breaches override) |

**Active breaches (4):**
1. [1.1-C] Compounder below 50%
2. [3.1-cr] FLBL at 13.4% exceeds 7% credit cap
3. [3.1-cr] CRED.AX at 7.1% exceeds 7% credit cap
4. [6.1] GHY.AX convexity flags missing

---

## Dollar Gap Analysis

| Dimension | Current | Target | Gap |
|-----------|--------:|-------:|----:|
| Stabiliser | 973,084 (54.6%) | ~445,000 (25.0%) | -528,084 over |
| Compounder | 801,405 (45.0%) | ~1,158,000 (65.0%) | +356,595 under |
| Optionality | 7,285 (0.4%) | ~178,000 (10.0%) | +170,715 under |
| FLBL | 239,018 (13.4%) | 115,815 (6.5%) | -123,203 over |
| CRED.AX | 126,861 (7.1%) | 115,815 (6.5%) | -11,046 over |
| Inflation-linked stabiliser | 0% | ≥25% of ~445k = ~111k | +111,000 |

---

## Design Constraints

Three hard constraints pin this allocation at S 25% / C 65% / O 10%:

1. **GSBG27 duration (Rule 7.2):** GSBG27 ($178,120) must be ≤40% of stabiliser, so minimum stabiliser = $178,120 / 0.40 = $445,300 = 25.0% of portfolio. Reaching 20% ($356k) would require selling ~$36k of a government bond that matures in 14 months — unnecessary transaction cost for a small gain. The right path is to accept 25% now: when GSBG27 matures (April 2027), $178k flows to cash, the constraint disappears, and stabiliser can be reduced to 18–20% with proceeds redeployed to compounders/optionality. The principle that 25% is more stabiliser than the objectives require is correct; the constraint is mechanical, not strategic.

2. **Compounder maximum (Rule 1.1):** The band ceiling is 65%. Maximising compounder allocation maximises expected risk-adjusted returns per the project objective.

3. **Optionality instrument constraint (Rule 0.1 + 6.1):** Under the long-only, non-derivative instrument universe, gold is the only scalable instrument that credibly passes Rule 6.1 criterion 3 (stress-period outperformance). With PMGOLD at 9.6% (buffer against 10% cap), optionality reaches 10.0%. Higher optionality would require instruments that don't exist within Rule 0.1.

Given these constraints, the three roles sum to 100% with no remaining slack.

---

## Recommendations

### Rec 1: Trim FLBL to 6.5%

- **Type**: Sell (partial)
- **Amount**: ~AUD 123,000 (USD ~87,000)
- **Post-trade**: AUD 115,815 (6.5%)
- **Role**: Compounder — proceeds redeployed to new compounders
- **Rules addressed**: [3.1-cr] credit cap breach; reduces credit spread cluster from 23.6% to 16.1%; reduces [4.2] global_credit_spreads
- **Buffer**: 0.5pp to 7% cap. FLBL must rally 8% (rest flat) to breach. Under the v2 recommendation (7.0%, 0pp buffer), any price appreciation created an immediate Rule 9.1 trigger — incompatible with the "no discretionary rebalancing" philosophy (Rule 9.2).
- **Risk note**: Larger trim than v2. Reduces income (FLBL yields ~8–9%). Acceptable: credit spread concentration was the portfolio's largest single-instrument risk.

### Rec 2: Trim CRED.AX to 6.5%

- **Type**: Sell (partial)
- **Amount**: ~AUD 11,000
- **Post-trade**: AUD 115,815 (6.5%)
- **Role**: Compounder
- **Rules addressed**: [3.1-cr] credit cap breach
- **Buffer**: 0.5pp to 7% cap. Same rationale as Rec 1.

### Rec 3: Swap Nominal Stabiliser for Inflation-Linked

- **Type**: Sell AGVT.AX (full, ~AUD 95,000) + Trim JPST (~AUD 22,000) → Buy Treasury Indexed Bonds (~AUD 114,000)
- **Role**: Stabiliser internal rebalance — no role change
- **Rules addressed**: [7.3] inflation coverage (0% → ~25.6%)
- **Instrument**: ASX-listed Treasury Indexed Bonds (GSBI series), maturities 2027–2033 to match stabiliser horizon. If direct TIBs are illiquid, an inflation-linked government bond ETF is an alternative.
- **Why sell AGVT.AX**: Nominal government bonds — no inflation protection. Same credit quality as GSBI (both AU Government). Overlaps GSBG27/GSBG33.
- **Why trim JPST**: Reduces USD currency mismatch within stabiliser. Post-trim JPST remains ~AUD 100,000 (still provides USD liquidity).
- **Constraint check**: AU Government group rises from 17.3% to 18.4% — under 20% cap (1.6pp buffer).

### Rec 4: Buy VAS.AX (Vanguard Australian Shares Index ETF)

- **Type**: Buy (new position)
- **Amount**: AUD 169,000
- **Role**: Compounder
- **Rules addressed**: [1.1-C] compounder below 50%; [1.1-S] stabiliser overweight
- **Position**: 9.5% — 0.5pp buffer to 10% equity cap. VAS must rally 6% (rest flat) to breach.
- **Rationale**: Broad exposure to ~300 ASX-listed stocks (0.07% MER). Diversifies domestic equity beyond four individual names.
- **Look-through note**: BHP is ~10% of the ASX300 index. VAS at 9.5% adds ~0.95% effective BHP exposure, putting total economic BHP at ~10.5%. This exceeds the 10% cap in look-through terms. Accepted as inherent to holding a broad index alongside direct names — the diversification benefit outweighs the look-through overlap. Same applies at smaller scale to SOL (~3% of index), AGL (~0.7%), ORG (~0.3%).

### Rec 5: Buy VGS.AX (Vanguard MSCI Index International Shares ETF)

- **Type**: Buy (new position)
- **Amount**: AUD 160,000
- **Role**: Compounder
- **Rules addressed**: [1.1-C]; [1.1-S]
- **Position**: 9.0% — 1.0pp buffer to 10% equity cap. VGS must rally 12% (rest flat) to breach.
- **Currency (Rule 5.1)**: Non-AUD — tracks international equities ex-Australia.
- **Rationale**: ~1,500 international developed-market stocks (0.18% MER). Portfolio currently lacks diversified international equity. Strategy §3 calls for "diversified global equity exposure."

### Rec 6: Buy VGE.AX (Vanguard FTSE Emerging Markets Shares ETF)

- **Type**: Buy (new position)
- **Amount**: AUD 83,000
- **Role**: Compounder
- **Rules addressed**: [1.1-C]; [1.1-S]
- **Position**: 4.7% — within 10% equity cap with 5.3pp buffer.
- **Currency (Rule 5.1)**: Non-AUD.
- **Rationale**: Adds emerging market exposure (absent from portfolio). China ~30%, India ~20%, Taiwan ~17%. Tracks real businesses in economies with structural growth drivers (demographics, urbanisation, rising middle class) — a genuine compounder per Strategy §3. Macro drivers (china_demand, emerging_markets) are distinct from everything else in the portfolio.

### Rec 7: Top Up SOL.AX

- **Type**: Buy (add to existing position)
- **Amount**: AUD 78,000
- **Post-trade**: AUD 152,216 (8.5%)
- **Role**: Compounder
- **Rules addressed**: [5.1] AUD growth; fills compounder to 65% target
- **Buffer**: 1.5pp to 10% equity cap.
- **Rationale**: SOL.AX (Washington H Soul Pattinson) is a diversified Australian investment conglomerate. Larger top-up than v2 (+$78k vs +$35k) serves two purposes: (a) fills the compounder bucket to 65% (maximum allowed, objective-maximising), and (b) provides a 2.4pp buffer on AUD growth (52.4% vs 50% floor), up from v2's 0.4pp. SOL is diversified across coal, banking, telecoms, and building materials — the conglomerate structure makes a larger position more defensible than a pure-play single sector.

### Rec 8: Buy PMGOLD.AX (Perth Mint Gold ETF)

- **Type**: Buy (new position)
- **Amount**: AUD 171,000
- **Role**: Optionality
- **Rules addressed**: [1.1-O] optionality below 10%
- **Rule 6.1 scoring** (under amended Rule 6.1):
  - Criterion 1 (bounded downside): ✓ — auto-satisfied under Rule 0.1.
  - Criterion 3 (stress-period outperformance): ✓ — gold rallied in 2008 GFC (+26%), 2020 COVID (initial -7% then +31%), 2011 European crisis. Consistent negative/zero correlation to equity beta in severe stress across multiple regimes.
  - **Score: 2/3 — passes.**
- **Currency (Rule 5.1)**: Non-AUD — gold is priced in USD globally.
- **Position**: 9.6% — 0.4pp buffer to 10% equity cap. PMGOLD must rally 5% (rest flat) to breach.
- **Honest characterisation**: Gold is **regime insurance and crisis diversifier**, not a convex payoff in the options-theory sense. Under Rule 0.1 constraints (no derivatives, no leverage), truly convex instruments are not available at scale. Gold is the best available proxy for crisis alpha within the instrument universe. The optionality bucket at 10% reflects this limitation — sizing is at the band floor, not the midpoint, because the available instruments only partially deliver the bucket's theoretical promise.

### ~~Rec 9: ETPMAG.AX — removed~~

Silver was in v2 as optionality (scored 2/3 on Rule 6.1) and in an earlier v3 draft as compounder ("real-asset growth bet"). Neither classification holds. Silver fails Rule 6.1 criterion 3 (falls 33–55% in acute crises), and the strategy defines compounders as "durable, high-ROIC businesses and diversified global equity exposure" — silver is none of those. At 1.7%, even excellent performance is immaterial to a $1.78M portfolio, but the position adds monitoring overhead and relies on a commodity proxy that the report's own limitations section identifies as dramatically wrong for silver. The $30k is redeployed to VGE (Rec 6), taking emerging markets from 3.0% to 4.7% — a genuine compounder with distinct macro drivers.

### Rec 9: Set GHY.AX Convexity Flags

- **Type**: Database update (no trade)
- **Rules addressed**: [6.1] convexity test
- **Scoring**: Criterion 1 ✓ (auto under Rule 0.1) + Criterion 2 ✓ (pre-revenue hydrogen exploration; binary outcome with many-x upside if successful). Score: 2/3.
- **Action**: Set `nonlinear_upside=true` for GHY.AX. Set `stress_outperformance=true` for PMGOLD.AX.

---

## Post-Trade Projection

### Role Allocation

| Role | Before | Before % | After | After % | Band | Status |
|------|-------:|---------:|------:|--------:|------|--------|
| Stabiliser | 973,084 | 54.6% | 445,444 | 25.0% | 15–25% | ✓ |
| Compounder | 801,405 | 45.0% | 1,158,153 | 65.0% | 50–65% | ✓ |
| Optionality | 7,285 | 0.4% | 178,177 | 10.0% | 10–20% | ✓ |

### All Positions After Trades

**Stabiliser:**

| Instrument | AUD | % Portfolio | Notes |
|------------|----:|-------------|-------|
| GSBG27.AX | 178,120 | 10.0% | Govt bond, matures Apr 2027 |
| GSBI (new) | 114,000 | 6.4% | Inflation-linked govt bond |
| JPST (trimmed) | 100,000 | 5.6% | USD ultra-short ETF |
| GSBG33.AX | 35,448 | 2.0% | Govt bond, matures Apr 2033 |
| Cash | 17,876 | 1.0% | Multi-currency |
| **Stabiliser total** | **445,444** | **25.0%** | |

**Compounder:**

| Instrument | AUD | % Portfolio | Cap | Notes |
|------------|----:|-------------|-----|-------|
| VAS.AX (new) | 169,268 | 9.5% | 10% eq | Broad AU equity |
| BHP.AX | 169,696 | 9.5% | 10% eq | Diversified miner |
| VGS.AX (new) | 160,360 | 9.0% | 10% eq | Broad intl equity |
| SOL.AX (topped up) | 152,216 | 8.5% | 10% eq | AU conglomerate |
| FLBL (trimmed) | 115,815 | 6.5% | **7% cr** | US senior loans |
| CRED.AX (trimmed) | 115,815 | 6.5% | **7% cr** | AU IG corporate bonds |
| VGE.AX (new) | 83,453 | 4.7% | 10% eq | Emerging markets |
| AGL.AX | 67,727 | 3.8% | 10% eq | AU energy utility |
| TCPC | 54,405 | 3.1% | **7% cr** | US BDC / private credit |
| UKW | 51,757 | 2.9% | 10% eq | UK wind infrastructure |
| ORG.AX | 17,640 | 1.0% | 10% eq | AU energy |
| **Compounder total** | **1,158,153** | **65.0%** | | |

**Optionality:**

| Instrument | AUD | % Portfolio | Cap | 6.1 Score |
|------------|----:|-------------|-----|-----------|
| PMGOLD.AX (new) | 170,892 | 9.6% | 10% eq | 2/3 (crit 1 + 3) |
| GHY.AX | 7,285 | 0.4% | 1% spec | 2/3 (crit 1 + 2) |
| **Optionality total** | **178,177** | **10.0%** | | |

### Breach Resolution

| Rule | Before | After | Resolved? |
|------|--------|-------|-----------|
| [1.1-C] Compounder ≥50% | 45.0% ✗ | 65.0% | ✓ |
| [3.1-cr] FLBL ≤7% | 13.4% ✗ | 6.5% | ✓ |
| [3.1-cr] CRED ≤7% | 7.1% ✗ | 6.5% | ✓ |
| [6.1] GHY convexity | 0/3 ✗ | 2/3 (flag fix) | ✓ |

### Warning Resolution

| Rule | Before | After | Status |
|------|--------|-------|--------|
| [1.1-S] Stabiliser ≤25% | 54.6% | 25.0% | ✓ Resolved |
| [1.1-O] Optionality ≥10% | 0.4% | 10.0% | ✓ Resolved (at floor) |
| [7.3] Inflation coverage ≥25% | 0% | ~25.6% | ✓ Resolved |
| [8.2] Credit spread cluster | 23.6% | 16.1% | ✓ Reduced |

---

## Validation Against All Rules

| Rule | Post-Trade | Detail |
|------|------------|--------|
| [0.1] Instrument Universe | ✓ | All instruments are long-only, non-leveraged, non-derivative, publicly listed |
| [1.1-S] Stabiliser | ✓ | 25.0% (15–25%) |
| [1.1-C] Compounder | ✓ | 65.0% (50–65%) |
| [1.1-O] Optionality | ✓ | 10.0% (10–20%) — at floor; see Design Constraints |
| [2.1] Income Substitution | ✓ | 445,444 / 9,000 = 49.5 months (≥24) |
| [2.2] Income Shock | ✓ | Not active |
| [3.1] Equity caps | ✓ | Largest: VAS 9.5%, BHP 9.5%, VGS 9.0%, PMGOLD 9.6% — all ≤10% |
| [3.1] Credit caps | ✓ | FLBL 6.5%, CRED 6.5%, TCPC 3.1% — all ≤7% |
| [3.1] Speculative caps | ✓ | GHY 0.4% (≤1% each, ≤3% agg) |
| [3.2] Issuer concentration | ✓ | Largest: AU Government 18.4% (≤20%) |
| [4.1] AU concentration | ✓ | AUD risk assets ~39% (≤55%) |
| [4.2] Macro drivers | ✓ | Largest: global_credit_spreads 16.1% (≤30%). All named drivers under 30%. |
| [5.1] AUD growth | ✓ | **52.4%** (50–70%). 2.4pp buffer above floor. |
| [5.2] Hedging | ✓ | 100% international growth unhedged (≥40%) |
| [6.1] Convexity | ✓ | PMGOLD 2/3, GHY 2/3. |
| [7.1] Stabiliser liquidity | ✓ | 100% liquid ≤5 days |
| [7.2] Stabiliser duration | ✓ | **GSBG27 = 40.0%** of stabiliser (≤40%). Pinned — see Design Constraints. |
| [7.3] Inflation coverage | ✓ | GSBI ~114,000 / 445,444 = 25.6% (≥25%) |
| [8.1] Drawdown tolerance | ✓ | After 35% equity drawdown, stabiliser 445,444 still covers 24 months (216,000) |
| [8.2] Stress correlation | ⚠ Monitor | Credit spread group: CRED+FLBL+TCPC = 286k = 16.1%. AU equity beta: BHP+SOL+AGL+ORG+VAS = ~576k = 32.3% — largest stress-correlated cluster. Precious metals: PMGOLD = 171k = 9.6%. Emerging equity: VGE = 83k = 4.7%. |
| [9.2] No action rule | ✓ | Breaches justify action; no discretionary triggers needed |

**Post-trade rule buffers (from `towsand sensitivity --trades`):**

| Constraint | Value | Limit | Buffer | Move to breach |
|------------|------:|------:|-------:|----------------|
| GSBG27 % of stabiliser (Rule 7.2) | 40.0% | 40% | 0.0pp | Other stabiliser assets decline |
| PMGOLD % of portfolio (Rule 3.1-eq) | 9.6% | 10% | 0.4pp | PMGOLD rallies 5% |
| BHP % of portfolio (Rule 3.1-eq) | 9.5% | 10% | 0.5pp | BHP rallies 6% |
| FLBL % of portfolio (Rule 3.1-cr) | 6.5% | 7% | 0.5pp | FLBL rallies 8% |
| CRED % of portfolio (Rule 3.1-cr) | 6.5% | 7% | 0.5pp | CRED rallies 8% |
| VAS % of portfolio (Rule 3.1-eq) | 9.5% | 10% | 0.5pp | VAS rallies 6% |
| VGS % of portfolio (Rule 3.1-eq) | 9.0% | 10% | 1.0pp | VGS rallies 12% |
| SOL % of portfolio (Rule 3.1-eq) | 8.5% | 10% | 1.5pp | SOL rallies 19% |
| AU Government group (Rule 3.2) | 18.4% | 20% | 1.6pp | Group outperforms rest |
| AUD growth floor (Rule 5.1) | 52.4% | 50% | 2.4pp | Non-AUD rallies 9.9% |

**Compared to v2 buffers:**

| Constraint | v2 Buffer | v3 Buffer | Change |
|------------|-----------|-----------|--------|
| FLBL credit cap | 0.0pp | 0.5pp | +0.5 |
| CRED credit cap | 0.0pp | 0.5pp | +0.5 |
| VAS equity cap | 0.1pp | 0.5pp | +0.4 |
| VGS equity cap | 0.2pp | 1.0pp | +0.8 |
| PMGOLD equity cap | 0.2pp | 0.4pp | +0.2 |
| AUD growth floor | 0.4pp | 2.4pp | +2.0 |
| Stabiliser band | -0.1pp (breaching) | 0.0pp | +0.1 |

---

## Trade Summary

| # | Action | Instrument | Direction | ~AUD Amount | Ccy | Market |
|---|--------|------------|-----------|----------:|-----|--------|
| 1 | Full sell | AGVT.AX | Sell | 95,473 | AUD | ASX (IB) |
| 2 | Trim | FLBL | Sell | 123,203 | USD | US (IB) |
| 3 | Trim | CRED.AX | Sell | 11,046 | AUD | ASX (IB) |
| 4 | Trim | JPST | Sell | 22,138 | USD | US (IB) |
| 5 | New buy | GSBI (TIBs) | Buy | 114,000 | AUD | ASX |
| 6 | New buy | VAS.AX | Buy | 169,268 | AUD | ASX (IB) |
| 7 | New buy | VGS.AX | Buy | 160,360 | AUD | ASX (IB) |
| 8 | Top up | SOL.AX | Buy | 77,917 | AUD | ASX (IB) |
| 9 | New buy | VGE.AX | Buy | 83,453 | AUD | ASX (IB) |
| 10 | New buy | PMGOLD.AX | Buy | 170,892 | AUD | ASX (IB) |
| 11 | DB fix | GHY.AX | Classify | 0 | — | — |

**Sell proceeds**: ~AUD 252,000
**Buy total**: ~AUD 776,000
**Net cash deployed from stabiliser**: ~AUD 524,000

### Execution Sequence

**Day 1 — Sells:**
1. Sell AGVT.AX (full, ASX — liquid, same-day fill)
2. Trim CRED.AX (~AUD 11k, ASX)
3. Trim FLBL (~USD 87k, US market)
4. Trim JPST (~USD 16k, US market)

**Day 2–3 — FX + Transfers:**
- Convert ~USD 299k → AUD on IB (needed for ASX purchases)
- Transfer ~AUD 95k from RACQ to IB (AUD shortfall coverage)

**Day 3–7 — Buys (use limit orders):**
- VAS.AX, VGS.AX (large, liquid ASX ETFs — high daily volume)
- SOL.AX top-up (liquid ASX equity)
- PMGOLD.AX (liquid ASX ETF)
- GSBI (direct bonds — check ASX order book, patient limit orders; OR buy via CommSec alongside existing govt bonds)

**Day 7–10 — Smaller buys:**
- VGE.AX (smaller position, adequate liquidity)

**Anytime — Database fix:**
- GHY.AX: `nonlinear_upside=true`
- PMGOLD.AX: `stress_outperformance=true`

### Tax Flags

| Trade | Tax event? | Note |
|-------|-----------|------|
| Sell AGVT.AX | Yes | CGT on disposal. Check cost base. |
| Trim FLBL | Yes | Partial disposal — CGT + potential FX gain/loss (USD). |
| Trim JPST | Yes | Partial disposal — CGT + potential FX gain/loss (USD). |
| Trim CRED.AX | Yes | Partial disposal — small amount. |
| All buys | No | |

User should assess CGT impact before executing.

### Classification Commands (post-purchase)

```bash
# New compounders
towsand classify role VAS.AX compounder
towsand classify role VGS.AX compounder
towsand classify role VGE.AX compounder

towsand classify tag VAS.AX \
  --macro "au_domestic_demand,au_equity_market" \
  --group "Vanguard AU Shares" \
  --corr-group "au_equity_beta" \
  --duration 0 --liquidity 1 --no-inflation-linked

towsand classify tag VGS.AX \
  --macro "global_developed_equity" \
  --group "Vanguard Intl Shares" \
  --corr-group "global_equity_beta" \
  --duration 0 --liquidity 1 --no-inflation-linked --unhedged

towsand classify tag VGE.AX \
  --macro "china_demand,emerging_markets" \
  --group "Vanguard Emerging Mkts" \
  --corr-group "emerging_equity_beta" \
  --duration 0 --liquidity 1 --no-inflation-linked --unhedged

# New optionality
towsand classify role PMGOLD.AX optionality

towsand classify tag PMGOLD.AX \
  --macro "gold_price" \
  --group "Perth Mint Gold" \
  --corr-group "precious_metals" \
  --duration 0 --liquidity 1 --no-inflation-linked --unhedged

# New stabiliser (inflation-linked)
towsand classify role GSBI stabiliser
towsand classify tag GSBI \
  --macro "au_interest_rates" \
  --group "AU Government" \
  --corr-group "au_govt_bond" \
  --duration 5.0 --liquidity 2 --inflation-linked

# GHY.AX convexity fix
# Set nonlinear_upside=true (criterion 2)
# Set stress_outperformance=true for PMGOLD.AX (criterion 3)
```

**Additional: asset_class and economic_currency** (requires direct SQL or CLI extension — the `classify tag` command does not currently support these fields):

```sql
-- New instruments: set asset_class and economic_currency
UPDATE instrument_classifications SET
  asset_class = 'equity', economic_currency = 'AUD'
WHERE instrument_id = (SELECT id FROM instruments WHERE ticker = 'VAS.AX');

UPDATE instrument_classifications SET
  asset_class = 'equity', economic_currency = 'USD'
WHERE instrument_id = (SELECT id FROM instruments WHERE ticker = 'VGS.AX');

UPDATE instrument_classifications SET
  asset_class = 'equity', economic_currency = 'USD'
WHERE instrument_id = (SELECT id FROM instruments WHERE ticker = 'VGE.AX');

UPDATE instrument_classifications SET
  asset_class = 'commodity', economic_currency = 'USD'
WHERE instrument_id = (SELECT id FROM instruments WHERE ticker = 'PMGOLD.AX');

UPDATE instrument_classifications SET
  asset_class = 'govt_bond_indexed', economic_currency = 'AUD'
WHERE instrument_id = (SELECT id FROM instruments WHERE ticker = 'GSBI');
```

**Implementation note**: The `classify tag` CLI should be extended to support `--asset-class` and `--economic-currency` flags. Without these fields set, compliance falls back to `instrument_type` (wrong caps for commodity ETPs) and `currency` (wrong AUD/non-AUD classification for PMGOLD). This is a code improvement item.

---

## Changes from v2

| Issue | v2 | v3 |
|-------|----|----|
| Stabiliser % | 25.1% (**above** 25% max — compliance error) | **25.0%** (inside band) |
| Compounder % | 63.0% | **65.0%** (maximum allowed — objective-maximising) |
| Optionality % | 11.9% | **10.0%** (honest about instrument limitations) |
| FLBL target | 7.0% (0pp buffer) | **6.5%** (0.5pp buffer) |
| CRED target | 7.0% (0pp buffer) | **6.5%** (0.5pp buffer) |
| VAS target | 9.9% (0.1pp buffer) | **9.5%** (0.5pp buffer) |
| VGS target | 9.8% (0.2pp buffer) | **9.0%** (1.0pp buffer) |
| PMGOLD target | 9.8% (0.2pp buffer) | **9.6%** (0.4pp buffer) |
| SOL target | 6.1% (+$35k top-up) | **8.5%** (+$78k top-up — fills compounder + AUD buffer) |
| ETPMAG | Optionality (scored 2/3 on 6.1) | **Removed** — fails both optionality (6.1) and compounder (not a business). $30k redeployed to VGE. |
| AUD growth buffer | 0.4pp | **2.4pp** |
| Inflation coverage | ~24.9% (below 25% target) | **25.6%** (above target) |
| Optionality characterisation | "Optionality" | **"Regime insurance / crisis diversifier"** within Rule 0.1 constraints |
| Classification commands | Missing asset_class, economic_currency | **Included** (SQL statements) |
| Design constraints | Not explained | **Explicit** — GSBG27 pins stabiliser, S+C+O must sum to 100% |
| VGE size | 3.0% ($53k) | **4.7%** ($83k) — absorbed ETPMAG's $30k |
| Trade count | 12 (11 trades + 1 DB fix) | **11** (10 trades + 1 DB fix) |

---

## Appendix A: Objective-Level Sensitivity

*Generated by `towsand sensitivity --trades data/trades-v3.json`.*

### Pre-Trade Portfolio (Current)

| Objective | Severity | Finding |
|-----------|----------|---------|
| **Income Bridge** | SAFE | Covers 108 months (84 months excess). Cash alone (AUD 541,906) exceeds the 24-month floor. |
| **Forced Liquidation** | SAFE | Stabiliser excess of AUD 757,084 (42.5% of portfolio). |
| **Compounding Capital** | FRAGILE | Compounder capital only AUD 801,405 (45%). A 35% drawdown destroys AUD 280,492 and costs 6.8 years of recovery. |
| **AUD Liability Matching** | SAFE | AUD growth at 57.3%. A 34.3% rally in non-AUD needed to breach 50%. |
| **Optionality as Crisis Insurance** | CRITICAL | At 0.4% (AUD 7,285), optionality is decorative. Even a 100% gain adds only AUD 7,285. |

### Post-Trade Portfolio (Projected)

| Objective | Severity | Finding |
|-----------|----------|---------|
| **Income Bridge** | SAFE | Post-trade stabiliser AUD 445,444 = 49 months. 25 months excess over the 24-month floor. A 54% decline in stabiliser holdings needed to break it. |
| **Forced Liquidation** | WATCH | Stabiliser excess AUD 229,444 (12.9%). Adequate but no longer fortress-like. |
| **Compounding Capital** | SAFE | Compounder rises to AUD 1,158,153 (65.0%). A 35% drawdown costs AUD 405,353 — more dollars at risk, but from a stronger base. Recovery: 6.8 years. |
| **AUD Liability Matching** | WATCH | AUD growth at 52.4%. A 9.9% rally in non-AUD growth weakens below 50%. Improved from v2's 50.4% (1.7% trigger). |
| **Optionality as Crisis Insurance** | FRAGILE | At 10.0% (AUD 178,177). Gold-only at scale — regime insurance, not convex payoff. Performs its designed function in proxy stress scenarios. |

---

## Appendix B: Stress Scenario Impact on Objectives

*Generated by `towsand stress --trades data/trades-v3.json --detail`.*

**Data source transparency:** COVID-2020 and GFC-2008 scenarios use **asset-class proxy drawdowns for all holdings** (no actual price data for those periods). The 2022 Rate Shock uses actual historical drawdowns for 11 of 17 post-trade holdings.

### Pre-Trade vs Post-Trade Comparison

| Scenario | | Wealth Lost | Comp. Destroyed | Recovery | Forced Sell? |
|----------|-|----------:|----------------:|---------:|-------------|
| **Flat 35% Haircut** | Pre | AUD 283,042 | AUD 280,492 | 6.8 yrs | No |
| | **Post** | **AUD 467,716** | **AUD 405,353** | **6.8 yrs** | **No** |
| | Delta | +184,674 | +124,862 | 0.0 | |
| **COVID-19 2020** ⚠ | Pre | AUD 188,849 | AUD 191,259 | 4.3 yrs | No |
| | **Post** | **AUD 359,338** | **AUD 342,971** | **5.6 yrs** | **No** |
| | Delta | +170,489 | +151,712 | +1.3 | |
| **GFC 2008** ⚠ | Pre | AUD 301,041 | AUD 327,938 | 8.4 yrs | No |
| | **Post** | **AUD 526,117** | **AUD 557,712** | **10.4 yrs** | **No** |
| | Delta | +225,076 | +229,774 | +2.0 | |
| **2022 Rate Shock** | Pre | AUD 38,000 | gained 7,343 | 0 yrs | No |
| | **Post** | **AUD 126,776** | **AUD 93,814** | **1.3 yrs** | **No** |
| | Delta | +88,776 | +101,157 | +1.3 | |

*⚠ = all-proxy scenario. Treat as indicative.*

### Post-Trade Objective Assessment by Scenario

**1. SURVIVABILITY: Pass in all scenarios.** Post-trade stabiliser AUD 445,444 covers 45–53 months under the worst stress. No forced liquidation.

**2. INCOME BRIDGE: Intact but thinner.** Worst case post-trade (2022 rate shock): 45 months. 21 months above the 24-month floor.

**3. COMPOUNDING: More capital at risk, by design.** Post-trade GFC (proxy) destroys AUD 558k vs pre-trade AUD 328k. But the post-trade has AUD 1,158k compounding vs pre-trade AUD 801k. Percentage loss is similar (~48% vs ~41%).

**4. OPTIONALITY PERFORMANCE:**
- COVID proxy: optionality lost 11% (PMGOLD at -10% commodity proxy) vs compounders' 30%. **Performed** — crisis insurance function activated.
- GFC proxy: optionality **gained** 3% (PMGOLD at +5% commodity proxy) vs compounders' 48% loss. **Performed**.
- 2022 Rate Shock: optionality **gained** 4% vs compounders' 8% loss. **Performed**.
- Flat 35%: optionality lost 35% (synthetic uniform hit). Did not perform — by design, this synthetic worst-case hits everything equally.

**5. 2022 RATE SHOCK remains the most informative scenario** (mostly historical data). Post-trade loss: AUD 127k. Optionality gained 4%.

---

## Appendix C: Diversification Quality

*Generated by `towsand correlations --detail`. Analysis uses current holdings only (5 years of daily prices, 55 stress trading days). New instruments (VAS, VGS, VGE, PMGOLD) have no price history in the database — post-trade diversification is not empirically validated.*

### Does Each Role Do Its Job?

| Question | Answer | Evidence |
|----------|--------|----------|
| **Does the stabiliser stabilise?** | Neutral — diversifies but doesn't actively offset. | Stabiliser–compounder stress correlation: 0.12. |
| **Does optionality provide crisis alpha?** | Unknown — insufficient data. | Only 1 optionality instrument (GHY.AX, AUD 7,285). |
| **Are compounders genuinely diversified?** | **Yes — well-diversified.** | Average intra-compounder stress correlation: 0.08. Highest pair: BHP–ORG at 0.36. |

### Hidden Concentration Risk

| Pair | Tagged Groups | Stress Corr | Meaning |
|------|---------------|------------:|---------|
| **AGVT–CRED** | au_govt_bond / credit_spread | **0.86** | CRED behaves like a duration instrument in stress. They are effectively the same bet. |

**Post-trade implication:** AGVT is sold; replaced by GSBI (inflation-linked). If CRED and GSBI have similar stress correlation, the hidden duration overlap persists. Monitor after GSBI purchase.

---

## Known Limitations

1. **FX is not modeled in stress or correlation.** Correlations are computed on stored close prices without reconstructing AUD returns through historical FX. This understates the stabilising benefit of USD-denominated assets during AUD depreciation events (common in crises). The error is conservative — real AUD-adjusted diversification is likely better than modeled.

2. **The "commodity" proxy is coarse.** GFC proxy: commodity = +5%. Gold actually gained ~25% in the GFC. The proxy is directionally correct for gold but imprecise. With ETPMAG removed from the portfolio, the commodity proxy now applies only to PMGOLD, where the error is smaller and conservative (proxy understates gold's actual crisis performance).

3. **Post-trade correlation is not validated for new instruments.** The four largest new positions (VAS, VGS, VGE, PMGOLD) have no price history in the database. The diversification thesis for index ETFs is self-evident from their holdings, but empirical stress correlation will only be available after price history accumulates.

4. **GSBG27 duration constraint pins stabiliser at 25%.** This is a mechanical constraint (Rule 7.2) that resolves when GSBG27 matures in April 2027. At that point, ~$178k flows to cash, stabiliser can be reduced below 25%, and additional capital can be deployed to compounders or optionality.

5. **Optionality is structurally limited under Rule 0.1.** The long-only, non-derivative instrument universe prevents access to truly convex payoff instruments at scale. Gold is the best available crisis alpha proxy but is not a convex payoff in the options-theory sense. The 10% optionality floor is realistic; the 15–20% upper band requires instruments that don't currently exist within the rules.

---

## Forward-Looking Notes

1. **GSBG27.AX maturity (April 2027):** When GSBG27 matures (~AUD 178k → cash), Rule 7.2 pressure resolves and stabiliser flexibility returns. Redeploy maturity proceeds into additional compounders/optionality if stabiliser exceeds 25%, or into GSBI to maintain inflation coverage.

2. **Rule 5.1 buffer at 2.4pp:** Improved from v2's 0.4pp but still requires monitoring. If non-AUD positions (VGS, PMGOLD) appreciate faster than AUD positions, AUD growth could drift toward 50%. The larger SOL position (8.5%) provides the buffer. Monitor quarterly.

3. **Compliance system updates needed:**
   - Extend `classify tag` CLI to support `--asset-class` and `--economic-currency` flags
   - Implement Rule 0.1 auto-satisfaction of 6.1 criterion 1
   - Consider splitting commodity proxy into gold/precious vs industrial/base for future accuracy
   - Add post-trade compliance projection capability (`towsand compliance --trades`)

4. **GSBI selection:** Verify current ASX-listed Treasury Indexed Bond availability. Target maturities 2027–2033 matching stabiliser horizon.

---

**Report Generated:** 2026-02-18
**Trades file:** `data/trades-v3.json`
**Analytics:** Re-run with v3 trade parameters. Sensitivity and stress `--trades` provide pre/post comparison.
**Portfolio Value:** AUD 1,781,774.17
**Current Compliance:** 10 pass, 4 warning, 4 breach
**Post-Trade Compliance (projected):** All breaches resolved. Optionality at band floor (10.0%). GSBG27 duration at constraint limit (40.0%).
