RISK_BASE = {
    "regulatory": {"impact": 0.9, "probability": 0.3, "horizon": "long"},
    "financial_reporting": {"impact": 0.8, "probability": 0.2, "horizon": "medium"},
    "governance": {"impact": 0.85, "probability": 0.25, "horizon": "long"},
    "liquidity": {"impact": 1.0, "probability": 0.4, "horizon": "short"},
    "operational": {"impact": 0.6, "probability": 0.5, "horizon": "medium"},
    "competitive": {"impact": 0.5, "probability": 0.5, "horizon": "long"},
    "unclassified": {"impact": 0.3, "probability": 0.2, "horizon": "long"}
}

HORIZON_WEIGHT = {
    "short": 1.0,
    "medium": 0.8,
    "long": 0.6
}

def compute_economic_risk(risk_profile):
    scored = []

    for risk, count in risk_profile:
        base = RISK_BASE.get(risk, RISK_BASE["unclassified"])

        score = (
            base["impact"]
            * base["probability"]
            * HORIZON_WEIGHT[base["horizon"]]
            * (1 + count * 0.1)
        )

        scored.append({
            "risk": risk,
            "count": count,
            "impact": base["impact"],
            "probability": base["probability"],
            "horizon": base["horizon"],
            "economic_score": round(score, 4)
        })

    return sorted(scored, key=lambda x: x["economic_score"], reverse=True)
