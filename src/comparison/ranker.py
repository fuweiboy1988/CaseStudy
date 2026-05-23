def rank_companies(company_outputs):
    scores = {}

    for company, data in company_outputs.items():
        total = sum(r["economic_score"] for r in data["economic_risk_profile"])
        scores[company] = total

    ranked = sorted(scores.items(), key=lambda x: x[1])

    return {
        "ranking": ranked,
        "best_risk_profile": ranked[0][0],
        "worst_risk_profile": ranked[-1][0]
    }
