def build_citations(context):
    citations = []

    for i, c in enumerate(context):
        citations.append({
            "chunk_id": i,
            "source": c["metadata"],
            "text": c["text"][:300]
        })

    return citations
