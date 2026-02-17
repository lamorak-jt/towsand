---
description: Record a portfolio decision with structured metadata and compliance context
alwaysApply: false
---

# Log Decision

Walk through structured decision recording: what was done, why, which trigger, which rules, expected outcome.

**Command Format**: `/log-decision [optional: brief description]`

## Execution

### 1. Gather context

```bash
cd /home/jtlamorak/towsand && source .venv/bin/activate
towsand compliance --detail --no-save
```

### 2. Ask the user

If the user didn't provide enough detail, ask for:
- **What**: What action was taken or is being approved? (trade, rebalance, classification change, parameter change, rule override, review)
- **Trigger**: What prompted this? (rule_breach, income_shock, inflation_shift, currency_regime, correlation_convergence, discretionary)
- **Rationale**: Why this action specifically?

### 3. Record the decision

Use the CLI to store the decision:

```bash
# This uses direct Python since the CLI command may not exist yet
python3 -c "
from src.db.connection import get_connection
with get_connection() as conn:
    conn.execute('''
        INSERT INTO decisions (decision_type, trigger, summary, rationale, linked_rule_ids, recorded_by)
        VALUES (?, ?, ?, ?, ?, 'ai_agent')
    ''', ('TYPE', 'TRIGGER', 'SUMMARY', 'RATIONALE', '[\"RULE_IDS\"]'))
    decision_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    print(f'Decision #{decision_id} recorded')
"
```

### 4. Confirm

Show the user the recorded decision with all fields, and ask if any corrections are needed.

## Decision Types

- `rebalance` — shifting allocation between roles or positions
- `classification_change` — changing an instrument's capital role or tags
- `parameter_change` — changing system parameters (e.g. monthly expenses, income shock flag)
- `trade` — executing a buy or sell
- `rule_override` — knowingly accepting a compliance breach with rationale
- `review` — periodic review with no action taken (supports Rule 9.2 audit trail)

## Triggers

- `rule_breach` — a compliance breach was detected
- `income_shock` — income dropped >30% or visibility <6 months
- `inflation_shift` — structural change in inflation/rate regime
- `currency_regime` — material change in currency dynamics
- `correlation_convergence` — previously uncorrelated assets converging
- `discretionary` — user-initiated without a specific trigger
