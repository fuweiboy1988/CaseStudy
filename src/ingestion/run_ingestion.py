from src.connectors.sec_edgar import fetch_company_filings, download_filing
from src.utils.chunking import chunk_text

def run():
    # Example: Sable Offshore placeholder CIK (replace later with correct mapping)
    cik = "0000000000"

    print("Fetching filings...")
    filings = fetch_company_filings(cik, count=5)

    all_chunks = []

    for f in filings:
        print("Downloading:", f["form"], f["accession"])
        text = download_filing(cik, f["accession"], f["primaryDoc"])

        if not text:
            continue

        chunks = chunk_text(text)
        all_chunks.extend(chunks)

    print(f"Total chunks created: {len(all_chunks)}")

    return all_chunks


if __name__ == "__main__":
    run()
