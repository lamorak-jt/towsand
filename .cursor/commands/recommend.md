---
description: Generate buy/sell recommendations anchored to strategy and compliance
alwaysApply: false
---

# Recommend

Generate specific buy/sell recommendations to improve the portfolio's compliance and alignment with strategy objectives.

**Command Format**: `/recommend [optional: focus area like "optionality" or "reduce FLBL"]`

## Execution

### 1. Gather current state

```bash
cd /home/jtlamorak/towsand && source .venv/bin/activate

# Portfolio and compliance
towsand portfolio summary
towsand compliance --detail --no-save
towsand classify list
towsand portfolio exposures
```

### 2. Run objective-level analytics

```bash
cd /home/jtlamorak/towsand && source .venv/bin/activate

# Sensitivity: how fragile are the strategic objectives?
towsand sensitivity

# Stress: what happens to objectives under stress?
towsand stress
```

### 3. Read strategy context

Read these files:
- `current-finances/portfolio-management-rules.md` — rules and constraints
- `current-finances/strategy-assumptions.md` — strategy context
- `current-finances/classification-recommendations.md` — classification rationale and known issues

### 4. Identify gaps

Calculate the dollar gap for each dimension:
- **Role gaps**: target band midpoints vs actual (e.g. compounder target ~57.5%, actual 43.5% → need AUD X more)
- **Position size breaches**: how much to trim to get within cap
- **Missing exposures**: inflation-linked, optionality, etc.
- **Concentration risk**: what to reduce

### 5. Generate recommendations

For each recommendation, provide:

```markdown
### [Action]: [Ticker or Description]
- **Type**: Buy / Sell / Trim / Rebalance
- **Amount**: AUD approximate value
- **Role**: Which capital role this serves
- **Rules addressed**: Which compliance rules this fixes
- **Rationale**: Why this specific action, anchored to strategy documents
- **Constraints**: Any rules that limit this action (e.g. position size caps)
- **Risk note**: What risk this introduces or removes
```

### 6. Apply Rule 9.2 gate (no-action rule)

**Before generating any recommendations**, check whether action is warranted:

- **Breaches exist?** → action required (Rule 1.1 breach action: rebalance within 30 days)
- **Active trigger?** (income_shock_active, inflation_shift_active, currency_regime_active, correlation_convergence_active in parameters) → action required per Rule 9.1
- **Neither?** → Rule 9.2 applies: "Absent a trigger, no discretionary rebalancing." Report this explicitly and do NOT generate buy/sell recommendations. You may note observations for future reference but must not recommend action.

Warnings alone (without breaches or triggers) do not justify action — they are monitoring items.

### 7. Prioritise (when action IS warranted)

Order recommendations by:
1. **Fix breaches** — mandatory, 30-day deadline per rules
2. **Address trigger-driven concerns** — if a trigger is active, address the specific risk it signals
3. **Reduce warnings** — only if actions to fix breaches naturally also address warnings

### 8. Validate recommendations

Before presenting, check each recommendation against ALL rules:
- Does the buy create a new position size breach?
- Does it push a macro driver above 30%?
- Does it breach corporate group concentration?
- Does it change the currency balance?
- Does the sell trigger a taxable event? (flag, don't model)

### 8a. Stress-test the post-trade portfolio

After computing trade recommendations, create a trades JSON file and run both pre-trade and post-trade stress/sensitivity analysis:

```bash
# Write the trade deltas to a temp file
cat > /tmp/trades.json << 'EOF'
[
  {"ticker": "FLBL", "delta_aud": -120000},
  {"ticker": "VAS.AX", "delta_aud": 80000}
]
EOF

# Run pre/post comparison
towsand stress --trades /tmp/trades.json
towsand sensitivity --trades /tmp/trades.json
```

Substitute the actual recommended trades into the JSON. Each entry has `ticker` and `delta_aud` (+buy, -sell).

From the output, assess:

1. **Survivability**: Does the post-trade portfolio survive all stress scenarios without forced liquidation? If any scenario now forces selling, the recommendation **fails**.
2. **Income bridge**: Post-trade stabiliser covers how many months under stress? Compare to pre-trade.
3. **Compounding damage under stress**: How much more/less compounder capital is at risk post-trade? Compare recovery years.
4. **Optionality**: Is optionality now large enough that it materially offsets losses in stress?
5. **Fragility trade-offs**: If the recommendations create new tight constraints (e.g., Rule 5.1 at 50.4%), state explicitly: "This recommendation trades [X breach] for [Y fragility]. The fragility is acceptable because [reason]."

Include a **"Post-trade objective assessment"** section in the report with the pre/post comparison table from `towsand stress --trades`.

### 9. Output

Always save the recommendation report to `reports/` as:

```
reports/initial-recommendation-report-{YYMMDD_HHMM}.md
```

Where `{YYMMDD_HHMM}` is the current date and time (e.g. `initial-recommendation-report-260217_1430.md`).

The report must be a complete, standalone document including:
- Current compliance summary table
- All numbered recommendations with full detail (per step 4 format)
- Post-trade projection table (before vs after vs target)
- Validation against all rules
- Execution notes (sequence, pacing, broker routing, tax flags)

Present a summary in the conversation and confirm the file was saved.

## Notes

- Recommendations must be **specific and actionable** — not "consider adding equities" but "buy AUD 50,000 of VAS.AX (Vanguard Australian Shares ETF)"
- Always explain WHY a specific instrument is recommended over alternatives
- If the user specified a focus area, prioritise that but still note other issues
- Flag any recommendation where you're uncertain about instrument selection — the user should verify suitability
- Never recommend instruments that violate the "non-sophisticated investor" constraint (no options, warrants, futures, private assets)
- Reference the strategy documents and rules by section number
