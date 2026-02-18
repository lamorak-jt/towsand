---
description: Test portfolio against strategic objectives under stress — survivability, income bridge, compounding damage, diversification
alwaysApply: false
---

# Stress Test

Test whether the portfolio achieves its strategic objectives under adversity. The question is NOT "do we still follow our rules?" — it's "do we succeed or fail on what actually matters?"

**Command Format**: `/stress-test [optional: "sensitivity" or "correlations" or scenario name]`

## Strategic Objectives Being Tested

From `current-finances/strategy-assumptions.md`:

1. **Survivability** — No forced liquidation of long-term assets under any scenario (§7)
2. **Income bridge** — Can fund 24+ months of living expenses without employment (§2)
3. **Compounding preservation** — Compounder capital survives to compound over 20+ years (§3)
4. **Optionality payoff** — Crisis insurance performs when the base case fails (§5)
5. **Regime resilience** — Diversification works when it matters, not just on paper (§7)

## Execution

### 1. Gather current state

```bash
cd /home/jtlamorak/towsand && source .venv/bin/activate
towsand portfolio summary
towsand compliance --detail --no-save
```

### 2. Run objective-level analytics (current portfolio)

```bash
# Sensitivity: how fragile are the objectives to market moves?
towsand sensitivity

# Stress: what happens to objectives under historical drawdowns?
towsand stress --detail

# Correlations: does diversification actually work in a crisis?
towsand correlations --detail
```

### 2a. Pre/post trade comparison (if trades are being evaluated)

If there are pending trade recommendations, create a trades JSON file and compare:

```bash
# Write trade deltas to JSON (substitute actual recommended trades)
cat > /tmp/trades.json << 'EOF'
[
  {"ticker": "FLBL", "delta_aud": -120000},
  {"ticker": "VAS.AX", "delta_aud": 80000}
]
EOF

# Pre-trade vs post-trade comparison
towsand stress --trades /tmp/trades.json --detail
towsand sensitivity --trades /tmp/trades.json
```

This shows: for each stress scenario, how do the recommended trades change survivability, income bridge coverage, compounding damage, and optionality payoff? The comparison table shows pre-trade vs post-trade side by side with deltas.

### 3. Read strategy context

Read `current-finances/strategy-assumptions.md` — the objectives being tested.

### 4. Present findings by objective, not by rule

Structure the response around the five objectives:

**For each objective, answer the question directly:**

1. **Survivability:** "In [worst scenario], are you forced to sell long-term assets?" YES or NO with dollar amounts.
2. **Income bridge:** "After a GFC-level drawdown, how many months of expenses can you fund?" Number, with commentary on the buffer.
3. **Compounding damage:** "A 35% equity drawdown destroys AUD X of compounder capital and costs Y years of recovery at 6.5% real." Dollar impact + time cost.
4. **Optionality payoff:** "In [crisis], optionality [gained/lost] X%. It [did/did not] perform its crisis insurance function." Evidence-based assessment.
5. **Diversification quality:** "Stabiliser [does/does not] protect against compounder losses in stress. Compounders are [well/poorly] diversified internally."

Then, as supporting detail: rule-level buffers, group tag validation, holding-level drawdowns.

## Notes

- Lead with objectives, not rules. Rules are supporting evidence.
- Dollar amounts > percentages. "AUD 280k of compounding destroyed, 6.8 years to recover" is more useful than "compounder band breaches 50% floor."
- If optionality is too small to matter, say so directly: "At 0.4%, optionality is decorative, not functional."
- Flag the difference between "portfolio survives" and "portfolio thrives." Survival is necessary but not sufficient.
