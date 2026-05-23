from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self):
        # lightweight but strong general-purpose embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, texts):
        """
        Returns list of embeddings (no API calls, fully local)
        """
        return self.model.encode(texts, show_progress_bar=False).tolist()
