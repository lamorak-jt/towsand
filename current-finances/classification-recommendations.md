# Instrument Classification Recommendations

**Date:** 2026-02-17
**Instruments:** 13 held (11 IB, 2 CommSec)
**Status:** Draft for review — no commands executed yet

---

## Portfolio Context

| Metric | Value |
|--------|-------|
| Total holdings (as of 2026-02-17) | AUD 1,239,868.57 |
| Total cash (as of 2026-02-17) | AUD 601,213.11 |
| Total portfolio (incl cash) | AUD 1,841,081.67 |
| Monthly expenses | AUD 9,000 |
| 24-month floor (Rule 2.1) | AUD 216,000 |
| Stabiliser band (Rule 1.1) | 15–25% of portfolio |
| Compounder band | 50–65% |
| Optionality band | 10–20% |

FX rates used: USD/AUD 1.4168, GBP/AUD 1.9293, EUR/AUD 1.6783

---

## 1. Capital Role Classifications

### Stabiliser (4 instruments + all cash, ~AUD 1,032,000)

| Ticker | Name | Type | Ccy | Approx AUD | Rationale |
|--------|------|------|-----|------------|-----------|
| AGVT.AX | BetaShares Aus Govt Bond ETF | etf | AUD | 95,473 | Diversified AUD government bond exposure. Core stabiliser — liquid, high-quality, rate-sensitive. |
| GSBG27.AX | AU Govt Bond Apr 2027 | govt_bond_nominal | AUD | 178,120 | Direct government bond maturing April 2027. Horizon-matched to the income-dependency window (strategy §2). Largest single stabiliser position. |
| GSBG33.AX | AU Govt Bond Apr 2033 | govt_bond_nominal | AUD | 35,448 | Direct government bond maturing April 2033. Provides duration beyond the income bridge, matching the 2027–2033 stabiliser horizon (strategy §3). |
| JPST | JPMorgan Ultra-Short Income ETF | etf | USD | 122,138 | Ultra-short duration (~0.5yr), near-zero credit risk. Functions as high-quality liquidity in USD. **Note:** USD denomination means this stabiliser carries currency risk against AUD living expenses — consider whether this is acceptable or whether it should be reclassified as compounder. |

**Stabiliser as % of total portfolio:** ~56.1% (above 15–25% band — driven by large cash allocation)
**Stabiliser as months of expenses:** ~114.8 months (well above 24-month floor)

**Interpretation (Rule 1.1a):** All cash balances are allocated to Stabiliser Capital. Cash satisfies every stabiliser criterion (liquid, short duration, yield-bearing) and does not meet the optionality convexity test (Rule 6.1). The strategic "dry powder" value of cash is a portfolio-level property tracked separately.

**Key concern:** Zero inflation-linked instruments in the stabiliser bucket. Rule 7.3 requires ≥25% of stabiliser in inflation-linked or real-rate sensitive instruments. This will be a **compliance warning** (per current implementation) until inflation-linked bonds (e.g. Treasury Indexed Bonds) are added.

---

### Compounder (8 instruments, ~AUD 801,400)

| Ticker | Name | Type | Ccy | Approx AUD | Rationale |
|--------|------|------|-----|------------|-----------|
| BHP.AX | BHP Group Ltd | equity | AUD | 169,696 | World's largest diversified miner. Durable business with high returns on capital, global commodity exposure, strong capital discipline. Core compounder — blue-chip global equity. |
| FLBL | Franklin Senior Loan ETF | etf | USD | 239,018 | Senior secured floating-rate bank loans. Provides credit income with near-zero duration risk. Return sourced from credit spread capture. Largest single position by AUD value — **position size (~13.0% of total portfolio) triggers Rule 3.1 breach vs the 10% cap.** |
| CRED.AX | BetaShares Aus IG Corp Bond ETF | etf | AUD | 126,861 | Investment grade AUD corporate bonds. Provides steady income with moderate credit risk. Not classified as stabiliser because (a) the strategy specifies government bonds for stabiliser (strategy §3), and (b) including it in stabiliser would push that bucket above 25%. Functions as a low-vol income generator within the compounder allocation. |
| SOL.AX | Washington H Soul Pattinson | equity | AUD | 74,300 | Australian investment conglomerate (coal via New Hope, telecoms via TPG, agriculture, financial services). Long track record of patient capital compounding. Diversified domestic exposure. |
| AGL.AX | AGL Energy Ltd | equity | AUD | 67,727 | Integrated energy utility (power generation, gas, retail). Stable revenue, high dividend yield. Exposure to Australian energy transition and domestic demand. |
| TCPC | BlackRock TCP Capital Corp | equity (BDC) | USD | 54,405 | Business Development Company — direct lending to US middle-market companies. Functionally a credit vehicle despite equity listing. Provides yield through credit spread income. |
| UKW | Greencoat UK Wind PLC | listed_fund | GBP | 51,757 | UK onshore/offshore wind farm investment trust. Long-duration operational infrastructure with partially inflation-linked revenue (UK power prices). Provides diversified income from real assets outside Australia. |
| ORG.AX | Origin Energy Ltd | equity | AUD | 17,640 | Energy company (power generation, LNG via APLNG stake, retail energy). Smaller compounder position with exposure to Australian energy markets and LNG export revenues. |

**Compounder as % of total portfolio:** ~43.5% (below 50–65% band — compliance breach)

---

### Optionality (1 instrument, ~AUD 7,300)

| Ticker | Name | Type | Ccy | Approx AUD | Rationale |
|--------|------|------|-----|------------|-----------|
| GHY.AX | Gold Hydrogen Ltd | equity | AUD | 7,285 | Early-stage hydrogen exploration company. Pre-revenue, binary outcome. **Conceptually** fits Optionality (binary upside, small size caps downside), but note the system currently requires explicit convexity flags in `instrument_classifications` to pass Rule 6.1 (see §9 addendum). **Should be flagged as speculative** (`is_speculative = true`). |

**Optionality as % of total portfolio:** ~0.4% (well below 10–20% band — compliance warning)

---

### Classification Decision Points

These deserve your explicit consideration:

1. **Cash-as-stabiliser (Rule 1.1a):** All cash is allocated to stabiliser for compliance purposes (see `portfolio-management-rules.md` §1.1a). This is because cash's return is linear yield, not a convex payoff — it fails the optionality convexity test (Rule 6.1) and is excluded by the yield exclusion rule (Rule 6.2). Cash satisfies all stabiliser criteria. The strategic "dry powder" value is a portfolio-level property, tracked separately.

2. **JPST as stabiliser vs. compounder:** It's functionally cash-like (ultra-short, high quality), but in USD — creating a currency mismatch against AUD expenses. With cash now in stabiliser, the stabiliser bucket is already overweight (~56%), so the JPST classification has less impact on band compliance. The question is conceptual: is USD liquidity part of your stabiliser or part of your growth capital?

3. **FLBL position size:** At ~13% of total portfolio, FLBL is the largest single position. Rule 3.1 caps single ETFs at 10%. This is a **compliance breach** regardless of classification.

4. **GHY.AX `is_speculative` flag:** Set to true in the database. Rule 3.1 caps speculative positions at 1% each, 3% aggregate. At ~0.4%, GHY.AX is within both caps.

---

## 2. Macro Driver Tags

Macro drivers per Rule 4.2 framework. Bold drivers are the named Rule 4.2 drivers with a 30% portfolio limit.

| Ticker | Macro Drivers | Notes |
|--------|--------------|-------|
| AGL.AX | `au_energy`, `au_domestic_demand` | Revenue tied to Australian electricity demand, gas prices, and energy policy. Not directly linked to the four named macro drivers. |
| AGVT.AX | `au_interest_rates` | Government bond ETF; value driven by RBA rate expectations and term premium. |
| BHP.AX | **`bulk_commodities`**, **`china_demand`** | Iron ore, copper, coal. Heavily tied to Chinese industrial demand cycle. |
| CRED.AX | **`global_credit_spreads`**, `au_interest_rates` | Investment grade bonds; sensitive to both domestic rate curve and credit spread movements. |
| FLBL | **`global_credit_spreads`**, `us_interest_rates` | Senior loans; floating rate eliminates duration but exposes to credit spread widening. |
| GHY.AX | `energy_transition` | Speculative hydrogen exploration. Driven by clean energy/hydrogen policy thesis. |
| GSBG27.AX | `au_interest_rates` | Short-duration nominal government bond. Rate-sensitive but nearing maturity. |
| GSBG33.AX | `au_interest_rates` | Longer-duration nominal government bond. More rate-sensitive. |
| JPST | `us_interest_rates` | Ultra-short USD; yield tracks Fed funds rate. Minimal spread exposure. |
| ORG.AX | `au_energy`, `au_domestic_demand` | Power generation + LNG (APLNG JV gives indirect gas/commodity exposure). |
| SOL.AX | `au_domestic_demand`, **`bulk_commodities`** | Conglomerate with significant coal exposure (New Hope), plus telecoms and financial services. |
| TCPC | **`global_credit_spreads`**, `us_private_credit` | BDC lending; credit cycle sensitive. Performs poorly in credit crunches. |
| UKW | `energy_transition`, `uk_inflation` | UK wind farm revenue linked to power prices (partially inflation-indexed). |

### Aggregate Macro Exposure (Rule 4.2 named drivers)

| Named Driver | Instruments | Combined Approx AUD | Approx % |
|-------------|-------------|---------------------|----------|
| **Bulk commodities** | BHP.AX, SOL.AX (partial) | ~207,000 | ~11% |
| **China demand** | BHP.AX | ~170,000 | ~9% |
| **Global credit spreads** | CRED.AX, FLBL, TCPC | ~420,000 | ~22% |
| **Australian housing** | (none) | 0 | 0% |

All named drivers are within the 30% limit. **Global credit spreads at ~22% is the highest concentration** — adding more credit instruments would approach the cap.

---

## 3. Corporate Groups

For Rule 3.2: no more than 20% exposed to a single corporate group.

| Ticker | Corporate Group | Notes |
|--------|----------------|-------|
| AGL.AX | `AGL Energy` | Single issuer |
| AGVT.AX | `AU Government` | Underlying is diversified AU govt bonds |
| BHP.AX | `BHP Group` | Single issuer |
| CRED.AX | `AU IG Corporate` | Diversified basket — no single issuer dominates |
| FLBL | `US Senior Loans` | Diversified basket of ~300+ senior loans |
| GHY.AX | `Gold Hydrogen` | Single issuer |
| GSBG27.AX | `AU Government` | Single sovereign issuer |
| GSBG33.AX | `AU Government` | Single sovereign issuer |
| JPST | `US Short Duration` | Diversified basket of short-term bonds |
| ORG.AX | `Origin Energy` | Single issuer |
| SOL.AX | `Soul Pattinson` | Single issuer (conglomerate holding company) |
| TCPC | `BlackRock TCP Capital` | Single issuer (BDC) |
| UKW | `Greencoat Capital` | Single issuer (investment trust) |

### Concentration Check

Percentages shown here are of **total portfolio value (incl cash)**, matching the compliance implementation.

| Corporate Group | Approx AUD | Approx % of total portfolio | Status |
|----------------|------------|----------|--------|
| AU Government | 309,040 | ~16.8% | OK (< 20%) |
| US Senior Loans | 239,018 | ~13.0% | OK (< 20%) |
| BHP Group | 169,696 | ~9.2% | OK |
| AU IG Corporate | 126,861 | ~6.9% | OK |
| US Short Duration | 122,138 | ~6.6% | OK |
| Soul Pattinson | 74,300 | ~4.0% | OK |
| AGL Energy | 67,727 | ~3.7% | OK |
| BlackRock TCP Capital | 54,405 | ~3.0% | OK |
| Greencoat Capital | 51,757 | ~2.8% | OK |
| Origin Energy | 17,640 | ~1.0% | OK |
| Gold Hydrogen | 7,285 | ~0.4% | OK |

**US Senior Loans (FLBL) is the largest single corporate-group exposure (~13% of total portfolio; ~19% of holdings).**

---

## 4. Stress Correlation Groups

For Rule 8.2: assets with >0.7 correlation in stress are treated as one risk for sizing.

| Correlation Group | Instruments | Rationale |
|------------------|-------------|-----------|
| `au_equity_beta` | BHP.AX, AGL.AX, ORG.AX, SOL.AX | All ASX-listed equities. High correlation in equity market sell-offs. |
| `au_govt_bond` | AGVT.AX, GSBG27.AX, GSBG33.AX | Flight-to-quality assets. Tend to rally (or hold) during equity stress. |
| `credit_spread` | CRED.AX, FLBL, TCPC | All credit-exposed instruments. Sell off together when credit spreads widen. |
| `us_short_duration` | JPST | Near-zero stress correlation. Ultra-short, high-quality. |
| `uk_infrastructure` | UKW | Partially idiosyncratic (operational wind farms, UK power prices). Some equity correlation in severe stress. |
| `speculative` | GHY.AX | Idiosyncratic pre-revenue equity. High beta but small position. |

**Key observation:** The `credit_spread` group represents ~AUD 420,000 (~23% of total portfolio; ~34% of holdings). Under Rule 8.2, these should be treated as one risk position for sizing purposes (and will likely trigger an 8.2 warning because it exceeds 20% of total portfolio).

---

## 5. Duration

Duration is most relevant for stabiliser instruments (Rule 7.2: no single duration point > 40% of stabiliser).

| Ticker | Duration (years) | Notes |
|--------|-----------------|-------|
| GSBG27.AX | 1.2 | Matures April 2027 |
| GSBG33.AX | 7.0 | Matures April 2033 |
| AGVT.AX | 5.5 | Composite government bond ETF duration |
| JPST | 0.5 | Ultra-short |
| CRED.AX | 3.0 | Investment grade corporate |
| FLBL | 0.25 | Floating rate — near-zero duration |
| TCPC | 0.3 | BDC — floating rate lending |
| UKW | 0 | Infrastructure fund — not rate duration |
| AGL.AX | 0 | Equity — no meaningful duration |
| BHP.AX | 0 | Equity — no meaningful duration |
| ORG.AX | 0 | Equity — no meaningful duration |
| SOL.AX | 0 | Equity — no meaningful duration |
| GHY.AX | 0 | Equity — no meaningful duration |

### Stabiliser Duration Distribution (Rule 7.2)

The compliance implementation for Rule 7.2 uses stabiliser **including cash** as the denominator. With current cash (~AUD 601k), no single duration bucket is close to 40%. This becomes more relevant once cash is deployed.

If stabiliser = AGVT.AX + GSBG27.AX + GSBG33.AX + JPST (holdings total ~AUD 431,000):

| Duration Bucket | Instrument | AUD | % of Stabiliser | Rule 7.2 (max 40%) |
|----------------|-----------|-----|-----------------|---------------------|
| Ultra-short (< 1yr) | JPST | 122,100 | 28% | OK |
| Short (1–2yr) | GSBG27.AX | 178,100 | 41% | **Breach (> 40%)** |
| Medium (5–6yr) | AGVT.AX | 95,500 | 22% | OK |
| Long (7yr+) | GSBG33.AX | 35,400 | 8% | OK |

**Note:** the table above is holdings-only. Once cash is included (as implemented), the GSBG27 bucket is well below 40% today.

---

## 6. Hedging (FX)

For Rule 5.2: ≥40% of international growth assets must be unhedged.

| Ticker | Currency | Hedged? | Notes |
|--------|----------|---------|-------|
| AGL.AX | AUD | N/A | Base currency — no FX exposure |
| AGVT.AX | AUD | N/A | Base currency |
| BHP.AX | AUD | N/A | AUD-listed but revenue is global (USD commodity prices). Implicitly unhedged to commodity FX. |
| CRED.AX | AUD | N/A | Base currency |
| FLBL | USD | **Unhedged** | USD exposure — no FX overlay |
| GHY.AX | AUD | N/A | Base currency |
| GSBG27.AX | AUD | N/A | Base currency |
| GSBG33.AX | AUD | N/A | Base currency |
| JPST | USD | **Unhedged** | USD exposure — no FX overlay |
| ORG.AX | AUD | N/A | Base currency |
| SOL.AX | AUD | N/A | Base currency |
| TCPC | USD | **Unhedged** | USD exposure — no FX overlay |
| UKW | GBP | **Unhedged** | GBP exposure — no FX overlay |

### International Exposure Summary

| Currency | AUD Value | % of Holdings |
|----------|-----------|---------------|
| USD (unhedged) | ~415,500 | ~34% |
| GBP (unhedged) | ~51,800 | ~4% |
| **Total international** | **~467,300** | **~38%** |
| **Of which unhedged** | **467,300** | **100%** |

Rule 5.2 requires ≥40% of international growth assets be unhedged → **100% is unhedged, so this is met.**
Rule 5.1 requires AUD 50–70% of growth capital → under the recommended roles above, AUD growth is ~AUD 463k of ~AUD 809k (~57%). **In band.**

---

## 7. Inflation Linkage

| Ticker | Inflation-Linked? | Notes |
|--------|-------------------|-------|
| AGVT.AX | No | Nominal government bonds |
| GSBG27.AX | No | Nominal government bond |
| GSBG33.AX | No | Nominal government bond |
| JPST | No | Nominal ultra-short |
| CRED.AX | No | Nominal corporate bonds |
| FLBL | No (partial) | Floating rate provides indirect inflation pass-through via rates, but not formally inflation-linked |
| UKW | No (partial) | UK wind revenue has partial inflation linkage through power prices, but not formally indexed |
| All equities | No | Equities have implicit real-asset characteristics but are not inflation-linked instruments |

**No instruments are formally inflation-linked.** Rule 7.3 requires ≥25% of stabiliser in inflation-linked instruments → **this is a compliance breach.** Consider adding Treasury Indexed Bonds (e.g. GSBI series on ASX) to the stabiliser.
**No instruments are formally inflation-linked.** Rule 7.3 requires ≥25% of stabiliser in inflation-linked instruments → **this is a compliance warning** (per current implementation). Consider adding Treasury Indexed Bonds (e.g. GSBI series on ASX) to the stabiliser.

---

## 8. Liquidity

| Ticker | Liquidity (days to exit) | Notes |
|--------|-------------------------|-------|
| BHP.AX | 1 | Very liquid large-cap |
| AGL.AX | 1 | Liquid ASX equity |
| ORG.AX | 1 | Liquid ASX equity |
| SOL.AX | 1 | Liquid ASX equity |
| AGVT.AX | 1 | Liquid ASX ETF |
| CRED.AX | 1 | Liquid ASX ETF |
| FLBL | 1 | Liquid US ETF |
| JPST | 1 | Very liquid US ETF |
| GSBG27.AX | 2 | Government bond — may need to work order |
| GSBG33.AX | 2 | Government bond — may need to work order |
| TCPC | 2 | NASDAQ-listed BDC — moderate volume |
| UKW | 2 | LSE-listed investment trust — moderate volume |
| GHY.AX | 5 | Small-cap — thin order book, potential slippage |

### Stabiliser Liquidity (Rule 7.1)

Rule 7.1 requires ≥70% of stabiliser liquid within 5 trading days.

| Instrument | AUD | Liquid in 5 days? |
|-----------|-----|-------------------|
| AGVT.AX | 95,500 | Yes (1 day) |
| GSBG27.AX | 178,100 | Yes (2 days) |
| GSBG33.AX | 35,400 | Yes (2 days) |
| JPST | 122,100 | Yes (1 day) |
| **Total** | **431,100** | **100% liquid in 5 days** |

Rule 7.1: **Pass** (100% > 70%).

---

## 9. CLI Commands to Execute

Once you've reviewed and approved the classifications above, run these commands:

### Capital Roles

```bash
towsand classify role AGVT.AX stabiliser
towsand classify role GSBG27.AX stabiliser
towsand classify role GSBG33.AX stabiliser
towsand classify role JPST stabiliser
towsand classify role BHP.AX compounder
towsand classify role FLBL compounder
towsand classify role CRED.AX compounder
towsand classify role SOL.AX compounder
towsand classify role AGL.AX compounder
towsand classify role TCPC compounder
towsand classify role UKW compounder
towsand classify role ORG.AX compounder
towsand classify role GHY.AX optionality
```

### Tags (macro drivers, corporate groups, duration, hedging)

```bash
# Stabiliser instruments
towsand classify tag AGVT.AX \
  --macro "au_interest_rates" \
  --group "AU Government" \
  --corr-group "au_govt_bond" \
  --duration 5.5 \
  --liquidity 1 \
  --no-inflation-linked

towsand classify tag GSBG27.AX \
  --macro "au_interest_rates" \
  --group "AU Government" \
  --corr-group "au_govt_bond" \
  --duration 1.2 \
  --liquidity 2 \
  --no-inflation-linked

towsand classify tag GSBG33.AX \
  --macro "au_interest_rates" \
  --group "AU Government" \
  --corr-group "au_govt_bond" \
  --duration 7.0 \
  --liquidity 2 \
  --no-inflation-linked

towsand classify tag JPST \
  --macro "us_interest_rates" \
  --group "US Short Duration" \
  --corr-group "us_short_duration" \
  --duration 0.5 \
  --liquidity 1 \
  --no-inflation-linked \
  --unhedged

# Compounder instruments
towsand classify tag BHP.AX \
  --macro "bulk_commodities,china_demand" \
  --group "BHP Group" \
  --corr-group "au_equity_beta" \
  --duration 0 \
  --liquidity 1 \
  --no-inflation-linked

towsand classify tag FLBL \
  --macro "global_credit_spreads,us_interest_rates" \
  --group "US Senior Loans" \
  --corr-group "credit_spread" \
  --duration 0.25 \
  --liquidity 1 \
  --no-inflation-linked \
  --unhedged

towsand classify tag CRED.AX \
  --macro "global_credit_spreads,au_interest_rates" \
  --group "AU IG Corporate" \
  --corr-group "credit_spread" \
  --duration 3.0 \
  --liquidity 1 \
  --no-inflation-linked

towsand classify tag SOL.AX \
  --macro "au_domestic_demand,bulk_commodities" \
  --group "Soul Pattinson" \
  --corr-group "au_equity_beta" \
  --duration 0 \
  --liquidity 1 \
  --no-inflation-linked

towsand classify tag AGL.AX \
  --macro "au_energy,au_domestic_demand" \
  --group "AGL Energy" \
  --corr-group "au_equity_beta" \
  --duration 0 \
  --liquidity 1 \
  --no-inflation-linked

towsand classify tag TCPC \
  --macro "global_credit_spreads,us_private_credit" \
  --group "BlackRock TCP Capital" \
  --corr-group "credit_spread" \
  --duration 0.3 \
  --liquidity 2 \
  --no-inflation-linked \
  --unhedged

towsand classify tag UKW \
  --macro "energy_transition,uk_inflation" \
  --group "Greencoat Capital" \
  --corr-group "uk_infrastructure" \
  --duration 0 \
  --liquidity 2 \
  --no-inflation-linked \
  --unhedged

towsand classify tag ORG.AX \
  --macro "au_energy,au_domestic_demand" \
  --group "Origin Energy" \
  --corr-group "au_equity_beta" \
  --duration 0 \
  --liquidity 1 \
  --no-inflation-linked

# Optionality instrument
towsand classify tag GHY.AX \
  --macro "energy_transition" \
  --group "Gold Hydrogen" \
  --corr-group "speculative" \
  --duration 0 \
  --liquidity 5 \
  --no-inflation-linked
```

---

## 10. Expected Compliance Issues After Classification

With all cash allocated to stabiliser (Rule 1.1a), `towsand compliance` reports:

| Rule | Status | Issue |
|------|--------|-------|
| 1.1-S Stabiliser band | **Breach** | Stabiliser ~56% vs. 15–25% target. Driven by large cash allocation — indicates underdeployment into compounders and optionality. |
| 1.1-C Compounder band | **Breach** | Compounder ~43% vs. 50–65% target. Mirror of the stabiliser overweight. |
| 1.1-O Optionality band | **Warning** | Optionality ~0.4% vs. 10–20% target. Significantly under-allocated. |
| 3.1 Position size (FLBL) | **Breach** | FLBL at ~13% of portfolio exceeds 10% single-position cap. |
| 6.1 Convexity test (GHY.AX) | **Breach** | GHY.AX scores 0/3 on payoff shape unless convexity flags are explicitly set. |
| 7.3 Inflation coverage | **Warning** | 0% of stabiliser in inflation-linked instruments vs. 25% requirement. |
| 8.2 Correlation stress | **Warning** | Credit spread correlation group at ~23% — concentrated risk as single position. |

---

## 11. Notes for Future Actions

1. **Deploy cash into compounders and optionality** — stabiliser at ~56% and compounder at ~43% means the portfolio is significantly underdeployed relative to the strategy's growth objectives. The cash allocation represents "dry powder" that should be systematically deployed.
2. **Inflation-linked bonds** are the most urgent gap — consider adding ASX-listed Treasury Indexed Bonds (GSBI series) to stabiliser. Rule 7.3 requires ≥25% of stabiliser in inflation-linked instruments.
3. **FLBL overweight** needs addressing — either partial trim or reclassification of the 10% rule for diversified ETFs (the intent of Rule 3.1 is idiosyncratic risk, which is lower for a 300+ loan ETF).
4. **Optionality underweight** is significant — the current portfolio has almost no asymmetric/convex exposure beyond the tiny GHY.AX position (~0.4% vs 10–20% band).
5. **AUD hedging** for international positions: all international exposure is unhedged (100%), which exceeds Rule 5.2's minimum (40%). This is compliant but note there's no hedged international exposure at all — consider whether this is intentional.
