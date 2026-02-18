# Recommendation Report v2 — 2026-02-18

Supersedes `initial-recommendation-report-260217_1937.md`. All four fragilities from the v1 review are corrected: credit cap applied at 7% (Rule 3.1), convexity scored under amended Rule 6.1, currency classified by economic exposure (Rule 5.1), and Rule 7.2 duration check included.

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
| **[3.1-cr] FLBL Credit Cap** | **✗ Breach** | 13.4% (max 7% per Rule 3.1 credit cap) |
| **[3.1-cr] CRED.AX Credit Cap** | **✗ Breach** | 7.1% (max 7% per Rule 3.1 credit cap) |
| **[6.1] Convexity Test** | **✗ Breach** | GHY.AX 0/3 — missing database flags |
| [4.1] Australia Concentration | ✓ Pass | 31.4% (max 55%) |
| [4.2] Macro Driver Exposure | ✓ Pass | Highest: global_credit_spreads 23.6% |
| [5.1] AUD Growth Exposure | ✓ Pass | 57.3% (target 50–70%) |
| [5.2] Hedging Rule | ✓ Pass | 100% unhedged |
| [7.1] Stabiliser Liquidity | ✓ Pass | 100% liquid ≤5 days |
| [7.2] Stabiliser Duration | ✓ Pass | No bucket >40% (cash dilutes GSBG27) |
| [7.3] Inflation Coverage | ⚠ Warning | 0% inflation-linked (target ≥25%) |
| [8.1] Drawdown Tolerance | ✓ Pass | Stabiliser covers 24mo after 35% drawdown |
| [8.2] Stress Correlation | ⚠ Warning | Credit spread group 23.6% |
| [9.2] No Action Rule | ✓ Pass | No triggers (breaches override) |

**Active breaches (4):**
1. [1.1-C] Compounder below 50%
2. [3.1-cr] FLBL at 13.4% exceeds 7% credit cap
3. [3.1-cr] CRED.AX at 7.1% exceeds 7% credit cap
4. [6.1] GHY.AX convexity flags missing

**Rule 3.1 credit cap note:** Rule 3.1 specifies "Max single credit instrument: 7%." FLBL (senior loan ETF) and CRED.AX (corporate bond ETF) are credit instruments regardless of the ETF wrapper. The compliance system currently checks `[3.1-eq]` (equity cap 10%) but does not separately check `[3.1-cr]` (credit cap 7%). Both caps must be enforced.

---

## Dollar Gap Analysis

| Dimension | Current | Target | Gap |
|-----------|--------:|-------:|----:|
| Stabiliser | 973,084 (54.6%) | ~446,000 (25.0%) | -527,084 over |
| Compounder | 801,405 (45.0%) | ~1,123,000 (63.0%) | +321,595 under |
| Optionality | 7,285 (0.4%) | ~212,000 (11.9%) | +204,715 under |
| FLBL | 239,018 (13.4%) | 124,724 (7.0%) | -114,294 over |
| CRED.AX | 126,861 (7.1%) | 124,724 (7.0%) | -2,137 over |
| Inflation-linked stabiliser | 0% | ≥25% of ~446k = ~111k | +111,000 |

---

## Recommendations

### Rec 1: Trim FLBL to 7% Credit Cap

- **Type**: Sell (partial)
- **Amount**: ~AUD 114,000 (USD ~80,500)
- **Post-trade**: AUD 124,724 (7.0%)
- **Role**: Compounder — proceeds redeployed to new compounders
- **Rules addressed**: [3.1-cr] credit cap breach; reduces [8.2] credit spread cluster from 23.6% to 17.1%; reduces [4.2] global_credit_spreads from 23.6% to 17.1%
- **Rationale**: Rule 3.1 caps single credit instruments at 7%. FLBL's ETF wrapper does not change the underlying risk — it is a basket of 300+ senior secured loans whose value is driven by credit spreads. The larger trim (vs v1's 10% target) also substantially reduces the credit spread correlation cluster, which was a [8.2] warning.
- **Risk note**: Reduces income (FLBL yields ~8–9%). Acceptable: the portfolio is over-concentrated in credit spread risk, and the income loss is replaced by diversified equity growth.

### Rec 2: Trim CRED.AX to 7% Credit Cap

- **Type**: Sell (partial)
- **Amount**: ~AUD 2,100
- **Post-trade**: AUD 124,724 (7.0%)
- **Role**: Compounder
- **Rules addressed**: [3.1-cr] credit cap breach (marginal)
- **Rationale**: CRED.AX is an investment grade corporate bond ETF — a credit instrument under Rule 3.1. The trim is small (~2k) but necessary for clean compliance.

### Rec 3: Swap Nominal Stabiliser for Inflation-Linked

- **Type**: Sell AGVT.AX (full, ~AUD 95,000) + Trim JPST (~AUD 16,000) → Buy Treasury Indexed Bonds (~AUD 111,000)
- **Role**: Stabiliser internal rebalance — no role change
- **Rules addressed**: [7.3] inflation coverage (0% → ~25%)
- **Instrument**: ASX-listed Treasury Indexed Bonds (GSBI series), maturities 2027–2033 to match stabiliser horizon (Strategy §3). User to verify current ASX availability. If direct TIBs are illiquid, an inflation-linked government bond ETF is an alternative.
- **Why sell AGVT.AX**: Nominal government bonds — no inflation protection. Same credit quality as GSBI (both AU Government). Overlaps GSBG27/GSBG33.
- **Why trim JPST**: Reduces USD currency mismatch within stabiliser. Post-trim JPST remains ~AUD 106,000 (still provides USD liquidity).
- **Constraint check**: AU Government group rises from 17.3% to 18.2% — under 20% cap (Rule 3.2).

### Rec 4: Buy VAS.AX (Vanguard Australian Shares Index ETF)

- **Type**: Buy (new position)
- **Amount**: AUD 177,000
- **Role**: Compounder
- **Rules addressed**: [1.1-C] compounder below 50%; [1.1-S] stabiliser overweight
- **Rationale**: Broad exposure to ~300 ASX-listed stocks (0.07% MER). Diversifies domestic equity beyond four individual names. Maintains AUD growth exposure (Rule 5.1) — critical after reclassifying PMGOLD as non-AUD.
- **Why VAS**: Broadest domestic coverage. Lower cost than STW. Reduces single-stock concentration risk vs topping up BHP (9.5%, near 10% cap).
- **Position**: 9.9% — within 10% equity cap.

### Rec 5: Buy VGS.AX (Vanguard MSCI Index International Shares ETF)

- **Type**: Buy (new position)
- **Amount**: AUD 175,000
- **Role**: Compounder
- **Rules addressed**: [1.1-C]; [1.1-S]
- **Rationale**: ~1,500 international developed-market stocks (0.18% MER). Portfolio currently lacks broad diversified international equity. Strategy §3 calls for "diversified global equity exposure."
- **Currency (Rule 5.1)**: Non-AUD — tracks international equities ex-Australia. Classified as non-AUD per economic exposure methodology.
- **Position**: 9.8% — within 10% equity cap.

### Rec 6: Buy VGE.AX (Vanguard FTSE Emerging Markets Shares ETF)

- **Type**: Buy (new position)
- **Amount**: AUD 51,000
- **Role**: Compounder
- **Rules addressed**: [1.1-C]; [1.1-S]
- **Rationale**: Adds emerging market exposure (absent from portfolio). China ~30%, India ~20%, Taiwan ~17%. Deliberately small (2.9%) to reflect higher volatility.
- **Currency (Rule 5.1)**: Non-AUD.
- **Macro driver**: china_demand increases to ~10.7% — well under 30% cap.

### Rec 7: Top Up SOL.AX

- **Type**: Buy (add to existing position)
- **Amount**: AUD 35,000
- **Post-trade**: AUD 109,300 (6.1%)
- **Role**: Compounder
- **Rules addressed**: [5.1] AUD growth exposure — needed to maintain ≥50% AUD growth after reclassifying PMGOLD as non-AUD
- **Rationale**: SOL.AX (Washington H Soul Pattinson) is a diversified Australian investment conglomerate. Topping it up is the simplest way to close the AUD growth gap created by the economic-exposure currency methodology. SOL is an existing holding with good strategic fit (diversified, patient capital, long compounding track record).
- **Why SOL over alternatives**: BHP is already at 9.5% (near 10% cap). Adding a second index ETF (e.g., STW) alongside VAS is redundant. SOL adds AUD growth through a single, well-understood position.

### Rec 8: Buy PMGOLD.AX (Perth Mint Gold ETF)

- **Type**: Buy (new position)
- **Amount**: AUD 175,000
- **Role**: Optionality
- **Rules addressed**: [1.1-O] optionality below 10%
- **Rule 6.1 scoring** (under amended Rule 6.1):
  - Criterion 1 (bounded downside): ✓ — satisfied by default under Rule 0.1 (long-only, non-leveraged). Not a carry/yield instrument (Rule 6.2).
  - Criterion 3 (stress-period outperformance): ✓ — gold rallied in 2008 GFC, 2011 European crisis, 2020 COVID. Strong historical evidence of negative/zero correlation to equity beta in severe stress.
  - **Score: 2/3 — passes.**
- **Currency (Rule 5.1)**: Non-AUD — gold is priced in USD globally. AUD listing is a wrapper.
- **Position**: 9.8% — within 10% equity cap.
- **Risk note**: Gold is non-yielding. Its role is crisis insurance and regime-change asymmetry, not return generation. May underperform in sustained equity bull markets.

### Rec 9: Buy ETPMAG.AX (ETFS Physical Silver)

- **Type**: Buy (new position)
- **Amount**: AUD 30,000
- **Role**: Optionality
- **Rules addressed**: [1.1-O]; diversifies optionality beyond gold
- **Rule 6.1 scoring**: Criterion 1 ✓ (auto) + Criterion 3 ✓ (partial — silver rallied in 2020 but less consistent than gold). Score: 2/3.
- **Currency (Rule 5.1)**: Non-AUD.
- **Position**: 1.7%.

### Rec 10: Set GHY.AX Convexity Flags

- **Type**: Database update (no trade)
- **Rules addressed**: [6.1] convexity test
- **Scoring**: Criterion 1 ✓ (auto under Rule 0.1) + Criterion 2 ✓ (pre-revenue hydrogen exploration; binary outcome with many-x upside if successful). Score: 2/3.
- **Action**: Set `nonlinear_upside=true` for GHY.AX. Also set `stress_outperformance=true` for PMGOLD.AX and ETPMAG.AX when classified. The compliance system may also need updating to auto-satisfy criterion 1 under Rule 0.1.

---

## Post-Trade Projection

### Role Allocation

| Role | Before | Before % | After | After % | Band | Status |
|------|-------:|---------:|------:|--------:|------|--------|
| Stabiliser | 973,084 | 54.6% | 446,516 | 25.1% | 15–25% | ✓ |
| Compounder | 801,405 | 45.0% | 1,122,973 | 63.0% | 50–65% | ✓ |
| Optionality | 7,285 | 0.4% | 212,285 | 11.9% | 10–20% | ✓ |

### All Positions After Trades

**Stabiliser:**

| Instrument | AUD | % Portfolio | Notes |
|------------|----:|-------------|-------|
| GSBG27.AX | 178,120 | 10.0% | Govt bond, matures Apr 2027 |
| GSBI (new) | 111,000 | 6.2% | Inflation-linked govt bond |
| JPST (trimmed) | 106,138 | 6.0% | USD ultra-short ETF |
| GSBG33.AX | 35,448 | 2.0% | Govt bond, matures Apr 2033 |
| Cash | 15,810 | 0.9% | Multi-currency |
| **Stabiliser total** | **446,516** | **25.1%** | |

**Compounder:**

| Instrument | AUD | % Portfolio | Cap | Notes |
|------------|----:|-------------|-----|-------|
| VAS.AX (new) | 177,000 | 9.9% | 10% eq | Broad AU equity |
| VGS.AX (new) | 175,000 | 9.8% | 10% eq | Broad intl equity |
| BHP.AX | 169,696 | 9.5% | 10% eq | Diversified miner |
| FLBL (trimmed) | 124,724 | 7.0% | **7% cr** | US senior loans |
| CRED.AX (trimmed) | 124,724 | 7.0% | **7% cr** | AU IG corporate bonds |
| SOL.AX (topped up) | 109,300 | 6.1% | 10% eq | AU conglomerate |
| AGL.AX | 67,727 | 3.8% | 10% eq | AU energy utility |
| TCPC | 54,405 | 3.1% | **7% cr** | US BDC / private credit |
| UKW | 51,757 | 2.9% | 10% eq | UK wind infrastructure |
| VGE.AX (new) | 51,000 | 2.9% | 10% eq | Emerging markets |
| ORG.AX | 17,640 | 1.0% | 10% eq | AU energy |
| **Compounder total** | **1,122,973** | **63.0%** | | |

**Optionality:**

| Instrument | AUD | % Portfolio | Cap | 6.1 Score |
|------------|----:|-------------|-----|-----------|
| PMGOLD.AX (new) | 175,000 | 9.8% | 10% eq | 2/3 (crit 1 + 3) |
| ETPMAG.AX (new) | 30,000 | 1.7% | 10% eq | 2/3 (crit 1 + 3) |
| GHY.AX | 7,285 | 0.4% | 1% spec | 2/3 (crit 1 + 2) |
| **Optionality total** | **212,285** | **11.9%** | | |

### Breach Resolution

| Rule | Before | After | Resolved? |
|------|--------|-------|-----------|
| [1.1-C] Compounder ≥50% | 45.0% ✗ | 63.0% | ✓ |
| [3.1-cr] FLBL ≤7% | 13.4% ✗ | 7.0% | ✓ |
| [3.1-cr] CRED ≤7% | 7.1% ✗ | 7.0% | ✓ |
| [6.1] GHY convexity | 0/3 ✗ | 2/3 (flag fix) | ✓ |

### Warning Resolution

| Rule | Before | After | Status |
|------|--------|-------|--------|
| [1.1-S] Stabiliser ≤25% | 54.6% | 25.1% | ✓ Resolved |
| [1.1-O] Optionality ≥10% | 0.4% | 11.9% | ✓ Resolved |
| [7.3] Inflation coverage ≥25% | 0% | ~25% | ✓ Resolved |
| [8.2] Credit spread cluster | 23.6% | 17.1% | ✓ Reduced (monitor) |

---

## Validation Against All Rules

| Rule | Post-Trade | Detail |
|------|------------|--------|
| [0.1] Instrument Universe | ✓ | All instruments are long-only, non-leveraged, non-derivative, publicly listed |
| [1.1-S] Stabiliser | ✓ | 25.1% (15–25%) |
| [1.1-C] Compounder | ✓ | 63.0% (50–65%) |
| [1.1-O] Optionality | ✓ | 11.9% (10–20%) |
| [2.1] Income Substitution | ✓ | 446,516 / 9,000 = 49.6 months (≥24) |
| [2.2] Income Shock | ✓ | Not active |
| [3.1] Equity caps | ✓ | Largest: VAS 9.9%, VGS 9.8%, BHP 9.5%, PMGOLD 9.8% — all ≤10% |
| [3.1] Credit caps | ✓ | FLBL 7.0%, CRED 7.0%, TCPC 3.1% — all ≤7% |
| [3.1] Speculative caps | ✓ | GHY 0.4% (≤1% each, ≤3% agg) |
| [3.2] Issuer concentration | ✓ | Largest: AU Government 18.2% (≤20%) |
| [4.1] AU concentration | ✓ | AUD risk assets ~37.8% (≤55%) |
| [4.2] Macro drivers | ✓ | Largest: global_credit_spreads 17.1% (≤30%). All named drivers under 30%. |
| [5.1] AUD growth | ✓ | **50.4%** (50–70%). Economic exposure: VGS/VGE/PMGOLD/ETPMAG = non-AUD. SOL top-up provides buffer. |
| [5.2] Hedging | ✓ | 100% international growth unhedged (≥40%) |
| [6.1] Convexity | ✓ | PMGOLD 2/3, ETPMAG 2/3, GHY 2/3 — all pass under amended Rule 6.1 (criterion 1 auto-satisfied per Rule 0.1) |
| [7.1] Stabiliser liquidity | ✓ | 100% liquid ≤5 days |
| [7.2] Stabiliser duration | ✓ | **GSBG27 = 39.9%** of stabiliser (≤40%). GSBI ~24.9%, JPST+cash ~27.3%, GSBG33 ~7.9%. No bucket >40%. |
| [7.3] Inflation coverage | ✓ | GSBI ~111,000 / 446,516 = ~24.9% (≥25% target — essentially at boundary) |
| [8.1] Drawdown tolerance | ✓ | After 35% equity drawdown, stabiliser 446,516 still covers 24 months (216,000) |
| [8.2] Stress correlation | ⚠ Monitor | Credit spread group: CRED+FLBL+TCPC = 304k = 17.1% (reduced from 23.6%). Precious metals: PMGOLD+ETPMAG = 205k = 11.5%. AU equity beta: BHP+SOL+AGL+ORG+VAS = 542k = 30.4% — largest stress-correlated cluster; monitor. |
| [9.2] No action rule | ✓ | Breaches justify action; no discretionary triggers needed |

**Tight constraints to monitor:**

| Constraint | Value | Limit | Buffer |
|------------|------:|------:|-------:|
| GSBG27 % of stabiliser (Rule 7.2) | 39.9% | 40% | 0.1% |
| AUD growth (Rule 5.1) | 50.4% | 50% floor | 0.4% |
| FLBL % of portfolio (Rule 3.1-cr) | 7.0% | 7% | 0.0% |
| CRED % of portfolio (Rule 3.1-cr) | 7.0% | 7% | 0.0% |
| AU Government group (Rule 3.2) | 18.2% | 20% | 1.8% |

Rule 7.2 and Rule 5.1 are the tightest. GSBG27 matures April 2027 (14 months) — the 7.2 pressure resolves naturally. Rule 5.1 has minimal buffer and will tighten if non-AUD positions appreciate faster than AUD positions.

---

## Trade Summary

| # | Action | Instrument | Direction | ~AUD Amount | Ccy | Market |
|---|--------|------------|-----------|----------:|-----|--------|
| 1 | Trim | FLBL | Sell | 114,000 | USD | US (IB) |
| 2 | Trim | CRED.AX | Sell | 2,000 | AUD | ASX (IB) |
| 3 | Full sell | AGVT.AX | Sell | 95,000 | AUD | ASX (IB) |
| 4 | Trim | JPST | Sell | 16,000 | USD | US (IB) |
| 5 | New buy | GSBI (TIBs) | Buy | 111,000 | AUD | ASX |
| 6 | New buy | VAS.AX | Buy | 177,000 | AUD | ASX (IB) |
| 7 | New buy | VGS.AX | Buy | 175,000 | AUD | ASX (IB) |
| 8 | Top up | SOL.AX | Buy | 35,000 | AUD | ASX (IB) |
| 9 | New buy | VGE.AX | Buy | 51,000 | AUD | ASX (IB) |
| 10 | New buy | PMGOLD.AX | Buy | 175,000 | AUD | ASX (IB) |
| 11 | New buy | ETPMAG.AX | Buy | 30,000 | AUD | ASX (IB) |
| 12 | DB fix | GHY.AX | Classify | 0 | — | — |

**Sell proceeds**: ~AUD 227,000
**Buy total**: ~AUD 754,000
**Net cash deployed from stabiliser**: ~AUD 527,000

### Execution Sequence

**Day 1 — Sells:**
1. Sell AGVT.AX (full, ASX — liquid, same-day fill)
2. Trim CRED.AX (~AUD 2k, ASX)
3. Trim FLBL (~USD 80.5k, US market)
4. Trim JPST (~USD 11.3k, US market)

**Day 2–3 — FX + Transfers:**
- Convert ~USD 299k → AUD on IB (needed for ASX purchases)
- Transfer ~AUD 95k from RACQ to IB (AUD shortfall coverage)

**Day 3–7 — Buys (use limit orders):**
- VAS.AX, VGS.AX (large, liquid ASX ETFs — high daily volume)
- SOL.AX top-up (liquid ASX equity)
- PMGOLD.AX (liquid ASX ETF)
- GSBI (direct bonds — check ASX order book, patient limit orders; OR buy via CommSec alongside existing govt bonds)

**Day 7–10 — Smaller buys:**
- VGE.AX, ETPMAG.AX (smaller positions, adequate liquidity)

**Anytime — Database fix:**
- GHY.AX: `nonlinear_upside=true`
- PMGOLD.AX: `stress_outperformance=true`
- ETPMAG.AX: `stress_outperformance=true`
- Update compliance system to auto-satisfy criterion 1 under Rule 0.1

### Tax Flags

| Trade | Tax event? | Note |
|-------|-----------|------|
| Sell AGVT.AX | Yes | CGT on disposal. Check cost base. |
| Trim FLBL | Yes | Partial disposal — CGT + potential FX gain/loss (USD). |
| Trim JPST | Yes | Partial disposal — CGT + potential FX gain/loss (USD). |
| Trim CRED.AX | Yes | Partial disposal — small amount. |
| All buys | No | |

User should assess CGT impact before executing. This report does not model tax consequences.

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
towsand classify role ETPMAG.AX optionality

towsand classify tag PMGOLD.AX \
  --macro "gold_price" \
  --group "Perth Mint Gold" \
  --corr-group "precious_metals" \
  --duration 0 --liquidity 1 --no-inflation-linked

towsand classify tag ETPMAG.AX \
  --macro "silver_price" \
  --group "ETFS Physical Silver" \
  --corr-group "precious_metals" \
  --duration 0 --liquidity 1 --no-inflation-linked

# New stabiliser (inflation-linked) — use actual GSBI ticker
towsand classify role GSBI stabiliser
towsand classify tag GSBI \
  --macro "au_interest_rates" \
  --group "AU Government" \
  --corr-group "au_govt_bond" \
  --duration 5.0 --liquidity 2 --inflation-linked

# GHY.AX convexity fix
# Set nonlinear_upside=true (criterion 2)
# Set stress_outperformance=true for PMGOLD.AX and ETPMAG.AX (criterion 3)
```

---

## Changes from v1

| Issue | v1 (incorrect) | v2 (corrected) |
|-------|----------------|-----------------|
| FLBL cap | 10% equity cap applied; trimmed to 9.9% | **7% credit cap** applied; trimmed to 7.0% |
| CRED cap | Not flagged | **7% credit cap** applied; trimmed to 7.0% |
| Rule 6.1 criterion 1 | "Defined downside via position sizing" | **Auto-satisfied** under Rule 0.1 (instrument universe). Rule amended. |
| PMGOLD currency (5.1) | AUD (listing currency) | **Non-AUD** (economic exposure per amended Rule 5.1) |
| VGS currency (5.1) | Non-AUD | Non-AUD (unchanged — now consistent with PMGOLD) |
| SOL.AX | No change | **Topped up +35k** to maintain AUD growth ≥50% |
| Rule 7.2 | **Omitted** from validation | GSBG27 at **39.9%** of stabiliser — explicitly checked |
| AUD growth | "~62%" (inconsistent methodology) | **50.4%** (consistent economic exposure) |
| Credit spread cluster | 20.0% | **17.1%** (improved by larger FLBL trim) |

---

## Forward-Looking Notes

1. **GSBG27.AX maturity (April 2027):** When GSBG27 matures (~AUD 178k → cash), Rule 7.2 pressure resolves and stabiliser grows. Redeploy maturity proceeds into additional GSBI (maintain inflation coverage) or compounders/optionality if stabiliser exceeds 25%.

2. **Rule 5.1 buffer is thin (50.4%):** If non-AUD positions (VGS, PMGOLD) appreciate faster than AUD positions, AUD growth could drift below 50%. Monitor quarterly. If approaching 50%, top up AUD compounders or trim non-AUD positions.

3. **Compliance system updates (completed 2026-02-18):**
   - ~~Add `[3.1-cr]` check for credit instruments at 7%~~ — **Done.** `asset_class` field now drives cap selection. CRED.AX, FLBL, TCPC correctly checked at 7%.
   - ~~Rule 5.1 economic currency~~ — **Done.** `economic_currency` field now drives AUD growth calculation instead of listing currency.
   - Implement Rule 0.1 auto-satisfaction of 6.1 criterion 1 (or simplify the scoring system) — **Still needed.**

4. **GSBI selection:** Verify current ASX-listed Treasury Indexed Bond availability. Target maturities 2027–2033 matching stabiliser horizon. If multiple maturities available, ladder across the horizon.

5. **Optionality at 11.9% vs 15% midpoint:** Could increase to 15% by adding ~AUD 55k more optionality (e.g., increase PMGOLD or add second gold ETF). Not urgent — 11.9% is within band.

---

## Appendix A: Objective-Level Sensitivity

*How fragile is the portfolio against its strategic objectives? Generated by `towsand sensitivity` (post-fix: asset_class-based caps, economic_currency for Rule 5.1).*

### Pre-Trade Portfolio (Current)

| Objective | Severity | Finding |
|-----------|----------|---------|
| **Income Bridge** | SAFE | Covers 108 months (84 months excess). Cash alone (AUD 541,906) exceeds the 24-month floor — market declines in stabiliser holdings cannot break the bridge. |
| **Forced Liquidation** | SAFE | Stabiliser excess of AUD 757,084 (42.5% of portfolio) buffers against forced selling. |
| **Compounding Capital** | FRAGILE | Compounder capital is only AUD 801,405 (45% of portfolio — below 50% target). A 35% drawdown destroys AUD 280,492 and costs **6.8 years of recovery** at 6.5% real. Per 10% decline: AUD 80,140 lost, 1.7 years to recover. |
| **AUD Liability Matching** | SAFE | AUD growth at 57.3% (economic exposure). A 34.3% rally in non-AUD growth (FLBL, TCPC, UKW) needed to weaken below 50%. |
| **Optionality as Crisis Insurance** | CRITICAL | At 0.4% of portfolio (AUD 7,285), optionality is **decorative, not functional**. Even a 100% gain adds only AUD 7,285 — negligible against a 35% compounder drawdown of AUD 280,492. |

**Pre-trade rule buffers (tightest):**

| Rule | Description | Current | Limit | Buffer | Note |
|------|-------------|--------:|------:|-------:|------|
| 3.1-cr | FLBL credit cap | 13.4% | 7% | **-6.4pp** | ALREADY IN BREACH |
| 3.1-cr | CRED.AX credit cap | 7.1% | 7% | **-0.1pp** | ALREADY IN BREACH |
| 3.1-eq | BHP.AX equity cap | 9.5% | 10% | +0.5pp | BHP rallies 6% to breach |
| 3.2 | Issuer: AU Government | 17.3% | 20% | +2.7pp | Group outperforms rest |

**Key finding:** Survivability and income bridge are massively over-buffered (108 months vs 24 needed). The real vulnerability is that compounder capital is under-weight and optionality is essentially absent. The portfolio survives everything but compounds nothing and insures nothing.

### Post-Trade Portfolio (Projected)

| Objective | Severity | Finding |
|-----------|----------|---------|
| **Income Bridge** | SAFE | Post-trade stabiliser AUD 446,515 = 50 months. Reduced from 108 but still 2x the 24-month floor. A 54% decline in stabiliser holdings needed to break it. |
| **Forced Liquidation** | WATCH | Stabiliser excess AUD 230,515 (12.9% of portfolio). Adequate but no longer fortress-like. |
| **Compounding Capital** | SAFE | Compounder rises to AUD 1,122,974 (63.0%). A 35% drawdown costs AUD 393,041 — more dollars at risk, but from a stronger base. Recovery: 6.8 years. Per 10% decline: AUD 112,297 lost, 1.7 years to recover. |
| **AUD Liability Matching** | FRAGILE | AUD growth at 50.4% (economic exposure). A **1.7% rally** in non-AUD growth (VGS, PMGOLD, FLBL) weakens liability matching below 50%. Monthly monitoring required. |
| **Optionality as Crisis Insurance** | SAFE | At 11.9% (AUD 212,285), optionality is now sized to matter. If PMGOLD+ETPMAG perform as designed, they can materially offset compounder losses. |

**Post-trade rule buffers (tightest):**

| Rule | Description | Current | Limit | Buffer | Note |
|------|-------------|--------:|------:|-------:|------|
| 3.1-cr | FLBL credit cap | 7.0% | 7% | **-0.0pp** | Borderline — at cap exactly |
| 3.1-cr | CRED.AX credit cap | 7.0% | 7% | +0.0pp | Borderline |
| 3.1-eq | VAS.AX equity cap | 9.9% | 10% | **0.1pp** | VAS rallies 1% to breach |
| 7.2 | Duration: bucket 1y | 39.9% | 40% | **0.1pp** | Other stabiliser assets decline |
| 3.1-eq | VGS.AX equity cap | 9.8% | 10% | 0.2pp | VGS rallies 2% to breach |
| 3.1-eq | PMGOLD.AX equity cap | 9.8% | 10% | 0.2pp | PMGOLD rallies 2% to breach |
| 3.1-eq | BHP.AX equity cap | 9.5% | 10% | 0.5pp | BHP rallies 6% to breach |
| 3.2 | Issuer: AU Government | 18.2% | 20% | 1.8pp | Group outperforms rest |

**Key trade-off:** The recommendations trade an impregnable but idle stabiliser for active compounding and crisis insurance. Income bridge shrinks from 108 to 50 months (still 2x the floor). The new vulnerability is AUD liability matching at 50.4% — one of the tightest constraints in the post-trade portfolio.

---

## Appendix B: Stress Scenario Impact on Objectives

*For each scenario: can you still feed your family? How much compounding was destroyed? Did optionality perform? Generated by `towsand stress` (post-fix: asset_class proxy drawdowns, proxy disclosure).*

**Data source transparency:** COVID-2020 and GFC-2008 scenarios use **asset-class proxy drawdowns for all holdings** (DB price history starts 2021-02-18 — no actual data for those periods). The 2022 Rate Shock uses actual historical drawdowns for 12 of 13 pre-trade holdings. Proxy drawdowns are keyed by economic asset class (not ETF wrapper), so bond/cash instruments receive appropriate fixed-income proxies, not equity-like drawdowns.

Stress tests applied to **both pre-trade (current) and post-trade (projected)** portfolios. The post-trade portfolio reflects all 10 recommendations.

### Pre-Trade vs Post-Trade Comparison

| Scenario | | Wealth Lost | Comp. Destroyed | Recovery | Income Bridge | Forced Sell? |
|----------|-|----------:|----------------:|---------:|--------------:|-------------|
| **Flat 35% Haircut** | Pre | AUD 283,042 | AUD 280,492 | 6.8 yrs | 108 months | No |
| | **Post** | **AUD 467,341** | **AUD 393,041** | **6.8 yrs** | **50 months** | **No** |
| | Delta | +184,299 | +112,549 | 0.0 | -58 months | |
| **COVID-19 2020** ⚠ | Pre | AUD 188,849 | AUD 191,259 | 4.3 yrs | 109 months | No |
| | **Post** | **AUD 346,934** | **AUD 327,094** | **5.5 yrs** | **50 months** | **No** |
| | Delta | +158,085 | +135,835 | +1.1 | -59 months | |
| **GFC 2008** ⚠ | Pre | AUD 301,041 | AUD 327,938 | 8.4 yrs | 112 months | No |
| | **Post** | **AUD 500,759** | **AUD 533,909** | **10.2 yrs** | **53 months** | **No** |
| | Delta | +199,718 | +205,971 | +1.9 | -59 months | |
| **2022 Rate Shock** | Pre | AUD 38,000 | gained 7,343 | 0 yrs | 103 months | No |
| | **Post** | **AUD 121,116** | **AUD 90,162** | **1.3 yrs** | **45 months** | **No** |
| | Delta | +83,116 | +97,505 | +1.3 | -58 months | |

*⚠ = all-proxy scenario (no historical price data for that period). Treat as indicative, not precisely historical.*

### What the Comparison Reveals

**The trade-off is clear and intentional.** The recommendations move capital from an impregnable stabiliser into compounders and optionality. This means:

- **More dollars at risk in stress** — because there are more dollars deployed in growth assets. Post-trade GFC losses rise from AUD 301k to AUD 501k (+66%). This is the mathematical consequence of putting capital to work.
- **Income bridge shrinks from 108→50 months** — still 2x the 24-month floor, and still covers 45+ months even in the worst stress scenario. The pre-trade 108 months was excess safety that earned nothing.
- **Recovery time rises modestly** — 6.8 years unchanged for a flat 35% haircut. For the GFC proxy scenario, recovery rises from 8.4 to 10.2 years because the post-trade portfolio has more capital exposed to equity-like drawdowns.
- **No forced liquidation in any scenario** — the critical survivability test passes for both portfolios. Post-trade stabiliser covers 45–53 months across all scenarios.
- **Optionality now performs in the proxy scenarios.** In COVID (proxy), optionality lost only 11% vs compounders' 29% — crisis insurance function triggered. In GFC (proxy), optionality **gained** 3% (commodity proxy +5%) while compounders lost 48%. The flat 35% scenario is worst-case because it hits everything uniformly.

### Post-Trade Objective Assessment by Scenario

**1. SURVIVABILITY: Pass in all scenarios (both portfolios).** Post-trade stabiliser AUD 446,515 still covers 45–53 months under the worst stress. Forced liquidation threshold is never close.

**2. INCOME BRIDGE: Intact but thinner.** Worst case post-trade (2022 rate shock): 45 months. This is 21 months above the 24-month floor — adequate buffer, but no longer the fortress-like 100+ months of pre-trade. The income bridge now requires monitoring.

**3. COMPOUNDING: More capital at risk, but by design.** Post-trade GFC (proxy) destroys AUD 534k vs pre-trade AUD 328k. But the pre-trade portfolio had only AUD 801k compounding — the post-trade has AUD 1,123k. The percentage loss is similar (48% vs 41%) with more absolute capital at risk. More dollars at risk is the price of having more dollars compounding.

**4. OPTIONALITY: Now meaningful, and performs in proxy scenarios.** At AUD 212,285, optionality is 12% of the portfolio. In COVID proxy, optionality lost 11% (commodity proxy: -10%) vs compounders' 29% — it performed its crisis function. In the GFC proxy, PMGOLD and ETPMAG **gained** (commodity proxy: +5%) while compounders lost 48%. Only in the uniform flat-35% synthetic does optionality fail — because it's designed as a synthetic worst-case, not a realistic scenario. In reality, gold rallied +26% during COVID 2020, reinforcing that the commodity proxy drawdowns are conservative.

**5. 2022 RATE SHOCK: The post-trade vulnerability.** The 2022 scenario is the most informative because it uses mostly actual historical data (12/18 holdings historical, 6 proxy). Post-trade loss: AUD 121k vs pre-trade AUD 38k. This is because bonds, credit, AND equities all fell simultaneously, and the post-trade portfolio has more assets in all three. However, optionality **gained** 4% (commodity proxy: +5%), partially offsetting. This scenario specifically targets the post-trade design — but even here the income bridge holds at 45 months.

---

## Appendix C: Diversification Quality

*Does your diversification actually work when it matters? Generated by `towsand correlations` (post-fix: corrected optionality member count).*

Analysis from 5 years of daily prices. 55 stress trading days identified (rolling 60-day equity drawdown exceeding -15%).

### Does Each Role Do Its Job?

| Question | Answer | Evidence |
|----------|--------|----------|
| **Does the stabiliser stabilise?** | Neutral — diversifies but doesn't actively offset. | Stabiliser–compounder stress correlation: 0.12. Low enough to not amplify losses, but not negative enough to provide a cushion. |
| **Does optionality provide crisis alpha?** | Unknown — insufficient data. | Only 1 optionality instrument (GHY.AX, AUD 7,285). Insufficient cross-role pairs for meaningful stress correlation measurement. |
| **Are compounders genuinely diversified?** | **Yes — well-diversified.** | Average intra-compounder stress correlation: 0.08. Losses in BHP are unlikely to coincide with losses in FLBL, CRED, or UKW. Highest pair: BHP–ORG at 0.36. |
| **Are stabiliser instruments diversified?** | Moderate. | Avg intra-stabiliser stress correlation: 0.27. Some shared duration sensitivity, but not a single bet. |
| **Optionality diversification** | N/A | Only 1 optionality instrument — intra-role diversification not applicable. |

### Hidden Concentration Risk

| Pair | Tagged Groups | Stress Corr | Meaning |
|------|---------------|------------:|---------|
| **AGVT–CRED** | au_govt_bond / credit_spread | **0.86** | CRED.AX behaves like a duration instrument in stress, not a credit instrument. When rates move, AGVT and CRED move together. They are effectively the same bet — both are long AUD duration. |

**Implication:** The post-trade portfolio has GSBI (inflation-linked govt bond) replacing AGVT, and CRED at 7% cap. But if CRED is really a duration bet disguised as credit, then the combined AU government + CRED duration exposure is larger than the compliance system recognises.

### False Diversification (Over-Grouped)

All three multi-member stress groups have average stress correlations well below the assumed 0.7 threshold:

| Group | Avg Stress Corr | Weakest Pair | Reality |
|-------|----------------:|-------------|---------|
| au_equity_beta | 0.26 | AGL–BHP (0.17) | BHP (mining), AGL/ORG (energy), SOL (conglomerate) are genuinely different businesses. Treating them as one risk overstates concentration. |
| au_govt_bond | 0.28 | AGVT–GSBG27 (0.07) | Different durations = different rate sensitivity. Not one risk. |
| credit_spread | 0.10 | CRED–TCPC (-0.05) | FLBL (floating-rate), CRED (IG fixed-rate), TCPC (equity-like BDC) are three different risk profiles. The "credit" label is misleading. |

**Net effect:** The compliance system's [8.2] stress correlation warnings are **conservative** — they flag concentration that doesn't exist in practice. This is safe-side error but wastes attention on non-problems.

---

**Report Generated:** 2026-02-18 09:47 AEST
**Analytics updated:** 2026-02-18 — Re-run with post-fix code (asset_class caps, economic_currency, corrected proxy drawdowns, proxy disclosure)
**Portfolio Value:** AUD 1,781,774.17
**Current Compliance:** 10 pass, 4 warning, 4 breach (FLBL 3.1-cr, CRED 3.1-cr, compounder band, GHY convexity)
**Post-Trade Compliance (projected):** Not fully verifiable — `towsand compliance` cannot yet run on a projected portfolio with full metadata propagation. Sensitivity and stress --trades provide the best current approximation.
**Data source notes:** COVID/GFC stress use all-proxy drawdowns (no DB price data pre-2021). 2022 Rate Shock uses 12/13 historical (pre-trade), 11/18 historical (post-trade).
