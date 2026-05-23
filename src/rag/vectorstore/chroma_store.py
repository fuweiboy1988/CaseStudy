import chromadb

class VectorStore:
    def __init__(self, path="./chroma_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name="investment_docs"
        )

    def add(self, ids, embeddings, documents, metadata=None):
        self.collection.add(
            ids=ids,
            embeddings=[list(map(float, e)) for e in embeddings],
            documents=documents,
            metadatas=metadata or [{} for _ in documents]
        )

    def query(self, query_embedding, k=5):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
