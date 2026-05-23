from src.rag.query_engine import QueryEngine
from src.rag.adversarial import AdversarialEngine
from src.rag.risk_severity import score_risks
from src.rag.bull_bear import BullBearEngine

class RAGSystem:
    def __init__(self):
        self.engine = QueryEngine()
        self.adversary = AdversarialEngine()
        self.bullbear = BullBearEngine()

    def answer(self, query):
        results = self.engine.retrieve(query, k=12)
        context = self.engine.format_context(results)

        risk_view = self.adversary.build_risk_view(context)
        scored = score_risks(risk_view["dominant_risks"])
        bullbear = self.bullbear.build(context)

        return {
            "query": query,
            "risk_profile_scored": scored,
            "interpretation": risk_view["interpretation"],
            "investment_thesis": risk_view["investment_thesis"],
            "bull_case": bullbear["bull_case"],
            "bear_case": bullbear["bear_case"],
            "evidence_sample": context[:5]
        }
