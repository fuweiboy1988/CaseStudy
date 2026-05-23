class ThesisEngine:
    def build_thesis(self, context, risk_profile):
        must_hold = []
        failure_modes = []

        for item in context:
            text = item["text"].lower()
            themes = item.get("themes", [])

            # --- Must-hold conditions (positive constraints) ---
            if "regulatory" in themes:
                must_hold.append("Regulatory compliance remains stable without material adverse ruling")

            if "financial_reporting" in themes:
                must_hold.append("Internal controls remain effective with no material weaknesses")

            if "liquidity" in themes:
                must_hold.append("Liquidity and financing access remain sufficient under stress conditions")

            if "governance" in themes:
                must_hold.append("Voting/control structure does not create misalignment or regulatory reclassification risk")

            # --- Failure mode extraction (adversarial) ---
            if "control" in text:
                failure_modes.append("Loss of control effectiveness or governance breakdown")

            if "misstatement" in text:
                failure_modes.append("Financial misstatement or audit failure event")

            if "competition" in text:
                failure_modes.append("Competitive pressure leading to margin or market share erosion")

        return {
            "must_hold_conditions": list(set(must_hold)),
            "key_failure_modes": list(set(failure_modes))
        }
