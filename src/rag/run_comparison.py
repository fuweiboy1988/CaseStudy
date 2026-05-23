from src.rag.answer import RAGSystem
from src.comparison.peer_engine import PeerComparisonEngine
from src.comparison.ranker import rank_companies

def run():
    system = RAGSystem()

    companies = ["SOC", "AKSO"]
    outputs = {}

    for c in companies:
        print(f"\nAnalyzing {c}...")
        outputs[c] = system.answer(f"Key risks and investment thesis for {c}")

    comparator = PeerComparisonEngine()
    comparison_matrix = comparator.compare(outputs)

    ranking = rank_companies(outputs)

    print("\n================ COMPARISON MATRIX ================\n")
    for risk, vals in comparison_matrix.items():
        print(risk, vals)

    print("\n================ RANKING ================\n")
    print(ranking)

if __name__ == "__main__":
    run()
