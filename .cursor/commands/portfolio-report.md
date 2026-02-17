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

### 2. Read context documents

Read these files for strategic context:
- `current-finances/portfolio-management-rules.md` — the rules being enforced
- `current-finances/strategy-assumptions.md` — strategic context
- `current-finances/classification-recommendations.md` — current classification rationale

### 3. Analyse

Using the command output and context documents, analyse:

1. **Portfolio composition** — total value, breakdown by role/type/currency/country/institution
2. **Compliance status** — every pass/warning/breach with explanation in plain language
3. **Capital role assessment** — are roles correctly sized? What's driving any breaches?
4. **Risk concentrations** — position size issues, macro driver exposure, correlation groups, corporate group concentration
5. **Currency & hedging** — is the AUD/international split appropriate for the strategy?
6. **Stabiliser health** — liquidity, duration distribution, inflation coverage, expense coverage months
7. **Key concerns** — the 2-3 most important issues requiring action, ranked by urgency
8. **Deployment opportunities** — where should excess stabiliser (cash) be deployed?

### 4. Write report

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

### 5. Confirm

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
