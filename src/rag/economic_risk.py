from collections import defaultdict


RISK_WEIGHTS = {
    "regulatory": 3.0,
    "governance": 2.5,
    "liquidity": 2.5,
    "operational": 2.0,
    "financial_reporting": 2.5,
    "unclassified": 0.5
}


def compute_economic_risk(dominant_risks):
    """
    Convert thematic risk signals into structured economic risk profile.
    Guaranteed to return stable, non-empty structure when signal exists.
    """

    # HARD SAFETY: normalize input
    if not dominant_risks:
        return {
            "scored_risks": [],
            "dominant_risks": [],
            "total_risk": 0.0
        }

    risk_scores = defaultdict(float)

    for r in dominant_risks:
        if isinstance(r, (tuple, list)):
            risk = r[0] if len(r) > 0 else "unclassified"
            weight = float(r[1]) / 10.0 if len(r) > 1 and isinstance(r[1], (int, float)) else 1.0
        else:
            risk = str(r)
            weight = 1.0

        risk_scores[risk] += RISK_WEIGHTS.get(risk, 1.0) * weight

    # If everything collapses, force fallback instead of empty output
    if not risk_scores:
        risk_scores = {"unclassified": 0.1}

    sorted_risks = sorted(risk_scores.items(), key=lambda x: x[1], reverse=True)

    total = sum(v for _, v in sorted_risks)

    return {
        "scored_risks": sorted_risks,
        "dominant_risks": [r[0] for r in sorted_risks[:5]],
        "total_risk": total
    }