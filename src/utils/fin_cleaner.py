import re
from bs4 import BeautifulSoup

def clean_html(text: str) -> str:
    # remove HTML
    text = BeautifulSoup(text, "html.parser").get_text(" ")

    # normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # remove SEC boilerplate noise
    noise_patterns = [
        "table of contents",
        "forward-looking statements",
        "risk factors",
    ]

    for n in noise_patterns:
        text = re.sub(n, "", text, flags=re.IGNORECASE)

    return text.strip()


def extract_sections(text: str) -> dict:
    """
    Try to split SEC filing into meaningful sections.
    Lightweight heuristic version (no dependency).
    """

    sections = {
        "risk_factors": [],
        "md_and_a": [],
        "business": [],
        "financial_notes": []
    }

    # crude section detection
    risk = re.findall(r"(risk factors.*?)(?=item|$)", text, re.IGNORECASE | re.DOTALL)
    mdna = re.findall(r"(management['’]?s discussion.*?)(?=item|$)", text, re.IGNORECASE | re.DOTALL)

    if risk:
        sections["risk_factors"].append(risk[0])

    if mdna:
        sections["md_and_a"].append(mdna[0])

    return sections
