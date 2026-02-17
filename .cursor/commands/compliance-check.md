---
description: Run compliance checks and explain breaches in plain language with suggested fixes
alwaysApply: false
---

# Compliance Check

Run the compliance engine and explain results in plain language, with specific suggested fixes for any warnings or breaches.

## Execution

### 1. Run compliance

```bash
cd /home/jtlamorak/towsand && source .venv/bin/activate
towsand compliance --detail
```

### 2. Read rules

Read `current-finances/portfolio-management-rules.md` for the rule definitions being checked.

### 3. Explain results

For each result:
- **Pass**: brief confirmation (one line)
- **Warning**: explain what's happening, why it matters, and what to do about it
- **Breach**: explain the breach clearly, quantify the gap, and give specific actionable steps to resolve it (e.g. "sell AUD X of FLBL" or "buy AUD Y of inflation-linked bonds")

### 4. Prioritise

Rank all warnings and breaches by urgency:
1. Breaches that increase risk (position size, correlation) — fix first
2. Breaches that reduce growth (underweight compounders/optionality) — fix next
3. Warnings that represent missing diversification (inflation, correlation)

### 5. Output

Present directly in the conversation — do NOT write a file. Use clear formatting:

```
## Compliance Summary
[X pass, Y warning, Z breach]

## Breaches (fix within 30 days)
### [Rule ID] — [Rule Name]
...

## Warnings (address at next review)
### [Rule ID] — [Rule Name]
...

## Passes
[Brief list]

## Recommended Fix Priority
1. ...
2. ...
```
