from src.rag.query_engine import QueryEngine
from src.rag.adversarial import AdversarialEngine
from src.rag.economic_risk import compute_economic_risk
from src.rag.materiality import interpret_materiality
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

        economic = compute_economic_risk(risk_view["dominant_risks"])
        interpretation = interpret_materiality(economic)

        bullbear = self.bullbear.build(context)

        return {
            "query": query,
            "economic_risk_profile": economic,
            "materiality_interpretation": interpretation,
            "bull_case": bullbear["bull_case"],
            "bear_case": bullbear["bear_case"],
            "investment_thesis": risk_view["investment_thesis"],
            "evidence_sample": context[:4]
        }
