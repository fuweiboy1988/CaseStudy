class AnalystBrief:
    def generate(self, result):
        return f"""
════════════════════════════
INVESTMENT ANALYST BRIEF
════════════════════════════

Query:
{result.get("query")}

────────────────────────────
RISK PROFILE (SCORED)
────────────────────────────
{result.get("risk_profile_scored")}

────────────────────────────
INVESTMENT THESIS
────────────────────────────
Must-Hold Conditions:
{result.get("investment_thesis", {}).get("must_hold_conditions")}

Key Failure Modes:
{result.get("investment_thesis", {}).get("key_failure_modes")}

────────────────────────────
BULL CASE
────────────────────────────
{result.get("bull_case")}

────────────────────────────
BEAR CASE
────────────────────────────
{result.get("bear_case")}

────────────────────────────
INTERPRETATION
────────────────────────────
{result.get("interpretation")}

════════════════════════════
END BRIEF
════════════════════════════
"""
