# Property Capital — Phase 1: Tax & Income Baseline

**Date:** 2026-08-16
**Plan ref:** `project/260816-plan.md`, Phase 1
**Author:** Towsand research (agent)
**Status:** Phase 1 deliverable (revised). Establishes the tax and income baseline against which Phase 2–7 are evaluated.
**Revision note:** This version applies the user-supplied 100% franking assumption for SOL, BHP, VAS, AGL and ORG; retains a clearly labeled 30% VGS/VGE foreign-tax planning assumption; and models no private patient hospital cover, spouse taxable income of AUD 95,000, and two dependants in the family MLS test. The FY2026–27 tax bands remain planning assumptions pending final ATO-table confirmation.

> **Bottom line up front.** Under the plan's confirmed assumptions — Property Capital owned by you individually; Australian tax resident; **you have no employment income**; your spouse receives the secure AUD 5,500/month net income (which reduces the household deficit but is **not** part of your taxable income); ~AUD 50k carried-forward capital losses — the AUD 70,596 household deficit is coverable at a blended Property Capital gross yield that is **well below the tested 3.5–5.5% range in every sensitivity**.
>
> | Sensitivity (FY2026–27) | Blended cash-income breakeven yield |
> |---|---:|
| Core (100% franking + no PHI; current base) | **2.24%** |
| Core, **no franking** (conservative bound) | 2.64% |
| Core, no franking **and** no PHI | 2.64% |
| Defensive (100% franking + no PHI; current defensive case) | **3.00%** |
| Defensive, no franking + no PHI | 3.23% |
>
> Two effects drive the low hurdle: (1) with no employment income in your name, the tax-free threshold is fully available to portfolio income; (2) franking credits on the Long-Term equity portfolio materially reduce tax at these income levels. With the supplied 100% franking assumption, the core breakeven is ~2.24%; removing franking entirely raises it to ~2.64%. No hospital cover does not change the breakeven because combined family income remains below the planning MLS threshold at the breakeven.
>
The precise breakeven remains subject to a few tax-detail refinements. The principal unresolved inputs are the actual company/ETF franking components, the VGS/VGE AMMA foreign-income/foreign-tax split, the final FY2026–27 tax and MLS tables, and the final FITO-limit calculation. The supplied no-PHI status, spouse taxable income of AUD 95,000, two dependants, and confirmed bond coupons are already incorporated. Until the tax-detail inputs are finalized, treat the figures above as a **planning range** (core ≈ 2.2–2.6%, defensive ≈ 3.0–3.2%), all below the 3.5% floor. The strategic implication is robust regardless: **optimize Property Capital for capital preservation, AUD matching, and liquidity first; yield second.**

---

## 1. Inputs and data sources

| Input | Value | Source / status |
|---|---|---|
| Holdings, units, cost bases | DB `holdings` | `data/towsand.db` (IB Flex + CommSec), 2026-08-14/16 |
| Market prices (AUD items) | 2026-08-14 close | DB `prices` (`ib_flex`) |
| Bond prices (GSBG27/33) | 2026-08-16 close | DB `prices` (`yfinance`) |
| FX: USD/AUD 1.4115, GBP/AUD 1.9104, EUR/AUD 1.6332 | 2026-08-14 | DB `fx_rates` (`ib_flex`) |
| Trailing-12m cash distributions per unit | yfinance dividend history | actual ex-date payments; **cash timing only — not tax character** |
| Forward distribution estimates | Conservative, analyst-set | see §1.1; BHP haircut for cyclicality |
| **Franking percentages** | 100% assumed for SOL/BHP/VAS/AGL/ORG | User supplied planning assumption; confirm final statements/AMMA when available |
| **VGS/VGE foreign income & foreign tax** | 30% foreign-tax gross-up | Reasonable planning assumption; AMMA would refine components but is not expected to change the decision |
| **Bond coupons** | 4.75% GSBG27; 4.50% GSBG33 | Confirmed from AOFM; YTM captured in Phase 2 |
| **MLS inputs** | no PHI; spouse taxable AUD 95k; two dependants | User supplied; family MLS modeled using combined income |
| Household deficit | AUD 70,596/yr | `strategy-assumptions.md` §3 (net of spouse's secure income) |
| Property Capital target | AUD 2,200,000 | `strategy-assumptions.md` §2 |
| Carried-forward capital losses | ~AUD 50,000 | plan (Given) |

**Holdings snapshot (market value, AUD):**

| Ticker | Units | Role | Market value (AUD) |
|---|---:|---|---:|
| SOL.AX | 6,200 | Long-Term | 288,486 |
| BHP.AX | 3,200 | Long-Term | 196,320 |
| VAS.AX | 1,500 | Long-Term | 169,380 |
| VGS.AX | 1,100 | Long-Term | 180,895 |
| VGE.AX | 1,316 | Long-Term | 124,125 |
| AGL.AX | 6,550 | Long-Term | 57,771 |
| ORG.AX | 1,500 | Long-Term | 18,105 |
| UKWl | 28,464 | Long-Term | 60,359 |
| GHY.AX | 20,522 | Long-Term (optionality) | 11,287 |
| **Long-Term subtotal** | | | **1,106,728** |
| GSBG27.AX | 1,742 | Property Capital | 177,196 |
| GSBG33.AX | 349 | Property Capital | 34,952 |
| CRED.AX | 4,930 | Property Capital | 112,355 |
| **Existing PC subtotal** | | | **324,503** (14.8% of 2.2m target) |
| FLBL | 2,300 | Transitional (USD) | 74,863 |
| JPST | 1,000 | Transitional (USD) | 71,281 |

Roles follow `recommendations.md` and the plan's Phase 3 treatment.

---

## 2. Section 1.1 — Expected portfolio income inventory

Per-unit trailing-12m (TTM) figures are **actual cash distributions** from yfinance. **Important limitation:** yfinance establishes only cash amount and timing — it does **not** establish Australian tax components (franked/unfranked split, franking credits), foreign income tax offsets, or capital-gains components. Those require the funds' annual AMMA statements and the companies' dividend statements. Where tax components are shown below they are **assumed and clearly marked**, pending those statements.

| Ticker | TTM cash (AUD) | Fwd net cash (AUD) | Income kind | Frank % (assumed) | Fwd gross (AUD) | Fwd WH (AUD) | Fwd taxable (AUD) | Fwd franking credit (AUD) | Foreign tax credit (AUD) | Reliability |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| SOL.AX | 6,634 | 6,510 | AU franked dividend | 100%⚠ | 6,510 | 0 | 9,300 | 2,790 | 0 | High |
| BHP.AX | 6,265 | 5,120 | AU franked dividend | 100%⚠ | 5,120 | 0 | 7,314 | 2,194 | 0 | Cyclical |
| VAS.AX | 4,879 | 4,800 | AU franked dividend | 100% | 4,800 | 0 | 6,857 | 2,057 | 0 | High |
| VGS.AX | 2,241 | 2,200 | Foreign ETF (AU-domiciled) | 0% | 3,143⚠ | 0 | 3,143 | 0 | 943⚠ | High |
| VGE.AX | 2,143 | 1,974 | Foreign ETF (AU-domiciled) | 0% | 2,820⚠ | 0 | 2,820 | 0 | 846⚠ | Moderate (lumpy) |
| AGL.AX | 3,210 | 3,144 | AU franked dividend | 100%⚠ | 3,144 | 0 | 4,491 | 1,347 | 0 | Moderate |
| ORG.AX | 900 | 825 | AU franked dividend | 100% | 825 | 0 | 1,179 | 354 | 0 | Moderate |
| UKWl | 5,731 | 5,438 | Foreign dividend (UK) | 0% | 5,438 | 0 | 5,438 | 0 | 0 | Moderate |
| GHY.AX | 0 | 0 | pre-revenue equity | — | 0 | 0 | 0 | 0 | 0 | None |
| CRED.AX | 5,974 | 5,916 | Interest (AUD IG credit) | 0% | 5,916 | 0 | 5,916 | 0 | 0 | High |
| GSBG27.AX | 8,275 | 8,275 | Govt coupon (4.75%✅) | 0% | 8,275 | 0 | 8,275 | 0 | 0 | High (contractual) |
| GSBG33.AX | 1,571 | 1,571 | Govt coupon (4.50%✅) | 0% | 1,571 | 0 | 1,571 | 0 | 0 | High (contractual) |
| FLBL | 5,594 | 4,691 | US senior-loan interest | 0% | 5,519 | 828⚠ | 5,519 | 0 | 828⚠ | Moderate (transition) |
| JPST | 2,987 | 2,520 | US ultra-short interest | 0% | 2,964 | 445⚠ | 2,964 | 0 | 445⚠ | High (transition) |

⚠ = **analyst assumption / placeholder, not directly sourced from an AMMA or dividend statement.** The current planning assumptions are 100% franking for the five Australian holdings and 30% foreign-tax gross-up for VGS/VGE; see §7.

**Notes on the plan's "pay particular attention" list:**

- **SOL** — TTM 107¢/share, 100% franked as supplied. Forward 105¢ (conservative, ~flat). Anchor equity income.
- **BHP** — TTM 195.77¢/share AUD. **Not annualized:** latest single dividend (103.85¢) × 2 would overstate. Forward **160¢/share** (~18% below TTM) reflects cyclicality and the plan's caution. 100% franking is the supplied planning assumption. Largest distribution-reliability risk.
- **VAS / VGS / VGE** — quarterly. VAS is modeled as 100% franked per the user's planning input. VGS/VGE unfranked foreign income use a reasonable 30% foreign-tax gross-up assumption; the AMMA would separate foreign income, foreign income tax offsets, discounted capital gains, and other components. yfinance is used only for cash timing.
- **CRED** — monthly interest (~10¢/unit), ~5.3% cash distribution yield. Property Capital interest (unfranked).
- **FLBL / JPST** — USD ETFs; included for inventory completeness but **excluded from the steady-state model** (Phase 3 flags both for sale/replacement; unhedged USD fails the AUD requirement). Their capital migrates into Property Capital and is captured via the blended Property yield. Withholding: 15% US WH assumed (W-8BEN filed — confirm); the WH is creditable as a foreign income tax offset. The IB transaction statement (which records actual withholding entries) is a better source than yfinance for these — use it when available.
- **UKWl** — Long-Term only (per plan §3.2); UK dividends bear **0% UK withholding** to a non-resident, so no foreign tax credit and no franking. Do not sell solely for the tax loss.
- **Government-bond coupons** — **CONFIRMED from AOFM (14 Aug 2026):** GSBG27 (Treasury Bond 4.75% 21 April 2027, ISIN AU3TB0000135) has a coupon of **4.75%**, not 4.50% as previously assumed. GSBG33 (Treasury Bond 4.50% 21 April 2033, ISIN AU000XCLWAG2) has a coupon of **4.50%**, confirmed as previously assumed. The corrected GSBG27 cash income is AUD 8,275 (1,742 units × AUD 100 face × 4.75%), an increase of AUD 436 from the 4.50% assumption. The combined existing PC cash income increases from AUD 15,326 to approximately AUD 15,762. **Yield to maturity** is now confirmed from RBA F16 (12 Aug 2026): GSBG27 YTM = 4.586%, GSBG33 YTM = 4.769%. See Phase 2 market scan for full details.

**Return-of-capital / AMMA components:** not separately modelled. ETF distributions can include discounted-capital-gain and return-of-capital components that alter taxable income; confirm against annual AMMA statements.

---

## 3. Section 1.2 — Personal tax model

**Financial year:** the modeled income is prospective from August 2026, so the base year is **FY2026–27** (1 Jul 2026 – 30 Jun 2027). The Stage-3 rate reduction taking effect from 1 July 2026 lowers the AUD 18,201–45,000 band from 16% to **15%**. Using the prior 16% rate overstated tax by a maximum of ~AUD 268/yr; the corrected rates lower the breakevens slightly.

**FY2026–27 resident tax brackets (as applied):**

| Band (AUD) | Rate |
|---|---:|
| 0 – 18,200 | 0% |
| 18,201 – 45,000 | **15%** |
| 45,001 – 135,000 | 30% |
| 135,001 – 190,000 | 37% |
| 190,001 + | 45% |

> ⚠ **Confirm the full FY2026–27 schedule against the ATO's published 2026–27 tax tables**, including any CPI indexation of the AUD 18,200 / 45,000 thresholds and the position of the 37% / 45% thresholds. This report applies the 15% rate to the AUD 18,200–45,000 band (per the legislated Stage-3 reduction) and retains the Stage-3 thresholds for the higher bands; if thresholds were also indexed/shifted, the figures move by small amounts.

Plus Medicare levy 2%. The Low Income Tax Offset (max AUD 700) is fully phased out well below the modeled taxable incomes (all > AUD 99,000), so it has **no effect** on any scenario. Franking credits are **refundable**; the foreign income tax offset is **non-refundable** (reduces tax to zero, cannot create a refund).

**Taxable income composition (steady-state forward year):**

1. **Australian interest** — Property Capital interest (deposits, term deposits, bond coupons, credit distributions) + CRED. All ordinary income, unfranked.
2. **Australian unfranked distributions** — unfranked portion of VAS, ORG.
3. **Franked dividends + grossed-up franking credits** — SOL, BHP, AGL, franked portion of VAS, ORG (gross-up 30%; credit = franked cash × 3/7). **Franking percentages are assumed — confirm.**
4. **Foreign dividends and interest** — VGS, VGE (grossed up for foreign tax per AMMA), UKWl (no foreign tax). FLBL/JPST excluded from steady state (sold in transition).
5. **Foreign tax offsets** — VGS/VGE foreign tax uses a reasonable 30% gross-up assumption and is claimed as non-refundable FITO; full FITO availability is assumed in the planning model pending AMMA and tax-return calculation. FLBL/JPST US WH (15%, creditable) — relevant to transition year only.
6. **Realized capital gains** — **AUD 0** in the steady-state year (no planned disposals).
7. **Carried-forward capital losses** — see (6): **zero current-year impact**. Capital losses cannot offset interest, dividends, or ordinary income. (See the corrected wording in §6.5 / Appendix B: the transition disposals of FLBL/UKWl at current values would *add* to losses, not consume the carried balance.)
8. **CGT discounts** — relevant only to transition disposals (Phase 3).
9. **Medicare levy (2%) and Medicare Levy Surcharge** — the 2% levy applies. The current base case assumes no private patient hospital cover and includes MLS whenever combined family income crosses the planning threshold, using the applicable tier. No-MLS rows are retained only as calculation controls. MLS family testing includes **both spouses'** taxable income — see §7 item 4.

**Endogenous effective rate.** With no employment income, portfolio income is taxed from AUD 0; the first AUD 18,200 is tax-free and the next AUD 26,800 is only 15%. As Property yield rises, taxable income is pushed through the 30% band and into the 37% band (above AUD 135,000). The effective total rate therefore rises from ~15.4% at 3.5% yield to ~21.1% at 5.5% yield (core) — the progressive-band effect the plan requires.

---

## 4. Section 1.3 — True fixed-income income requirement

**Starting deficit:** AUD 70,596/yr. This already nets out your spouse's AUD 5,500/month secure net income, so the portfolio's job is to cover the residual AUD 70,596. Your spouse's income is **not** in your taxable income (you own the portfolio individually and have no employment income) — this attribution is **confirmed** (see §7 item 1, now resolved).

**Long-Term (equity) portfolio income, forward:**

| Case | Cash distributions (AUD) | Taxable (AUD, grossed-up) | Franking credits (AUD) | Foreign tax (AUD) |
|---|---:|---:|---:|---:|
| Core | 30,011 | 40,542 | 8,742 | 1,789 |
| Defensive | 17,739 | 23,943 | 5,121 | 1,083 |

> **Conceptual note (important):** Australian tax is progressive, so there is **no unique standalone "after-tax equity income"** once Property Capital income is added — the tax attributable to the equity slice depends on the marginal band it falls in after Property income is stacked. The table below is therefore **descriptive only**: it shows the tax result *if the equity income were your only taxable income*. It must **not** be treated as an independently additive after-tax amount. The actual breakeven is solved from the integrated model in §5.

| Case | Equity cash (AUD) | Equity taxable (AUD) | Income tax (AUD) | Medicare (AUD) | − Franking (AUD) | − FITO (AUD) | **Net tax** (AUD) | **"After-tax" if equity-only** (AUD) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Core | 30,011 | 40,542 | 3,351 | 811 | 8,742 | 1,789 | −6,369 (refund) | 36,380 |
| Defensive | 17,739 | 23,943 | 861 | 479 | 5,121 | 1,083 | −4,864 (refund) | 22,603 |

In both cases the equity portfolio, assessed on its own, generates a **net tax refund** because franking credits exceed the tax + Medicare due. *(The equity-only figures are descriptive only and are not used as additive inputs to the integrated breakeven.)*

**Defensive case definition:** equity distributions cut materially — BHP −60%, SOL −30%, VAS/VGS −30%, VGE −50%, AGL/ORG −50%, UKWl −40%. GHY nil throughout.

**Existing Property Capital cash distribution.** The three existing PC-eligible holdings (GSBG27, GSBG33, CRED; AUD 324,503, 14.8% of target) generate **AUD 15,762/yr of cash distributions** — a **cash distribution yield of ~4.9%**, not a yield-to-maturity or expected total return. For the bonds trading above par, part of the coupon income is economically offset at redemption (the bond redeems at face, below its current price), so cash income exceeds economic return. **Do not treat 4.7% as a return anchor** — Phase 2 computes YTM. This cash is *inside* the AUD 2.2m blended-yield model below (not added on top).

**Breakeven blended Property Capital gross cash-income yield (surplus = 0 vs AUD 70,596), FY2026–27:**

| Sensitivity | Breakeven gross yield | Implied gross PC income (AUD) |
|---|---:|---:|
| **Core (100% franking + no PHI)** | **2.24%** | 49,334 |
| Core, no franking | 2.64% | 58,077 |
| Core, no franking + no PHI | 2.64% | 58,077 |
| **Defensive (100% franking + no PHI)** | **3.00%** | 65,933 |
| Defensive, no franking | 3.14% | 69,000 |
| Defensive, no franking + no PHI | 3.23% | 71,060 |

All breakevens sit **below** the 3.5% floor of the plan's test range. Operating Capital (AUD 105,894) is not drawn in any tested scenario.

---

## 5. Deliverable — Tax & income table

Blended Property Capital gross cash-income yield is applied to the full AUD 2.2m Property Capital target as cash income (deposits + Commonwealth + semis + credit), all ordinary/interest income. This is a cash-flow variable, not a yield-to-maturity or expected-total-return measure. "Other portfolio income" = Long-Term equity cash distributions (net of foreign withholding). "Tax" = net tax after franking credits and FITO, including Medicare 2%. MLS is separately modeled where combined family income exceeds the planning threshold. "Net household income" = Property cash + Other cash − net tax − MLS. "Deficit/surplus" = Net household income − AUD 70,596. **FY2026–27 planning bands.**

### Core case (100% franking assumption, no PHI; current base case)

| Blended Property cash-income yield | Property cash income (AUD) | Other portfolio income (AUD) | Taxable income (AUD) | Owner tax (AUD) | MLS (AUD) | Net household income (AUD) | Deficit / surplus (AUD) | Effective tax rate |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3.5% | 77,000 | 30,011 | 117,542 | 17,602 | 1,175 | 88,233 | +17,637 | 15.0% |
| 4.0% | 88,000 | 30,011 | 128,542 | 21,122 | 1,285 | 95,603 | +25,007 | 16.4% |
| 4.5% | 99,000 | 30,011 | 139,542 | 24,960 | 1,395 | 102,655 | +32,059 | 17.9% |
| 5.0% | 110,000 | 30,011 | 150,542 | 29,250 | 1,505 | 109,255 | +38,659 | 19.4% |
| 5.5% | 121,000 | 30,011 | 161,542 | 33,540 | 1,615 | 115,855 | +45,259 | 20.8% |

### Defensive case (100% franking assumption, no PHI; current defensive case)

| Blended Property cash-income yield | Property cash income (AUD) | Other portfolio income (AUD) | Taxable income (AUD) | Owner tax (AUD) | MLS (AUD) | Net household income (AUD) | Deficit / surplus (AUD) | Effective tax rate |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3.5% | 77,000 | 17,739 | 100,943 | 16,618 | 0 | 78,121 | +7,525 | 16.5% |
| 4.0% | 88,000 | 17,739 | 111,943 | 20,138 | 0 | 85,601 | +15,005 | 18.0% |
| 4.5% | 99,000 | 17,739 | 122,943 | 23,658 | 1,229 | 91,852 | +21,256 | 19.2% |
| 5.0% | 110,000 | 17,739 | 133,943 | 27,178 | 1,339 | 99,222 | +28,626 | 20.3% |
| 5.5% | 121,000 | 17,739 | 144,943 | 31,394 | 1,449 | 105,896 | +35,300 | 21.7% |

### Sensitivity — Core, no franking (conservative bound; franked dividends treated as unfranked ordinary income, no credits, no gross-up)

| Blended Property cash-income yield | Property cash income (AUD) | Other portfolio income (AUD) | Taxable income (AUD) | Tax (AUD) | Net household income (AUD) | Deficit / surplus (AUD) | Effective tax rate |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3.5% | 77,000 | 30,011 | 108,800 | 23,547 | 83,464 | +12,868 | 21.6% |
| 4.0% | 88,000 | 30,011 | 119,800 | 27,067 | 90,944 | +20,348 | 22.6% |
| 4.5% | 99,000 | 30,011 | 130,800 | 30,587 | 98,424 | +27,828 | 23.4% |
| 5.0% | 110,000 | 30,011 | 141,800 | 34,583 | 105,428 | +34,832 | 24.4% |
| 5.5% | 121,000 | 30,011 | 152,800 | 38,873 | 112,138 | +41,542 | 25.4% |

Removing all franking raises the core breakeven by approximately **+0.40pp** (2.24% → 2.64%) — consistent with the review estimate of ~0.3–0.4pp. The deficit remains covered at every tested yield.

### MLS treatment — no private patient hospital cover

The family MLS test uses Jacob's taxable income plus the spouse's supplied AUD 95,000 taxable income, with two dependants. Using a conservative AUD 210,000 planning family threshold before any dependant uplift and tiered MLS rates, MLS is zero below the threshold, approximately 1% above the threshold and up to 1.25 times the threshold, approximately 1.25% up to 1.5 times the threshold, and 1.5% above 1.5 times the threshold. The resulting MLS amounts are included in the core and defensive tables above and in the CSV. At the core and defensive breakevens, family income remains below the threshold, so no-PHI does not change either breakeven. The threshold, dependant uplift, and final rate schedule should be checked against the applicable ATO table when filing rules are published.

Supporting CSV artifacts: `reports/property-capital-phase1-income-inventory.csv` (14 rows, with gross/withholding/net/foreign-tax-credit columns and assumption notes), `reports/property-capital-phase1-tax-income-table.csv` (40 rows: current no-PHI base cases, no-franking sensitivities, and explicit no-MLS controls).

---

## 6. Findings and implications for later phases

1. **The income hurdle is lower than the strategy document's 4.0–4.8%, robustly.** Across the updated cash-income sensitivities (core 2.24–2.64%, defensive 3.00–3.23%), the breakeven is below the 3.5% floor. Phase 2–7 should **optimize for capital preservation, AUD matching, and liquidity first, yield second** — there is no need to chase 5%+ at the cost of credit or duration risk.
2. **Franking remains material, but the planning input is now supplied.** Modeling 100% franking for SOL, BHP, VAS, AGL and ORG produces a core hurdle of ~2.24%; removing all franking moves it to ~2.64%. Confirming final statements/AMMA remains useful for tax filing, but is unlikely to alter the portfolio decision.
3. **BHP is the dominant income-reliability risk** (~21% of TTM equity cash, cyclical). Defensive already cuts it 60%; Phase 6 combined stress should test a deeper cut.
4. **Capital losses are correctly inert here**, with corrected wording: the AUD 50k carried loss is reserved for Phase 3; transition disposals of FLBL/UKWl (currently at unrealized losses) would *add* to available losses, not consume the carried balance. Losses offset only capital gains from other strategically justified disposals — they do not justify an otherwise-bad sale.
5. **Existing Property Capital** (AUD 324.5k) is a solid cash-income anchor (~4.9% **cash distribution yield**) but is only 14.8% of target; the bulk must be built from the residual EUR conversion (Phase 3.1) and AUD cash deployment. Do not anchor Phase 2 expectations to the 4.9% cash figure — use Phase 2 YTM.

---

## 7. Blocking inputs and flags

**Remaining verification inputs (not expected to change the portfolio decision):**

1. **Income attribution — RESOLVED/CONFIRMED.** You own the portfolio individually; you have no employment income; your spouse receives the AUD 5,500/month net income, which reduces the household deficit but is **not** in your taxable income. No remaining conflict. *(Suggestion: `strategy-assumptions.md` could say "secure net income of the non-owner spouse" for clarity.)* The stale `seed.py` parameters (`income_amount=11000`, `monthly_expenses=9000`) should be updated to match the strategy docs.
2. **Franking percentages — planning input supplied.** The model now uses 100% for SOL, BHP, VAS, AGL and ORG. Final dividend statements/AMMA statements can refine the filing position.
3. **VGS/VGE AMMA annual tax statements — residual refinement.** The model uses a reasonable 30% foreign-tax gross-up assumption. The AMMA would separate foreign income, foreign income tax offsets, discounted capital gains, and other components; use it for the final return, but it is not decision-critical for portfolio selection.
4. **MLS — supplied and modeled.** No PHI, spouse taxable income AUD 95,000, and two dependants are now included. The family threshold, any two-dependant uplift, and tier boundaries remain subject to final ATO confirmation; MLS is calculated from combined family income rather than applying a blanket rate.
5. **Bond coupons — RESOLVED.** Confirmed from AOFM (14 Aug 2026): GSBG27 = 4.75% (ISIN AU3TB0000135), GSBG33 = 4.50% (ISIN AU000XCLWAG2). YTM confirmed from RBA F16 (12 Aug 2026): GSBG27 = 4.586%, GSBG33 = 4.769%. See Phase 2 market scan for full AGS yield curve.

**Other flags (lower priority):**

6. **ETF AMMA components** (capital-gain / return-of-capital split) — confirm at tax time; not separately modelled.
7. **FY2026–27 bracket schedule** — this means the progressive tax-rate bands, not a separate user input. The model uses 0% to AUD 18,200, 15% to AUD 45,000, 30% to AUD 135,000, 37% to AUD 190,000, then 45%. Confirm the final ATO thresholds/rates when filing tables are available.
8. **US withholding (W-8BEN)** — FLBL/JPST assumed 15%; confirm via IB statement (which also records the actual withholding entries — preferred source over yfinance). Transition-year effect only.
9. **DB parameters stale** — `seed.py` `monthly_expenses`/`income_amount` contradict the strategy docs (see item 1).

---

## Appendix A — Methodology and worked example (core, 4.5% yield, FY2026–27)

- Property income = 2,200,000 × 4.5% = AUD 99,000 (all ordinary/interest).
- Other (equity) cash = 30,011; grossed-up taxable = 40,542 (franking credits 8,742 + foreign gross-up 1,789).
- Total taxable = 139,542.
- Income tax by band:
  - 15% × (45,000 − 18,200) = 4,020
  - 30% × (135,000 − 45,000) = 27,000
  - 37% × (139,542 − 135,000) = 1,680
  - Total income tax = 32,701
- Medicare = 2% × 139,542 = 2,791. Gross tax + Medicare = 35,491.
- FITO = min(1,789, 35,491) = 1,789 → **full FITO assumed available**; tax after FITO = 33,702. The precise FITO limit requires the AMMA components and tax-return calculation.
- Franking credits = 8,742 → owner tax = 33,702 − 8,742 = **24,960**.
- MLS at 4.5%: approximately AUD 1,395 under the 1% family tier.
- Net household income = (99,000 + 30,011) − 24,960 − 1,395 = 102,655.
- Surplus = 102,655 − 70,596 = +32,059.

Note the taxable income (139,542) crosses into the 37% band (above 135,000); the marginal Property-Capital dollar at 4.5% yield is taxed at 37%, which is why the effective rate accelerates toward the top of the tested range. The table now also includes family MLS because the supplied spouse taxable income takes combined family income above the planning threshold at this yield.

## Appendix B — Capital-loss wording (corrected)

At current values, **JPST is around break-even, while FLBL and UKWl carry unrealized capital losses** (FLBL: cost USD 24.27/share vs price USD 23.06; UKWl: cost GBP 1.345/share vs price GBP 1.11 — AUD figures depend on the acquisition-date FX). Selling FLBL/UKWl therefore **adds** to the available capital-loss pool; it does **not** consume the carried-forward AUD 50k. Correct statement:

> The existing ~AUD 50k carried-forward capital loss, plus any new realized losses from transition disposals (FLBL, UKWl, and any FX-driven loss on JPST), will be available to offset capital gains from other strategically justified disposals. They do not offset interest, dividends, or ordinary distributions, and they remain inert in the steady-state income model.

The breakeven is unaffected (losses are inert in the steady state); this correction is to the descriptive wording only.

## Appendix C — What is *not* in this baseline

- No Phase 2 market data (deposit/bond/credit/semis/indexed yields) — captured on a single date in Phase 2.
- No transition-year tax (JPST/FLBL/UKWl disposals, EUR conversion, capital-loss application) — Phase 3.
- No portfolio construction, normalization, stress testing, or final instrument selection — Phases 4–7.
- No drawdown of Operating Capital modelled (not needed: surplus in all tested scenarios).
- No spouse tax return modeling (her income is excluded from your taxable income; only the MLS family test references it, as a sensitivity).
