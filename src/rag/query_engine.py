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
        """
        Normalize ChromaDB output into strict list[dict]
        Ensures consistent theme propagation (single source of truth per chunk)
        """

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        ids = results.get("ids", [[]])[0]

        context = []
        seen = set()

        for i, doc in enumerate(documents):
            if doc in seen:
                continue
            seen.add(doc)

            meta = metadatas[i] if i < len(metadatas) else {}

            # SINGLE SOURCE OF TRUTH: prioritize stored metadata, fallback to tagging
            themes = meta.get("themes")

            if not themes:
                themes = tag_themes(doc)

            if not themes:
                themes = ["unclassified"]

            context.append({
                "text": doc,
                "metadata": meta,
                "chunk_id": ids[i] if i < len(ids) else None,
                "themes": themes
            })

        return context