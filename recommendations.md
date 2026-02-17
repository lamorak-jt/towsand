# Instrument Classification Recommendations

Based on the **Portfolio Management Rules** and **Strategy Assumptions**, here are the recommended classifications for the 13 identified instruments.

## Summary of Roles

*   **Stabiliser:** Strictly AUD Government Bonds (Nominal & Indexed) to cover liability matching (2027–2033).
*   **Compounder:** The growth engine; durable businesses, credit, and income generators.
*   **Optionality:** Asymmetric payoffs, convex upside, or specific speculative bets (capped at 1-3%).

---

## Detailed Classifications

### 1. AGL Energy (AGL.AX)
*   **Role:** `compounder`
    *   *Reasoning:* Established utility, cash-generative, part of the core equity portfolio.
*   **Tags:**
    *   Macro Drivers: `["Australian Energy", "Wholesale Power Prices"]`
    *   Corporate Group: `AGL Group`
    *   Duration: `Equity`
    *   Hedging: `AUD`

### 2. BetaShares Aus Gov Bond ETF (AGVT.AX)
*   **Role:** `stabiliser`
    *   *Reasoning:* Fits the strict definition of Stabiliser capital (AUD Government Bonds) for liquidity and defensive ballast.
*   **Tags:**
    *   Macro Drivers: `["AUD Rates"]`
    *   Corporate Group: `Australian Government`
    *   Duration: `7.5 years` (approx avg duration of AGVT)
    *   Hedging: `AUD`

### 3. BHP Group (BHP.AX)
*   **Role:** `compounder`
    *   *Reasoning:* Global resource major, core portfolio holding.
*   **Tags:**
    *   Macro Drivers: `["Bulk Commodities", "China Demand"]`
    *   Corporate Group: `BHP Group`
    *   Duration: `Equity`
    *   Hedging: `AUD`

### 4. BetaShares Investment Grade Corp Bond (CRED.AX)
*   **Role:** `compounder`
    *   *Reasoning:* While defensive, it is Corporate Credit, not Government. It carries credit risk and fits better as a yield-generating Compounder than a risk-free Stabiliser.
*   **Tags:**
    *   Macro Drivers: `["Global Credit Spreads", "AUD Credit Spreads"]`
    *   Corporate Group: `Diversified`
    *   Duration: `4.5 years` (approx avg duration)
    *   Hedging: `AUD`

### 5. Gold Hydrogen (GHY.AX)
*   **Role:** `optionality`
    *   *Reasoning:* Speculative, pre-revenue exploration. Fits the "convex payoff" profile (binary outcome) and the "Speculative" cap rules.
*   **Tags:**
    *   Macro Drivers: `["Energy Transition", "Speculative Exploration"]`
    *   Corporate Group: `Gold Hydrogen`
    *   Duration: `Equity`
    *   Hedging: `AUD`

### 6. Origin Energy (ORG.AX)
*   **Role:** `compounder`
    *   *Reasoning:* Core energy utility and LNG exposure.
*   **Tags:**
    *   Macro Drivers: `["Australian Energy", "LNG Prices", "Oil"]`
    *   Corporate Group: `Origin Energy`
    *   Duration: `Equity`
    *   Hedging: `AUD`

### 7. Washington H Soul Pattinson (SOL.AX)
*   **Role:** `compounder`
    *   *Reasoning:* Diversified investment house, long-term compounder track record.
*   **Tags:**
    *   Macro Drivers: `["Diversified", "Coal", "Australian Property"]`
    *   Corporate Group: `Soul Pattinson Group`
    *   Duration: `Equity`
    *   Hedging: `AUD`

### 8. Greencoat UK Wind (UKW)
*   **Role:** `compounder`
    *   *Reasoning:* Infrastructure yield play with inflation linkage.
*   **Tags:**
    *   Macro Drivers: `["UK Power Prices", "UK Inflation"]`
    *   Corporate Group: `Greencoat`
    *   Duration: `Equity`
    *   Hedging: `Unhedged` (GBP exposure)

### 9. Franklin Senior Loan ETF (FLBL)
*   **Role:** `compounder`
    *   *Reasoning:* Floating rate senior loans. Income generation.
*   **Tags:**
    *   Macro Drivers: `["Global Credit Spreads", "US Rates"]`
    *   Corporate Group: `Diversified`
    *   Duration: `0.2 years` (Floating rate duration is low, credit duration is higher)
    *   Hedging: `Unhedged` (USD exposure)

### 10. JPMorgan Ultra-Short Income (JPST)
*   **Role:** `compounder`
    *   *Reasoning:* Cash management / Short-term income. Not Stabiliser because it is USD and credit-based, not AUD Gov.
*   **Tags:**
    *   Macro Drivers: `["US Rates"]`
    *   Corporate Group: `Diversified`
    *   Duration: `0.5 years`
    *   Hedging: `Unhedged` (USD exposure)

### 11. BlackRock TCP Capital Corp (TCPC)
*   **Role:** `compounder`
    *   *Reasoning:* BDC (Business Development Corp), high yield credit exposure.
*   **Tags:**
    *   Macro Drivers: `["US Credit Spreads", "SME Credit"]`
    *   Corporate Group: `BlackRock TCP`
    *   Duration: `Equity`
    *   Hedging: `Unhedged` (USD exposure)

### 12. AU Govt Bond Apr 2027 (GSBG27.AX)
*   **Role:** `stabiliser`
    *   *Reasoning:* Direct AUD Government Bond liability matching.
*   **Tags:**
    *   Macro Drivers: `["AUD Rates"]`
    *   Corporate Group: `Australian Government`
    *   Duration: `1.2 years`
    *   Hedging: `AUD`

### 13. AU Govt Bond Apr 2033 (GSBG33.AX)
*   **Role:** `stabiliser`
    *   *Reasoning:* Direct AUD Government Bond liability matching.
*   **Tags:**
    *   Macro Drivers: `["AUD Rates"]`
    *   Corporate Group: `Australian Government`
    *   Duration: `7.2 years`
    *   Hedging: `AUD`

---

## Recommended Commands

```bash
# Roles
towsand classify role AGL.AX compounder
towsand classify role AGVT.AX stabiliser
towsand classify role BHP.AX compounder
towsand classify role CRED.AX compounder
towsand classify role GHY.AX optionality
towsand classify role ORG.AX compounder
towsand classify role SOL.AX compounder
towsand classify role UKW compounder
towsand classify role FLBL compounder
towsand classify role JPST compounder
towsand classify role TCPC compounder
towsand classify role GSBG27.AX stabiliser
towsand classify role GSBG33.AX stabiliser

# Tags (Example format - adjust syntax if CLI requires specific flags for tags)
# Assuming 'towsand classify tag <ticker> --macro <drivers> --group <group> --duration <years> --hedging <status>'
# Or if it's interactive, these are the values to input.

# AGL
towsand classify tag AGL.AX --macro "Australian Energy" --group "AGL Group" --duration "Equity" --hedging "AUD"

# AGVT
towsand classify tag AGVT.AX --macro "AUD Rates" --group "Australian Government" --duration 7.5 --hedging "AUD"

# BHP
towsand classify tag BHP.AX --macro "Bulk Commodities, China Demand" --group "BHP Group" --duration "Equity" --hedging "AUD"

# CRED
towsand classify tag CRED.AX --macro "Global Credit Spreads" --group "Diversified" --duration 4.5 --hedging "AUD"

# GHY
towsand classify tag GHY.AX --macro "Energy Transition, Speculative" --group "Gold Hydrogen" --duration "Equity" --hedging "AUD"

# ORG
towsand classify tag ORG.AX --macro "Australian Energy, LNG" --group "Origin Energy" --duration "Equity" --hedging "AUD"

# SOL
towsand classify tag SOL.AX --macro "Diversified, Coal" --group "Soul Pattinson Group" --duration "Equity" --hedging "AUD"

# UKW
towsand classify tag UKW --macro "UK Power, Inflation" --group "Greencoat" --duration "Equity" --hedging "Unhedged"

# FLBL
towsand classify tag FLBL --macro "Global Credit Spreads" --group "Diversified" --duration 0.2 --hedging "Unhedged"

# JPST
towsand classify tag JPST --macro "US Rates" --group "Diversified" --duration 0.5 --hedging "Unhedged"

# TCPC
towsand classify tag TCPC --macro "US Credit Spreads" --group "BlackRock TCP" --duration "Equity" --hedging "Unhedged"

# GSBG27
towsand classify tag GSBG27.AX --macro "AUD Rates" --group "Australian Government" --duration 1.2 --hedging "AUD"

# GSBG33
towsand classify tag GSBG33.AX --macro "AUD Rates" --group "Australian Government" --duration 7.2 --hedging "AUD"
```
