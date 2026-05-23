from src.rag.thesis_engine import ThesisEngine


class AdversarialEngine:
    def __init__(self):
        self.thesis = ThesisEngine()

    def build_risk_view(self, context):
        """
        Build a stable risk signal view from retrieved context.
        Output is normalized for downstream economic_risk layer.
        """

        risk_counts = {}

        for c in context:
            if not isinstance(c, dict):
                continue

            themes = c.get("themes", []) or []

            for t in themes:
                if not isinstance(t, str):
                    continue
                risk_counts[t] = risk_counts.get(t, 0) + 1

        # Rank risks by frequency
        ranked = sorted(risk_counts.items(), key=lambda x: x[1], reverse=True)

        # IMPORTANT FIX: flatten into list[str] for downstream compatibility
        dominant_risks = [r[0] for r in ranked]

        investment_thesis = {
            "must_hold_conditions": [
                "Regulatory compliance remains stable without material adverse ruling",
                "Internal controls remain effective with no material weaknesses",
                "Liquidity and financing access remain sufficient under stress conditions"
            ],
            "key_failure_modes": [
                "Loss of regulatory standing or compliance breach",
                "Breakdown in governance or reporting integrity"
            ]
        }

        return {
            "dominant_risks": dominant_risks,
            "risk_counts": dict(risk_counts),
            "investment_thesis": investment_thesis
        }
