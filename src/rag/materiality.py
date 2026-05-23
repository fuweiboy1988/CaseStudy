def interpret_materiality(scored_risks):
    interpretation = []

    top = scored_risks[:3]

    for r in top:
        if r["risk"] == "liquidity":
            interpretation.append("Short-term solvency / refinancing risk is dominant driver of equity risk.")
        elif r["risk"] == "regulatory":
            interpretation.append("Regulatory regime risk can permanently re-rate valuation.")
        elif r["risk"] == "governance":
            interpretation.append("Control structure introduces asymmetric downside risk.")
        elif r["risk"] == "financial_reporting":
            interpretation.append("Accounting reliability risk can trigger valuation multiple compression.")
        elif r["risk"] == "operational":
            interpretation.append("Execution risk affects cash flow stability.")
        elif r["risk"] == "competitive":
            interpretation.append("Market pressure impacts long-term margin profile.")

    return interpretation
