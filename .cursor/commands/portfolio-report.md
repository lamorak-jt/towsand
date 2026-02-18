---
description: Run full portfolio analysis and write a dated report to reports/
alwaysApply: false
---

# Portfolio Report

Generate a comprehensive portfolio analysis report. Run all available data, compliance checks, and analytical tools, then write a structured markdown report.

**Command Format**: `/portfolio-report [optional focus area]`

## Execution

### 1. Gather data

Run these commands and capture the output. Do NOT theorise — run the actual commands.

```bash
# Activate the environment first
cd /home/jtlamorak/towsand && source .venv/bin/activate

# Current portfolio valuation
towsand portfolio value

# Portfolio allocation summary
towsand portfolio summary

# Classification status
towsand classify list

# Compliance check (with detail)
towsand compliance --detail --no-save

# FX rates
towsand fx list

# Latest prices
towsand prices list

# Exposure analysis
towsand portfolio exposures
```

### 2. Run objective-level analytics

```bash
cd /home/jtlamorak/towsand && source .venv/bin/activate

# Sensitivity: how fragile are the strategic objectives?
towsand sensitivity

# Stress: what happens to objectives under historical drawdowns?
towsand stress --detail

# Correlations: does diversification work when it matters?
towsand correlations --detail
```

If the report includes trade recommendations, also run pre/post comparison:

```bash
# Create trades JSON from recommendations, then:
towsand stress --trades /tmp/trades.json --detail
towsand sensitivity --trades /tmp/trades.json
```

### 3. Read context documents

Read these files for strategic context:
- `current-finances/portfolio-management-rules.md` — the rules being enforced
- `current-finances/strategy-assumptions.md` — strategic context
- `current-finances/classification-recommendations.md` — current classification rationale

### 4. Analyse

Using the command output and context documents, analyse:

1. **Portfolio composition** — total value, breakdown by role/type/currency/country/institution
2. **Compliance status** — every pass/warning/breach with explanation in plain language
3. **Constraint fragility** — which rules are tightest? What market moves would breach them? Include the `towsand sensitivity` output as a fragility table.
4. **Stress scenario pass/fail** — for each scenario (flat 35%, COVID 2020, GFC 2008, 2022 rate shock): which constraints breach? Is Rule 8.1 (forced liquidation) triggered? Include the `towsand stress` output as a stress results table.
5. **Correlation validation** — are the stress correlation groups (au_equity_beta, credit_spread, etc.) validated by actual price data? Flag any mismatches from `towsand correlations`.
6. **Capital role assessment** — are roles correctly sized? What's driving any breaches?
7. **Risk concentrations** — position size issues, macro driver exposure, correlation groups, corporate group concentration
8. **Currency & hedging** — is the AUD/international split appropriate for the strategy?
9. **Stabiliser health** — liquidity, duration distribution, inflation coverage, expense coverage months
10. **Key concerns** — the 2-3 most important issues requiring action, ranked by urgency
11. **Deployment opportunities** — where should excess stabiliser (cash) be deployed?

### 5. Write report

Create the report at `reports/YYYY-MM-DD-portfolio-report.md` using today's date.

Structure:

```markdown
# Portfolio Report — YYYY-MM-DD

## Executive Summary
[3-5 bullet points: total value, compliance status, key finding, top action]

## Portfolio Composition
[Table of holdings with AUD values, role, type]
[Table of cash balances]
[Role allocation with band targets]

## Compliance Status
[Table: rule | status | detail]
[Plain-language explanation of each warning and breach]

## Objective-Level Sensitivity
[From `towsand sensitivity` — assess each objective:]
- Income bridge: how many months covered, what market move breaks it
- Forced liquidation: how far from selling long-term assets
- Compounding at risk: AUD damage and recovery years per 10%/35% decline
- AUD liability matching: how much non-AUD outperformance weakens it
- Optionality sizing: is crisis insurance large enough to matter?

## Stress Scenario Results
[From `towsand stress --detail` — for each scenario, report against objectives:]
- Survivability: forced to sell? YES/NO
- Income bridge: months of expenses still covered
- Compounding damage: AUD lost + years to recover at 6.5% real
- Optionality payoff: did it perform its crisis function?
- Real wealth: total AUD impact
[Per-scenario holding-level drawdowns as supporting detail]

## Diversification Quality
[From `towsand correlations --detail`:]
- Does stabiliser protect against compounder losses in stress?
- Does optionality provide crisis alpha?
- Are compounders truly diversified or the same bet wearing different tickers?
- Flagged pairs: hidden concentration or over-estimated groupings

## Risk Analysis
### Position Concentration
### Macro Driver Exposure
### Correlation Groups
### Currency Exposure

## Stabiliser Assessment
[Expense coverage, liquidity, duration distribution, inflation gap]

## Key Concerns & Recommended Actions
[Numbered list, most urgent first, with specific actionable steps]

## Appendix: Raw Data
[FX rates, price dates, data freshness notes]
```

### 6. Confirm

After writing the report, show the user:
- The file path
- The executive summary
- The top 3 recommended actions

## Notes

- Always use **actual command output**, never estimate or assume values
- All monetary values in AUD unless stated otherwise
- Reference specific rules by number (e.g. "Rule 3.1") when discussing compliance
- If prices or FX rates are stale (>5 trading days old), flag this prominently
- If any command fails, report the error and work with available data
- The report should be self-contained — readable without needing to run any commands
