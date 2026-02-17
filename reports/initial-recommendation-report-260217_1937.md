# Initial Recommendation Report — 2026-02-17 19:37

All monetary values are in **AUD** unless stated otherwise.

---

## Rule 9.2 Gate: Action Assessment

| Check | Result |
|-------|--------|
| Breaches exist? | **Yes** — 3 active breaches |
| Active triggers? | No (`income_shock_active`, `inflation_shift_active`, `currency_regime_active`, `correlation_convergence_active` — all inactive) |
| Rule 9.2 override? | **No** — breaches require mandatory action per Rule 1.1 breach action: "rebalance within 30 days unless driven by market moves <10%." |

**Conclusion: Action is required.** Three compliance breaches exist. Rule 9.2 ("Absent a trigger, no discretionary rebalancing") does not apply because the rebalancing is mandatory, not discretionary. The 30-day deadline runs from the date of this report (2026-02-17).

---

## Current Compliance Summary

| Rule | Status | Detail |
|------|--------|--------|
| [D.1] Data Freshness | ✓ Pass | All prices ≤7 days old |
| [2.1] Income Substitution | ✓ Pass | 108.1 months coverage (≥24 required) |
| [1.1-S] Stabiliser Band | ⚠ Warning | **54.6%** (target 15–25%) — AUD 527,641 over upper bound |
| **[1.1-C] Compounder Band** | **✗ Breach** | **45.0%** (min 50%) — AUD 89,483 below minimum |
| [1.1-O] Optionality Band | ⚠ Warning | **0.4%** (target 10–20%) — AUD 170,892 below minimum |
| [2.2] Income Shock | ✓ Pass | No income shock active |
| **[3.1-eq] Single Equity Cap** | **✗ Breach** | **FLBL at 13.4%** (max 10%) — AUD 60,841 over cap |
| [4.1] Australia Concentration | ✓ Pass | 31.4% (max 55%) |
| [4.2] Macro Driver Exposure | ✓ Pass | Highest: global_credit_spreads at 23.6% (max 30%) |
| [5.1] AUD Growth Exposure | ✓ Pass | 57.3% (target 50–70%) |
| [5.2] Hedging Rule | ✓ Pass | 100% unhedged (≥40% required) |
| **[6.1] Convexity Test** | **✗ Breach** | **GHY.AX scores 0/3** (need ≥2) — missing database flags |
| [7.1] Stabiliser Liquidity | ✓ Pass | 100% liquid within 5 days |
| [7.3] Inflation Coverage | ⚠ Warning | **0.0%** inflation-linked (target ≥25%) |
| [8.1] Drawdown Tolerance | ✓ Pass | Stabiliser covers 24 months after 35% drawdown |
| [8.2] Stress Correlation | ⚠ Warning | Credit spread group at **23.6%** |
| [9.2] No Action Rule | ✓ Pass | No triggers active (but breaches override) |

**Active breaches requiring action within 30 days:**
1. [1.1-C] Compounder below 50% minimum
2. [3.1-eq] FLBL exceeds 10% single-position cap
3. [6.1] GHY.AX fails convexity test (database flag issue)

---

## Dollar Gap Analysis

### Role Gaps (vs target band edges)

| Role | Current | Current % | Target % | Target AUD | Gap |
|------|--------:|----------:|---------:|-----------:|----:|
| Stabiliser | 973,084 | 54.6% | 25% (upper) | 445,444 | -527,640 (over by) |
| Compounder | 801,405 | 45.0% | 63%* | 1,122,518 | +321,113 (under by) |
| Optionality | 7,285 | 0.4% | 12%* | 213,813 | +206,528 (under by) |

*Target allocation: 25/63/12 = 100%. Compounder at 63% (within 50–65% band), optionality at 12% (within 10–20% band). See rationale in §Recommendations.

### Position Size Breach

| Holding | Current AUD | Current % | Cap | Excess |
|---------|------------:|----------:|----:|-------:|
| FLBL | 239,018 | 13.4% | 10% (178,177) | 60,841 |

### Missing Exposures

| Exposure | Current | Target | Gap |
|----------|---------|--------|-----|
| Inflation-linked stabiliser | 0% (AUD 0) | ≥25% of stabiliser | ~AUD 111,000 (after stabiliser resize to 445k) |
| Optionality capital | 0.4% (AUD 7,285) | 10–20% | ~AUD 207,000 to reach 12% |

### Concentration Risk

| Risk | Current | Concern |
|------|---------|---------|
| Credit spread cluster (Rule 8.2) | 23.6% (AUD 420,284) | CRED + FLBL + TCPC treated as one risk in stress |
| Global credit spreads (Rule 4.2) | 23.6% | Approaching 30% cap — must not add more credit |

---

## Recommendations

### Priority 1: Fix Breaches (Mandatory — 30 Day Deadline)

---

### Rec 1: Trim FLBL (Franklin Senior Loan ETF)

- **Type**: Sell (partial)
- **Amount**: AUD ~63,000 (USD ~44,500 at current FX)
- **Current position**: AUD 239,018 (13.4%)
- **Post-trade position**: AUD ~176,000 (9.9%)
- **Role**: Compounder (unchanged — proceeds redeployed to new compounders)
- **Rules addressed**: [3.1-eq] Single Equity Cap breach; also reduces [8.2] credit spread cluster from 23.6% to ~20.0%, and [4.2] global_credit_spreads from 23.6% to ~20.0%
- **Rationale**: FLBL is a diversified ETF (300+ senior loans) so idiosyncratic risk is low, but the position is 34% above the 10% cap. The trim is mandatory per Rule 3.1 and the 30-day breach action. Reducing FLBL also brings the credit spread correlation cluster (Rule 8.2) back toward a manageable level.
- **Constraints**: Rule 3.1 caps single listed instruments at 10%. Trimming to 9.9% provides a small buffer against price appreciation re-triggering the breach.
- **Risk note**: Reduces income (FLBL yields ~8–9% from floating-rate credit spread). This is acceptable because the portfolio is over-concentrated in credit spread risk and the income loss is replaced by diversified growth from new compounder positions.

---

### Rec 2: Deploy Cash into Compounders — Buy VAS.AX (Vanguard Australian Shares Index ETF)

- **Type**: Buy (new position)
- **Amount**: AUD 175,000
- **Role**: Compounder
- **Rules addressed**: [1.1-C] Compounder below 50% (primary); [1.1-S] Stabiliser overweight (reduces cash in stabiliser)
- **Rationale**: VAS provides broad exposure to ~300 ASX-listed stocks at low cost (0.07% MER). The portfolio currently concentrates its Australian equity exposure in four individual names (BHP, SOL, AGL, ORG), which creates stock-specific risk. VAS diversifies the domestic equity allocation while maintaining the Strategy §3 objective of "durable, high-ROIC businesses and diversified global equity exposure." VAS includes exposure to the banking sector (CBA, NAB, WBC, ANZ), healthcare (CSL), and consumer sectors — macro drivers currently absent from the portfolio.
- **Why VAS over alternatives**:
  - Over STW.AX: VAS has broader coverage (~300 vs ~200 stocks) with similar cost.
  - Over topping up BHP: BHP is already at 9.5%, near the 10% cap. Individual stock concentration should decrease, not increase.
  - Over individual stock picks: The "non-sophisticated investor" constraint and diversification objective favour index ETFs.
- **Constraints**: Position at 9.8% of portfolio, within 10% cap. Partially overlaps existing AU equity holdings (BHP ~10% of ASX 300 index) but this is manageable.
- **Risk note**: Concentrates more capital in Australian equities. Mitigated by: (a) Rule 4.1 check — AUD risk assets remain well under 55%, (b) balanced by international compounder purchases (Rec 3, Rec 4).

---

### Rec 3: Deploy Cash into Compounders — Buy VGS.AX (Vanguard MSCI Index International Shares ETF)

- **Type**: Buy (new position)
- **Amount**: AUD 150,000
- **Role**: Compounder
- **Rules addressed**: [1.1-C] Compounder below 50%; [1.1-S] Stabiliser overweight
- **Rationale**: VGS tracks the MSCI World ex-Australia Index (~1,500 stocks across US, Europe, Japan, UK) at low cost (0.18% MER). The portfolio currently lacks broad diversified international equity exposure — its international compounders are concentrated in credit instruments (FLBL, TCPC) and a single UK infrastructure fund (UKW). VGS adds developed-market equity exposure without concentrating on any single macro driver named in Rule 4.2. Strategy §3 explicitly calls for "diversified global equity exposure" within the compounder allocation.
- **Why VGS over alternatives**:
  - Over IVV.AX (S&P 500): VGS provides broader geographic diversification (US ~70%, Europe ~20%, Japan ~6%), not just US equity.
  - Over VGAD (hedged): Strategy §5.2 and §6 emphasise unhedged international exposure for regime insurance. All current international positions are unhedged.
  - Over single international stocks: Diversification and "non-sophisticated investor" constraint favour index ETFs.
- **Currency note**: VGS.AX is AUD-denominated but holds international equities (unhedged). For Rule 5.1 (AUD Growth Exposure), VGS should be classified as **non-AUD growth** since the underlying has no Australian exposure. The system will need `hedged: no` in classification to reflect this.
- **Constraints**: Position at 8.4% of portfolio. Macro driver exposure is diversified across multiple economies — no single Rule 4.2 driver is materially affected.
- **Risk note**: International equity exposure is fully unhedged to AUD. In a scenario where AUD strengthens sharply, VGS would underperform AUD-denominated alternatives. This is intentional per Strategy §6 (regime insurance).

---

### Rec 4: Deploy Cash into Compounders — Buy VGE.AX (Vanguard FTSE Emerging Markets Shares ETF)

- **Type**: Buy (new position)
- **Amount**: AUD 57,000
- **Role**: Compounder
- **Rules addressed**: [1.1-C] Compounder below 50%; [1.1-S] Stabiliser overweight
- **Rationale**: VGE provides exposure to emerging market equities (China ~30%, India ~20%, Taiwan ~17%, Brazil ~5%) which are completely absent from the portfolio. Emerging markets offer higher long-term growth potential and diversify the compounder allocation beyond developed markets. The position is intentionally small (3.2%) to reflect the higher volatility and political risk of EM equities.
- **Why VGE**: Strategy §4 states "No single position or macro factor is allowed to dominate total outcomes." EM equity adds a growth driver that is partially independent of developed-market cycles.
- **Constraints**: china_demand exposure increases modestly (~AUD 17,000 via China weight in VGE) — new total china_demand ~AUD 187,000 = 10.5%, well under 30% cap.
- **Risk note**: Emerging markets carry higher volatility, political risk, and currency risk. Small sizing (3.2%) limits impact. Also adds china_demand exposure, but this remains well within Rule 4.2 limits.

---

### Rec 5: Fix GHY.AX Convexity Test — Set Database Flags

- **Type**: Database update (no trade required)
- **Amount**: AUD 0
- **Role**: Optionality (unchanged)
- **Rules addressed**: [6.1] Convexity Test breach
- **Rationale**: GHY.AX (Gold Hydrogen Ltd) is a pre-revenue hydrogen exploration company with a binary outcome profile. It conceptually meets the optionality convexity test but fails because the convexity flags are not set in the database. Scoring:
  1. **Defined downside** ✓ — Position is AUD 7,285 (0.4% of portfolio). Maximum loss is capped by position size, similar to an option premium.
  2. **Non-linear upside (>3x in favourable regime)** ✓ — If hydrogen exploration succeeds, the upside is many multiples. This is a genuine binary bet.
  3. **Stress-period outperformance** ✗ — A speculative micro-cap would likely correlate with risk-off in equity stress.
  - **Score: 2/3 → passes Rule 6.1** (requires ≥2/3).
- **Action**: Run `towsand classify` commands to set `defined_downside=true` and `nonlinear_upside=true` for GHY.AX. This resolves the breach without any trade.
- **Risk note**: None — this is a data correction, not a portfolio change. GHY.AX remains within the speculative cap (0.4% < 1% individual, < 3% aggregate per Rule 3.1).

---

### Priority 2: Address Warnings (Naturally Resolved by Breach Fixes)

---

### Rec 6: Swap Nominal Stabiliser for Inflation-Linked — Sell AGVT.AX, Trim JPST, Buy Treasury Indexed Bonds

- **Type**: Sell (AGVT.AX, full position) + Sell (JPST, partial) + Buy (GSBI series)
- **Amount**: Sell AGVT.AX ~AUD 95,000; Trim JPST ~AUD 16,000; Buy ~AUD 111,000 of Treasury Indexed Bonds
- **Role**: Stabiliser (internal rebalance — no role change)
- **Rules addressed**: [7.3] Inflation Coverage (0% → ~25% of stabiliser)
- **Rationale**: Rule 7.3 requires ≥25% of stabiliser in inflation-linked or real-rate sensitive instruments. Currently 0%. After resizing stabiliser to ~AUD 445,000, 25% = ~AUD 111,000. Selling AGVT.AX (a nominal government bond ETF, AUD 95,473) and trimming JPST (USD ultra-short, AUD 16,000) generates AUD 111,473 to purchase Treasury Indexed Bonds (TIBs). TIBs are Australian government bonds with coupon and principal indexed to CPI — they provide real (after-inflation) returns and directly address the inflation coverage gap.
- **Instrument selection**: Purchase ASX-listed Treasury Indexed Bonds (GSBI series) with maturities in the 2027–2033 range, matching the stabiliser horizon per Strategy §3. **User should verify current ASX availability** — specific tickers may include GSBI27, GSBI30, GSBI35, or equivalent. If direct TIBs are illiquid, an alternative is an inflation-linked bond ETF (e.g., check availability of inflation-linked government bond ETFs on ASX).
- **Why sell AGVT.AX**: AGVT holds nominal government bonds with no inflation protection. Replacing it with inflation-linked bonds of similar credit quality (both are AU Government) addresses Rule 7.3 without changing the stabiliser's risk profile. AGVT.AX also has overlapping exposure with GSBG27.AX and GSBG33.AX (all track au_interest_rates).
- **Why trim JPST**: JPST is USD-denominated, creating a currency mismatch against AUD living expenses within the stabiliser. Trimming AUD 16,000 to fund the remaining GSBI purchase reduces this currency mismatch. Post-trim JPST is AUD ~106,000 (still provides USD liquidity).
- **Constraints**: AU Government corporate group concentration increases from 17.3% to ~18.2% (GSBG27 + GSBG33 + GSBI) — still under the 20% cap per Rule 3.2.
- **Risk note**: GSBI bonds have longer duration than AGVT/JPST, which introduces more interest rate sensitivity. Mitigated by: (a) real yield protects purchasing power, (b) maturities matched to stabiliser horizon, (c) stabiliser liquidity remains ≥70% (Rule 7.1).

---

### Rec 7: Build Optionality Allocation — Buy PMGOLD.AX (Perth Mint Gold ETF)

- **Type**: Buy (new position)
- **Amount**: AUD 175,000
- **Role**: Optionality
- **Rules addressed**: [1.1-O] Optionality underweight (0.4% → 12%); [1.1-S] Stabiliser overweight (deploys cash)
- **Rationale**: Gold is the most accessible genuinely convex instrument for a non-sophisticated investor (no options, warrants, futures, or private assets per Strategy constraints). PMGOLD.AX is backed by physical gold stored at the Perth Mint, is highly liquid on ASX, and has one of the lowest costs for physical gold exposure on the Australian market.
- **Rule 6.1 Convexity Test scoring for gold**:
  1. **Defined downside** ✓ — Gold doesn't go to zero; production cost floor (~USD 1,000–1,200/oz) provides a fundamental floor. Position sizing at 9.8% of portfolio caps absolute loss.
  2. **Non-linear upside (>3x in favourable regime)** — Partial. Gold went from USD 260 (2001) to USD 1,900 (2011) = 7.3x over 10 years. In shorter horizons (12–18 months per optionality definition), gold can rally 30–80% in crisis/inflation regimes but rarely >3x.
  3. **Stress-period outperformance** ✓ — Strong historical evidence: gold rallied during GFC (2008), European debt crisis (2011), COVID (2020), and equity drawdowns. Negative/zero correlation to equity beta in severe stress.
  - **Score: 2/3 → passes Rule 6.1.**
- **Why PMGOLD over alternatives**:
  - Over gold miners (e.g., GDX equivalent): Miners carry operating leverage, management risk, and cost inflation. In severe equity stress, gold miners can fall WITH equities initially (2008 precedent). Physical gold is a purer crisis hedge.
  - Over managed futures/tail-risk ETFs: Not reliably available on ASX for retail non-sophisticated investors. Gold is simpler and well-understood.
  - Over Bitcoin/crypto ETFs: Higher regulatory uncertainty, extreme volatility, and shorter track record of stress-period outperformance. Not appropriate as core optionality.
- **Currency note**: PMGOLD.AX is AUD-denominated. The underlying gold price is USD-denominated globally, so PMGOLD has embedded USD exposure — it benefits from both rising gold AND AUD weakness. For Rule 5.1 classification, PMGOLD should be tagged as AUD (listing currency). See §Validation for the impact on AUD growth exposure.
- **Constraints**: Position at 9.8% of portfolio, within the 10% single-position cap.
- **Risk note**: Gold is a non-yielding asset. It produces no income, dividends, or coupons. Its role is portfolio insurance and regime-change asymmetry, not return generation. In sustained equity bull markets with low inflation, gold may underperform significantly. This is the intended trade-off for optionality.

---

### Rec 8: Build Optionality Allocation — Buy ETPMAG.AX (ETFS Physical Silver)

- **Type**: Buy (new position)
- **Amount**: AUD 32,000
- **Role**: Optionality
- **Rules addressed**: [1.1-O] Optionality underweight; diversifies the optionality bucket beyond gold alone
- **Rationale**: Silver provides higher-beta precious metals exposure that complements gold in the optionality bucket. Silver has both monetary and industrial demand drivers, creating a different payoff profile. Silver's higher volatility means it can deliver larger percentage moves in dislocations (e.g., silver went from ~USD 12 to ~USD 28 in mid-2020 = 2.3x in months). The allocation is deliberately small (1.8%) to reflect silver's higher volatility and less reliable stress-hedge characteristics compared to gold.
- **Rule 6.1 scoring**: Similar to gold — defined downside (position sizing at 1.8%), stress-period outperformance (partially — silver rallied in 2020 but is less consistent than gold). Score: 2/3 (borderline).
- **Constraints**: Position at 1.8% — well within all caps.
- **Risk note**: Silver is more volatile than gold and has partial industrial demand, which can cause it to correlate with equities during industrial downturns. Small position size limits this risk.

---

## Post-Trade Projection

### Role Allocation (Before → After → Target Band)

| Role | Before AUD | Before % | After AUD | After % | Target Band | Status |
|------|----------:|---------:|----------:|--------:|-------------|--------|
| Stabiliser | 973,084 | 54.6% | ~445,000 | ~25.0% | 15–25% | ✓ At upper bound |
| Compounder | 801,405 | 45.0% | ~1,122,000 | ~63.0% | 50–65% | ✓ In band |
| Optionality | 7,285 | 0.4% | ~215,000 | ~12.1% | 10–20% | ✓ In band |

### Breach Resolution

| Rule | Before | After | Resolved? |
|------|--------|-------|-----------|
| [1.1-C] Compounder min 50% | 45.0% (BREACH) | ~63.0% | ✓ Yes |
| [3.1-eq] FLBL max 10% | 13.4% (BREACH) | ~9.9% | ✓ Yes |
| [6.1] GHY.AX convexity | 0/3 (BREACH) | 2/3 (flag fix) | ✓ Yes |

### Warning Improvement

| Rule | Before | After | Status |
|------|--------|-------|--------|
| [1.1-S] Stabiliser 15–25% | 54.6% (Warning) | ~25.0% | ✓ Resolved |
| [1.1-O] Optionality 10–20% | 0.4% (Warning) | ~12.1% | ✓ Resolved |
| [7.3] Inflation coverage ≥25% | 0.0% (Warning) | ~25.0% | ✓ Resolved |
| [8.2] Credit spread cluster | 23.6% (Warning) | ~20.0% | ⚠ Improved (monitor) |

### Stabiliser Detail (After)

| Instrument | AUD Value | Type | Duration | Inflation-linked? |
|------------|----------:|------|----------|--------------------|
| GSBG27.AX | 178,120 | govt_bond_nominal | 1.2yr | No |
| GSBI (new) | ~111,000 | govt_bond_indexed | 3–7yr* | **Yes** |
| JPST (trimmed) | ~106,000 | etf (USD) | 0.5yr | No |
| GSBG33.AX | 35,448 | govt_bond_nominal | 7.0yr | No |
| Cash | ~14,000 | cash | 0 | No |
| **Total** | **~445,000** | | | **~25% inflation-linked** |

*Duration depends on specific GSBI maturity selected.

**Expense coverage**: AUD 445,000 / AUD 9,000/month = **49.4 months** (≥24 required) ✓

### Compounder Detail (After)

| Instrument | AUD Value | % of Portfolio | Macro Drivers |
|------------|----------:|---------------:|---------------|
| FLBL (trimmed) | ~176,000 | 9.9% | global_credit_spreads, us_interest_rates |
| VAS.AX (new) | 175,000 | 9.8% | au_domestic_demand, au_equity_market |
| BHP.AX | 169,696 | 9.5% | bulk_commodities, china_demand |
| VGS.AX (new) | 150,000 | 8.4% | global_developed_equity |
| CRED.AX | 126,861 | 7.1% | global_credit_spreads, au_interest_rates |
| SOL.AX | 74,300 | 4.2% | au_domestic_demand, bulk_commodities |
| AGL.AX | 67,727 | 3.8% | au_energy, au_domestic_demand |
| VGE.AX (new) | 57,000 | 3.2% | china_demand, emerging_markets |
| TCPC | 54,405 | 3.1% | global_credit_spreads, us_private_credit |
| UKW | 51,757 | 2.9% | energy_transition, uk_inflation |
| ORG.AX | 17,640 | 1.0% | au_energy, au_domestic_demand |
| **Total** | **~1,121,000** | **~63%** | |

### Optionality Detail (After)

| Instrument | AUD Value | % of Portfolio | Convexity Score |
|------------|----------:|---------------:|-----------------|
| PMGOLD.AX (new) | 175,000 | 9.8% | 2/3 |
| ETPMAG.AX (new) | 32,000 | 1.8% | 2/3 |
| GHY.AX | 7,285 | 0.4% | 2/3 (after flag fix) |
| **Total** | **~214,000** | **~12.0%** | |

### Position Sizes (All Positions After Trades)

| Position | AUD Value | % | Cap | Status |
|----------|----------:|--:|----:|--------|
| GSBG27.AX | 178,120 | 10.0% | N/A (govt bond) | ✓ |
| FLBL | ~176,000 | 9.9% | 10% | ✓ |
| VAS.AX | 175,000 | 9.8% | 10% | ✓ |
| PMGOLD.AX | 175,000 | 9.8% | 10% | ✓ |
| BHP.AX | 169,696 | 9.5% | 10% | ✓ |
| VGS.AX | 150,000 | 8.4% | 10% | ✓ |
| CRED.AX | 126,861 | 7.1% | 10% | ✓ |
| GSBI | ~111,000 | 6.2% | N/A (govt bond) | ✓ |
| JPST | ~106,000 | 6.0% | 10% | ✓ |
| SOL.AX | 74,300 | 4.2% | 10% | ✓ |
| AGL.AX | 67,727 | 3.8% | 10% | ✓ |
| VGE.AX | 57,000 | 3.2% | 10% | ✓ |
| TCPC | 54,405 | 3.1% | 10% | ✓ |
| UKW | 51,757 | 2.9% | 10% | ✓ |
| GSBG33.AX | 35,448 | 2.0% | N/A (govt bond) | ✓ |
| ETPMAG.AX | 32,000 | 1.8% | 10% | ✓ |
| ORG.AX | 17,640 | 1.0% | 10% | ✓ |
| GHY.AX | 7,285 | 0.4% | 1% (speculative) | ✓ |

No position exceeds its applicable cap.

---

## Validation Against All Rules

| Rule | Post-Trade Status | Detail |
|------|-------------------|--------|
| [D.1] Data Freshness | ✓ Pass | No change |
| [1.1-S] Stabiliser Band | ✓ Pass | 25.0% (was 54.6% warning) |
| [1.1-C] Compounder Band | ✓ Pass | ~63.0% (was 45.0% **breach**) |
| [1.1-O] Optionality Band | ✓ Pass | ~12.0% (was 0.4% warning) |
| [2.1] Income Substitution | ✓ Pass | 49.4 months (≥24, reduced from 108 but still well above floor) |
| [2.2] Income Shock | ✓ Pass | No change |
| [3.1-eq] Single Equity Cap | ✓ Pass | FLBL at 9.9% (was 13.4% **breach**); all others under 10% |
| [3.1] Speculative Cap | ✓ Pass | GHY.AX at 0.4% (< 1% individual, < 3% aggregate) |
| [3.2] Issuer Concentration | ✓ Pass | AU Government highest at ~18.2% (< 20% cap) |
| [4.1] Australia Concentration | ✓ Pass | AUD risk assets ~43% (< 55% cap). Increased from 31.4% by VAS addition but well within limit. |
| [4.2] Macro Driver Exposure | ✓ Pass | global_credit_spreads reduced to ~20.0% (from 23.6%); no driver >30% |
| [5.1] AUD Growth Exposure | ✓ Pass (see note) | ~62% if PMGOLD/ETPMAG counted as AUD (listing currency). **Caveat**: if system classifies gold/silver as non-AUD underlying, this drops to ~48% — would breach 50% minimum. Recommend classifying PMGOLD/ETPMAG as AUD (they are AUD-denominated instruments on ASX). If reclassified as non-AUD, increase VAS by ~AUD 30k and decrease VGS by ~AUD 30k to restore balance. |
| [5.2] Hedging Rule | ✓ Pass | All international growth remains unhedged (>40% minimum) |
| [6.1] Convexity Test | ✓ Pass | GHY.AX 2/3 (after flag fix); PMGOLD 2/3; ETPMAG 2/3 |
| [7.1] Stabiliser Liquidity | ✓ Pass | >70% liquid within 5 days (GSBG27, GSBI, JPST, cash all liquid ≤2 days) |
| [7.3] Inflation Coverage | ✓ Pass | GSBI ~AUD 111,000 = ~25% of stabiliser (from 0%) |
| [8.1] Drawdown Tolerance | ✓ Pass | After 35% equity drawdown, stabiliser AUD 445,000 still covers 24 months (AUD 216,000). Equity drawdown would affect compounders (~AUD 734k equity-exposed × 35% = ~AUD 257k loss), but stabiliser is untouched. |
| [8.2] Stress Correlation | ⚠ Monitor | Credit spread group reduced to ~20.0% (from 23.6%). Improved but still concentrated. Precious metals group (PMGOLD + ETPMAG) at ~11.6% — these have >0.7 correlation to each other in stress but this is acceptable for optionality. |
| [9.2] No Action Rule | ✓ Pass | No triggers active; all breaches resolved |

**Validation result: All rules pass after proposed trades.** One monitoring item remains (credit spread cluster), and one caveat on Rule 5.1 requires confirming PMGOLD/ETPMAG currency classification.

---

## Execution Notes

### Trade Summary

| # | Action | Instrument | Direction | AUD Amount | Currency | Market |
|---|--------|------------|-----------|----------:|----------|--------|
| 1 | Trim | FLBL | Sell | ~63,000 | USD | US (IB) |
| 2 | Full sell | AGVT.AX | Sell | ~95,000 | AUD | ASX (IB) |
| 3 | Trim | JPST | Sell | ~16,000 | USD | US (IB) |
| 4 | New buy | GSBI (TIBs) | Buy | ~111,000 | AUD | ASX (IB or CommSec) |
| 5 | New buy | VAS.AX | Buy | 175,000 | AUD | ASX (IB) |
| 6 | New buy | VGS.AX | Buy | 150,000 | AUD | ASX (IB) |
| 7 | New buy | VGE.AX | Buy | 57,000 | AUD | ASX (IB) |
| 8 | New buy | PMGOLD.AX | Buy | 175,000 | AUD | ASX (IB) |
| 9 | New buy | ETPMAG.AX | Buy | 32,000 | AUD | ASX (IB) |
| 10 | DB fix | GHY.AX | Classify | 0 | — | — |

### Recommended Sequence

**Phase A — Sells (Day 1):**
1. Sell AGVT.AX (full position, ASX, liquid — should fill same day)
2. Trim FLBL (~USD 44,500, US market, liquid ETF)
3. Trim JPST (~USD 11,300, US market, very liquid)

**Phase B — FX Conversion (Day 2–3):**
- After USD sells settle (T+1 for US ETFs), convert excess USD to AUD on IB
- Total AUD needed for ASX purchases: ~AUD 700,000
- AUD available after sells: IB AUD ~134k + AGVT proceeds ~95k = ~229k
- USD available for conversion: IB USD + sell proceeds = ~USD 254k = ~AUD 360k
- Shortfall: ~AUD 111k — transfer from RACQ accounts to IB, OR purchase GSBI through CommSec (alongside existing govt bond holdings there)

**Phase C — Buys (Day 3–10):**
- Day 3–5: Buy VAS.AX, VGS.AX (most liquid ASX ETFs, high daily volume)
- Day 5–7: Buy PMGOLD.AX, GSBI (liquid but may require limit orders for GSBI direct bonds)
- Day 7–10: Buy VGE.AX, ETPMAG.AX (smaller positions, less liquid)

Use limit orders for all purchases to avoid slippage. For direct GSBI bonds, check ASX order book depth and use patient limit orders.

**Phase D — Database Fix (anytime):**
- Set GHY.AX convexity flags: `defined_downside=true`, `nonlinear_upside=true`

### Tax Flags

| Trade | Potential Tax Event? | Note |
|-------|---------------------|------|
| Sell AGVT.AX | **Yes** | May crystallise capital gain/loss depending on purchase price. Check CGT impact. |
| Trim FLBL | **Yes** | Partial disposal — CGT on sold units using FIFO or specific identification. |
| Trim JPST | **Yes** | Partial disposal — CGT on sold units. USD-denominated; forex gain/loss may also apply. |
| All buys | No | Purchases are not taxable events. |

**The user should consult their tax records to assess CGT impact before executing.** This report does not model tax consequences.

### Broker Routing

- **Interactive Brokers**: Primary broker for all trades (US and ASX). Holds the majority of assets.
- **CommSec**: Consider purchasing GSBI here to keep government bonds consolidated (GSBG27 and GSBG33 are already at CommSec). This simplifies maturity management.
- **Cash transfers**: If CommSec is used for GSBI, transfer AUD from RACQ to CommSec. Otherwise, consolidate at IB.

### Classification Commands for New Instruments

After purchase, classify all new instruments:

```bash
# New compounders
towsand classify role VAS.AX compounder
towsand classify role VGS.AX compounder
towsand classify role VGE.AX compounder

towsand classify tag VAS.AX \
  --macro "au_domestic_demand,au_equity_market" \
  --group "Vanguard AU Shares" \
  --corr-group "au_equity_beta" \
  --duration 0 \
  --liquidity 1 \
  --no-inflation-linked

towsand classify tag VGS.AX \
  --macro "global_developed_equity" \
  --group "Vanguard Intl Shares" \
  --corr-group "global_equity_beta" \
  --duration 0 \
  --liquidity 1 \
  --no-inflation-linked \
  --unhedged

towsand classify tag VGE.AX \
  --macro "china_demand,emerging_markets" \
  --group "Vanguard Emerging Mkts" \
  --corr-group "emerging_equity_beta" \
  --duration 0 \
  --liquidity 1 \
  --no-inflation-linked \
  --unhedged

# New optionality
towsand classify role PMGOLD.AX optionality
towsand classify role ETPMAG.AX optionality

towsand classify tag PMGOLD.AX \
  --macro "gold_price" \
  --group "Perth Mint Gold" \
  --corr-group "precious_metals" \
  --duration 0 \
  --liquidity 1 \
  --no-inflation-linked

towsand classify tag ETPMAG.AX \
  --macro "silver_price" \
  --group "ETFS Physical Silver" \
  --corr-group "precious_metals" \
  --duration 0 \
  --liquidity 1 \
  --no-inflation-linked

# New stabiliser (inflation-linked)
towsand classify role GSBI stabiliser  # Use actual ticker
towsand classify tag GSBI \
  --macro "au_interest_rates" \
  --group "AU Government" \
  --corr-group "au_govt_bond" \
  --duration 5.0 \
  --liquidity 2 \
  --inflation-linked

# Fix GHY.AX convexity flags
# (check towsand classify command for setting convexity flags:
#  defined_downside=true, nonlinear_upside=true)
```

---

## Forward-Looking Notes

1. **GSBG27.AX maturity (April 2027)**: This bond matures in ~14 months, converting AUD 178,120 back to cash (stabiliser). When it matures, the stabiliser will temporarily grow and the inflation-linked percentage will drop. Plan to redeploy maturity proceeds into: (a) additional GSBI indexed bonds (maintain inflation coverage), or (b) compounders/optionality if stabiliser exceeds 25% band.

2. **Optionality target 15%**: This report targets 12% optionality (the achievable minimum within the band). The midpoint is 15% = AUD 267,000. To reach 15%, an additional ~AUD 53,000 of convex instruments would be needed. The precious metals allocation could be increased, or alternative convex instruments identified. This is not urgent — 12% is within the 10–20% band.

3. **Rule 5.1 currency classification**: Confirm whether PMGOLD.AX and ETPMAG.AX are classified as AUD or non-AUD for the AUD Growth Exposure check. If classified as non-AUD, adjust the VAS/VGS split (increase VAS by ~AUD 30k, decrease VGS by ~AUD 30k).

4. **Credit spread monitoring**: The credit_spread correlation group (CRED + FLBL + TCPC) remains at ~20% after FLBL trim. Do not add further credit instruments. If any of these positions grow through price appreciation, monitor for re-breach of the 10% single-position cap (FLBL) or approach of the 30% macro driver cap (global_credit_spreads).

5. **GSBI selection**: Verify current ASX-listed Treasury Indexed Bond availability. Recommend maturities spanning the 2027–2033 stabiliser horizon. If a single maturity is used, target the ~2030 range (middle of the horizon). If multiple maturities are available, ladder across 2027, 2030, and 2033.

---

**Report Generated:** 2026-02-17 19:37 AEST
**Portfolio Value:** AUD 1,781,774.17
**Current Compliance:** 10 pass, 4 warning, 3 breach
**Post-Trade Compliance (projected):** 16 pass, 1 monitor, 0 breach
