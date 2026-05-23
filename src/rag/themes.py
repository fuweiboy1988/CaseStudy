RISK_THEMES = {
    "regulatory": ["sec", "nasdaq", "compliance", "regulation"],
    "financial_reporting": ["internal control", "financial reporting", "audit", "misstatement"],
    "competitive": ["competition", "market share", "competitors"],
    "liquidity": ["liquidity", "cash flow", "debt", "financing"],
    "operational": ["operations", "fleet", "logistics", "execution"],
    "governance": ["management", "control", "board", "oversight"]
}

def tag_themes(text):
    text_lower = text.lower()

    tags = []
    for theme, keywords in RISK_THEMES.items():
        if any(k in text_lower for k in keywords):
            tags.append(theme)

    return tags if tags else ["unclassified"]
