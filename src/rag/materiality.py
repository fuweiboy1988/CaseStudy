def interpret_materiality(economic_risk):
    """
    Convert economic risk output into top material risks.
    """

    if not isinstance(economic_risk, dict):
        return {"top_risks": []}

    # Primary signal: ranked scores
    scored = economic_risk.get("scores")

    # Fallback: dominant_risks (already top-k list)
    if not scored:
        scored = economic_risk.get("dominant_risks", [])

    # Normalize format:
    # scores = [(risk, score), ...]
    # dominant_risks = [risk, ...]
    normalized = []

    if isinstance(scored, list):
        for item in scored:
            if isinstance(item, tuple) or isinstance(item, list):
                normalized.append(item[0])
            else:
                normalized.append(item)

    # final top 3
    top = normalized[:3]

    return {
        "top_risks": top
    }