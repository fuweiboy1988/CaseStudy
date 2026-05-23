from src.rag.answer import RAGSystem
from src.reports.analyst_brief import AnalystBrief

def run():
    system = RAGSystem()
    brief = AnalystBrief()

    query = input("\nQuery: ")

    result = system.answer(query)
    report = brief.generate(result)

    print("\n" + "="*80)
    print(report)
    print("="*80)

if __name__ == "__main__":
    run()
