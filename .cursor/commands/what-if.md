---
description: Model a hypothetical trade and report impact on compliance and allocation
alwaysApply: false
---

# What-If

Model a hypothetical trade or portfolio change and report its impact on compliance, allocation, and risk.

**Command Format**: `/what-if <description of proposed change>`

Examples:
- `/what-if sell 3000 units of FLBL and buy VAS.AX`
- `/what-if add $100k of Treasury Indexed Bonds to stabiliser`
- `/what-if FLBL drops 20%`

## Execution

### 1. Capture current state

```bash
cd /home/jtlamorak/towsand && source .venv/bin/activate
towsand portfolio summary
towsand compliance --detail --no-save
```

### 2. Parse the proposed change

From the user's description, identify:
- Instruments affected (ticker, amount/quantity, buy/sell/price change)
- If a new instrument: research it briefly (type, currency, country, likely capital role, macro drivers)
- If a market move: apply percentage change to relevant holdings

### 3. Model the impact

Calculate the portfolio **after** the change:
- New holding values (adjusted quantities × current prices × FX)
- New role allocations (recalculate stabiliser/compounder/optionality percentages)
- New position sizes as % of total
- New macro driver exposures
- New currency split

### 4. Run compliance mentally

Check every rule against the post-change portfolio:
- Role bands (1.1)
- Income substitution (2.1)
- Position size caps (3.1, 3.2)
- Macro exposure (4.1, 4.2)
- Currency bands (5.1, 5.2)
- Optionality constraints (6.1, 6.2)
- Stabiliser constraints (7.1, 7.2, 7.3)
- Drawdown tolerance (8.1)

### 5. Present comparison

```markdown
## What-If: [description]

### Before → After

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total portfolio | ... | ... | ... |
| Stabiliser % | ... | ... | ... |
| Compounder % | ... | ... | ... |
| Optionality % | ... | ... | ... |
| [affected position] % | ... | ... | ... |

### Compliance Impact

| Rule | Before | After | Notes |
|------|--------|-------|-------|
| [only rules that change] | ... | ... | ... |

### Assessment

[1-3 sentences: does this improve the portfolio? What trade-offs?]
```

## Notes

- This is a **read-only analysis** — do NOT modify the database
- Use `--no-save` flag on compliance to avoid storing hypothetical snapshots
- If the user proposes something that creates a new breach, clearly flag it
- If the user proposes something that fixes breaches, quantify the improvement
