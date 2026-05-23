import uuid
from src.configs.company_registry import COMPANIES
from src.connectors.sec_edgar import fetch_company_filings, download_filing
from src.utils.chunking import chunk_text
from src.reports.ingestion_report import generate_report
from src.rag.embeddings import Embedder
from src.rag.vectorstore.chroma_store import VectorStore


def run(company_key="SABLE_OFFSHORE"):
    company = COMPANIES[company_key]
    cik = company["sec_cik"]

    print(f"Fetching filings for {company['name']}...")

    filings = fetch_company_filings(cik, count=5)

    embedder = Embedder()
    store = VectorStore()

    all_chunks = []
    ids = []
    docs = []
    metas = []

    for f in filings:
        text = download_filing(cik, f["accession"], f["primary_doc"])

        if not text:
            continue

        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            ids.append(str(uuid.uuid4()))
            docs.append(chunk)
            metas.append({
                "form": f["form"],
                "date": f["date"],
                "accession": f["accession"]
            })

        all_chunks.extend(chunks)

    print(f"Embedding {len(docs)} chunks...")

    batch_size = 64
    embeddings = []

    for i in range(0, len(docs), batch_size):
        batch = docs[i:i+batch_size]
        embeddings.extend(embedder.embed(batch))

    print("Storing in vector DB...")

    store.add(
        ids=ids,
        embeddings=embeddings,
        documents=docs,
        metadata=metas
    )

    report = generate_report(
        filings,
        company["name"]
    )

    with open("outputs_ingestion_report.md", "w") as f:
        f.write(report)

    print(report)
    print(f"\nChunks embedded: {len(docs)}")


if __name__ == "__main__":
    run()
