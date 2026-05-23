RISK_SEVERITY = {
    "regulatory": 3,
    "financial_reporting": 3,
    "governance": 3,
    "liquidity": 3,
    "operational": 2,
    "competitive": 2,
    "unclassified": 1
}

def score_risks(risk_profile):
    scored = []

    for risk, count in risk_profile:
        severity = RISK_SEVERITY.get(risk, 1)
        scored.append({
            "risk": risk,
            "count": count,
            "severity": severity,
            "impact_score": count * severity
        })

    return sorted(scored, key=lambda x: x["impact_score"], reverse=True)
