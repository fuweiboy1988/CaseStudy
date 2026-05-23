import requests
from bs4 import BeautifulSoup


def fetch_aker_ir_documents():
    """
    Placeholder connector for Aker Solutions investor relations.
    In production, this would pull:
    - Annual reports
    - Quarterly reports
    - Earnings presentations
    - Oslo Stock Exchange disclosures
    """

    return []


def download_ir_doc(url: str) -> str:
    """
    Downloads raw IR document HTML/text from a URL.
    """
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.text
    except Exception as e:
        print(f"Failed to download IR doc: {e}")

    return None
