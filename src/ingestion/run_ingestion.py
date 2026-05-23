import uuid
from src.utils.fin_cleaner import clean_html
from src.configs.company_registry import COMPANIES
from src.connectors.sec_edgar import fetch_company_filings, download_filing
from src.utils.chunking import chunk_text
from src.reports.ingestion_report import generate_report
from src.rag.embeddings import Embedder
from src.rag.vectorstore.chroma_store import VectorStore
import os

os.makedirs("outputs", exist_ok=True)

def preprocess_filings(text: str) -> str:
    cleaned = clean_html(text)

    # filter extreme noise
    if len(cleaned) < 200:
        return None

    return cleaned

def run(company_key="SABLE_OFFSHORE"):
    company = COMPANIES[company_key]
    if "sec_cik" not in company:
        print(f"[SKIP] {company['name']} - no SEC ingestion source")
        return {
            "context": [],
            "report": f"No SEC data available for {company['name']}",
            "filings": []
        }

    cik = company["sec_cik"]

    print(f"Fetching filings for {company['name']}...")

    filings = fetch_company_filings(cik, count=5)

    embedder = Embedder()
    store = VectorStore()

    ids, docs, metas = [], [], []
    all_chunks = []

    for f in filings:
        text = download_filing(cik, f["accession"], f["primary_doc"])
        if not text:
            continue

        text = preprocess_filings(text)
        if not text:
            continue

        chunks = chunk_text(text)

        for chunk in chunks:
            ids.append(str(uuid.uuid4()))
            docs.append(chunk)
            metas.append({
                "form": f["form"],
                "date": f["date"],
                "accession": f["accession"]
            })

        all_chunks.extend(chunks)

    print(f"Embedding {len(docs)} chunks...")

    embeddings = []
    batch_size = 64

    for i in range(0, len(docs), batch_size):
        batch = docs[i:i+batch_size]
        embeddings.extend(embedder.embed(batch))

    store.add(ids=ids, embeddings=embeddings, documents=docs, metadata=metas)

    report = generate_report(filings, company["name"])

    with open("outputs_ingestion_report.md", "w") as f:
        f.write(report)

    # IMPORTANT: guaranteed return
    return {
        "context": all_chunks,
        "report": report,
        "filings": filings
    }


def run_ingestion(company: str):
    return run(company)

if __name__ == "__main__":
    run()
