from src.rag.thesis_engine import ThesisEngine

class AdversarialEngine:
    def __init__(self):
        self.thesis = ThesisEngine()

    def build_risk_view(self, context):
        risk_summary = {}

        for c in context:
            for t in c["themes"]:
                risk_summary[t] = risk_summary.get(t, 0) + 1

        sorted_risks = sorted(risk_summary.items(), key=lambda x: x[1], reverse=True)

        thesis = self.thesis.build_thesis(context, risk_summary)

        return {
            "dominant_risks": sorted_risks,
            "interpretation": self._interpret(sorted_risks),
            "investment_thesis": thesis
        }

    def _interpret(self, risks):
        insights = []

        for r, score in risks:
            if r == "financial_reporting":
                insights.append("Reporting integrity risk present")
            elif r == "liquidity":
                insights.append("Financing stress exposure detected")
            elif r == "competitive":
                insights.append("Competitive pressure likely compressing margins")
            elif r == "regulatory":
                insights.append("Regulatory exposure is structurally material")
            elif r == "governance":
                insights.append("Governance/control structure complexity detected")

        return insights
