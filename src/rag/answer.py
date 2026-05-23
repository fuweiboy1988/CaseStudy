from src.rag.query_engine import QueryEngine
from src.rag.adversarial import AdversarialEngine
from src.rag.economic_risk import compute_economic_risk
from src.rag.materiality import interpret_materiality
from src.rag.bull_bear import BullBearEngine
from src.rag.dossier import ResearchDossierBuilder


class RAGSystem:
    def __init__(self):
        self.engine = QueryEngine()
        self.adversary = AdversarialEngine()
        self.bullbear = BullBearEngine()
        self.dossier_builder = ResearchDossierBuilder()

    def _attach_evidence(self, obj, context):
        if not isinstance(obj, dict):
            return obj

        for key in ["bull_case", "bear_case"]:
            if key in obj and isinstance(obj[key], list):
                enriched = []
                for item in obj[key]:
                    enriched.append({
                        "claim": item,
                        "evidence": context[:2]
                    })
                obj[key] = enriched

        return obj

    def answer(self, query):
        # Step 1: retrieve raw chunks
        results = self.engine.retrieve(query, k=12)

        # Step 2: structured context
        structured_context = self.engine.format_context(results)

        # Step 3: build dossier (NEW)
        dossier = self.dossier_builder.build(structured_context)

        # Step 4: adversarial risk reasoning (now uses dossier themes)
        risk_view = self.adversary.build_risk_view(dossier["evidence"])

        # Step 5: economic + materiality layer
        ranked = risk_view.get("dominant_risks", [])

        # pass FULL signal, not truncated abstraction
        economic = compute_economic_risk(ranked)

        interpretation = interpret_materiality(economic)

        # Step 6: bull/bear reasoning
        bullbear = self.bullbear.build(dossier["evidence"])

        # Step 7: attach evidence
        bullbear = self._attach_evidence(bullbear, dossier["evidence"])

        return {
            "query": query,
            "economic_risk_profile": economic,
            "materiality_interpretation": interpretation,
            "bull_case": bullbear["bull_case"],
            "bear_case": bullbear["bear_case"],
            "investment_thesis": risk_view["investment_thesis"],
            "dossier": dossier
        }
