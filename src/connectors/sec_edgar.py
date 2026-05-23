import requests
import time

SEC_HEADERS = {
    "User-Agent": "AI-Research-Platform weifu@example.com"
}

SEC_ARCHIVES = "https://data.sec.gov"

def fetch_company_filings(cik: str, count: int = 10):
    """
    Fetch recent SEC filings metadata for a company.
    """
    url = f"{SEC_ARCHIVES}/submissions/CIK{cik.zfill(10)}.json"
    
    resp = requests.get(url, headers=SEC_HEADERS)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch filings: {resp.status_code}")

    data = resp.json()
    filings = data.get("filings", {}).get("recent", {})

    results = []
    for i in range(min(count, len(filings.get("accessionNumber", [])))):
        results.append({
            "accession": filings["accessionNumber"][i],
            "form": filings["form"][i],
            "date": filings["filingDate"][i],
            "reportDate": filings["reportDate"][i],
            "primaryDoc": filings["primaryDocument"][i],
        })

    return results


def download_filing(cik: str, accession: str, primary_doc: str):
    """
    Download raw filing text from SEC.
    """
    acc_nodash = accession.replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_nodash}/{primary_doc}"

    resp = requests.get(url, headers=SEC_HEADERS)
    time.sleep(0.2)

    if resp.status_code != 200:
        return None

    return resp.text
