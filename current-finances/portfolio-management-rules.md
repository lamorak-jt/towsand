# Portfolio Management Rules

## One-Sentence Summary

This strategy prioritises survivability, real purchasing power, and asymmetric upside, using explicit income reliance, disciplined role-based capital allocation, and intentional currency exposure — rather than implicit assumptions or yield-driven comfort.

---

## 0. Investable Assets Definition

All percentage-based rules (role bands, position size, concentration limits, currency bands) use **investable assets** as the denominator. Investable assets are defined as:

**Included:**
- All instrument holdings at current market value (AUD-converted)
- All cash and deposit balances (bank accounts, broker cash, multi-currency wallets)

**Excluded:**
- Receivables and debts owed to the family (e.g. personal loans outstanding) — these are not liquid, not market-priced, and their recovery timing is uncertain
- Credit card liabilities — these are operational cash-flow items, not investment positions; they are expected to be settled monthly from income
- Primary residence equity — explicitly excluded per Strategy §1 ("housing equity is treated as illiquid and excluded from portfolio risk budgeting")
- Employment income / human capital — not a financial asset

**Implementation:** Cash balances with `account_type = 'credit'` or accounts tagged as receivables are excluded from the investable-assets denominator. The `parameters` table stores `exclude_account_ids` as a JSON list of account IDs to exclude.

---

## 1. Capital Role Constraints (Top-Level)

### 1.1 Role Allocation Bands

- **Stabiliser Capital:** 15–25% of investable assets
- **Compounder Capital:** 50–65%
- **Optionality Capital:** 10–20%

**Breach action:** rebalance within 30 days unless driven by market moves <10%.

### 1.1a Cash Allocation Interpretation

All cash balances are allocated to **Stabiliser Capital** for the purpose of role band compliance. Rationale:

- Cash satisfies every stabiliser criterion: liquid (instant), short duration (zero), yield-bearing (deposit interest).
- Cash does not satisfy the Optionality convexity test (Rule 6.1): its return is linear yield, not a convex payoff shape. Rule 6.2 explicitly excludes yield-dominant instruments from the optionality bucket.
- The strategic value of cash as "dry powder" (the option to deploy into dislocations) is a portfolio-level property, not an instrument payoff characteristic. This is tracked separately but does not override the instrument-level classification.
- Role allocation bands are calculated against total portfolio value (holdings + cash). Cash is included in the stabiliser numerator and in the denominator.

### Why

- Preserves liquidity and downside control.
- Prevents optionality or conviction positions from crowding out durability.

---

## 2. Income Dependency Constraints

### 2.1 Income Substitution Rule

Stabiliser capital must be sufficient to fund **≥24 months of core living expenses** without employment income.

**Clarification:**

- **Rule 2.1 (absolute) becomes primary:** Stabiliser capital must fund ≥24 months of core living expenses.
- **Rule 1.1 (percentage) becomes conditional:** Stabiliser capital should be 15–25% of the portfolio once the absolute expense-coverage requirement is met.

Or, more formally:

```
Stabiliser allocation = max(
  • 24 months of core expenses,
  • 15–25% of portfolio value
)
```

### 2.2 Income Shock Trigger

If any occur:
- Net income ↓ >30%, or
- Forward income visibility <6 months

Then:
- Freeze new risk deployment.
- Shift toward top of stabiliser band.
- Optionality allocation capped at 10%.

### Why

- Converts income reliance into a mechanical rule.
- Removes discretion under stress.

---

## 3. Position Size Constraints

### 3.1 Single Security Caps

- Max single listed equity: **10%** of total portfolio
- Max single credit instrument: **7%**
- Speculative / pre-revenue assets: **1%** each, **3%** aggregate

### 3.2 Issuer Concentration

No more than **20%** exposed to a single corporate group or economic driver.

### Why

- Prevents idiosyncratic risk from dominating outcomes.
- Forces diversification without diluting conviction.

---

## 4. Macro Factor Exposure Constraints

### 4.1 Australia Concentration

Max AUD-domiciled risk assets: **55%** (excludes AUD government bonds)

### 4.2 Single Macro Driver

Exposure to any one of:
- Australian housing (not including the residence)
- Bulk commodities
- China demand
- Global credit spreads

must not exceed **30%** of portfolio value.

### Why

- Avoids portfolio failure from one narrative breaking.
- Forces intentional macro bets.

---

## 5. Currency Exposure Constraints

### 5.1 Currency Bands (Growth Capital Only)

- **AUD exposure:** 50–70%
- **Non-AUD exposure:** 30–50%

### 5.2 Hedging Rule

- At least **40%** of international growth assets must be unhedged.
- Hedging may increase tactically, but never reach 100%.

### Why

- Balances liability matching with regime insurance.
- Prevents hidden AUD over-concentration.

---

## 6. Optionality Constraints (Convexity Rules)

### 6.1 Payoff Shape Test

Optionality capital must satisfy **two of three**:

- Defined downside (premium or capped loss)
- Non-linear upside (>3x in favourable regime)
- Stress-period outperformance

### 6.2 Yield Exclusion Rule

Instruments whose expected return is predominantly sourced from carry/yield/spread compression (i.e., the upside is mainly linear and the downside is not tightly bounded) may not exceed **25%** of the optionality bucket.

Instruments where carry is incidental to a convex payoff profile (e.g., protection that benefits from volatility/dislocation) are permitted, provided they satisfy Rule 6.1 (Convexity Test).

### Why

- Prevents "false optionality".
- Keeps the bucket purpose-pure.

---

## 7. Stabiliser Constraints

### 7.1 Liquidity Rule

**≥70%** of stabiliser assets must be liquid within 5 trading days at low spread cost.

### 7.2 Duration Rule

Weighted duration aligned to:
- Income bridge horizon
- No single duration point >40% of stabiliser capital.

### 7.3 Inflation Coverage

**≥25%** of stabiliser in inflation-linked or real-rate sensitive instruments.

### Why

- Ensures stabiliser functions when needed, not just on paper.

---

## 8. Drawdown & Correlation Constraints

### 8.1 Drawdown Tolerance

Portfolio must be constructed such that a **35% equity market drawdown** does not force liquidation of long-term assets.

### 8.2 Correlation Stress Rule

Assets with **>0.7 correlation** in stress periods are treated as one risk for sizing purposes.

### Why

- Correlation rises when it matters.
- This prevents false diversification.

---

## 9. Review & Enforcement Rules

### 9.1 Review Triggers (Only These)

- Income shock
- Structural inflation shift
- Currency regime change
- Correlation convergence
- Rule breach >30 days

### 9.2 No Action Rule

Absent a trigger, no discretionary rebalancing.

### Why

- Eliminates over-management.
- Keeps the framework dominant over emotion.
