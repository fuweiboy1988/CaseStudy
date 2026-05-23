from src.rag.answer import RAGSystem
import json

def main():
    rag = RAGSystem()

    print("\n=== Investment Research Engine (Structured RAG) ===\n")

    while True:
        q = input("\nQuery: ")

        if q.lower() == "exit":
            break

        result = rag.answer(q)

        print("\n" + "="*80)
        print(json.dumps(result, indent=2))
        print("="*80)

if __name__ == "__main__":
    main()
