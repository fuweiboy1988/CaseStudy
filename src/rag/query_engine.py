from src.rag.embeddings import Embedder
from src.rag.vectorstore.chroma_store import VectorStore
from src.rag.themes import tag_themes

class QueryEngine:
    def __init__(self):
        self.embedder = Embedder()
        self.store = VectorStore()

    def retrieve(self, query, k=10):
        q_emb = self.embedder.embed([query])[0]
        results = self.store.query(q_emb, k=k)
        return results

    def format_context(self, results):
        docs = results["documents"][0]
        metas = results.get("metadatas", [[]])[0]

        context = []

        for i in range(len(docs)):
            text = docs[i]
            context.append({
                "text": text,
                "metadata": metas[i] if i < len(metas) else {},
                "themes": tag_themes(text)
            })

        return context
