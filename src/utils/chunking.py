def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200):
    chunks = []
    i = 0

    while i < len(text):
        chunks.append(text[i:i+chunk_size])
        i += chunk_size - overlap

    return chunks
