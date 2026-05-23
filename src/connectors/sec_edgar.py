import requests
import time

SEC_HEADERS = {
    "User-Agent": "AI-Investment-Research weifu@example.com"
}

SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"


def fetch_company_filings(cik: str, count: int = 10):
    url = SUBMISSIONS_URL.format(cik=cik.zfill(10))

    r = requests.get(url, headers=SEC_HEADERS)
    if r.status_code != 200:
        raise Exception(f"SEC fetch failed: {r.status_code}")

    data = r.json()
    recent = data["filings"]["recent"]

    filings = []

    for i in range(min(count, len(recent["accessionNumber"]))):
        filings.append({
            "accession": recent["accessionNumber"][i],
            "form": recent["form"][i],
            "date": recent["filingDate"][i],
            "primary_doc": recent["primaryDocument"][i]
        })

    return filings


def download_filing(cik: str, accession: str, primary_doc: str):
    acc_no_dash = accession.replace("-", "")
    cik_int = str(int(cik))

    url = f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{acc_no_dash}/{primary_doc}"

    r = requests.get(url, headers=SEC_HEADERS)
    time.sleep(0.2)

    if r.status_code != 200:
        return None

    return r.text
