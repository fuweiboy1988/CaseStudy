class BullBearEngine:
    def build(self, context):
        bull = []
        bear = []

        for item in context:
            text = item["text"].lower()
            themes = item.get("themes", [])

            # Bull logic (stability assumptions)
            if "regulatory" in themes:
                bull.append("Regulatory framework remains stable and predictable")

            if "liquidity" in themes:
                bull.append("Access to financing remains uninterrupted")

            # Bear logic (failure modes)
            if "control" in text:
                bear.append("Governance/control structure may fail or create misalignment")

            if "misstatement" in text:
                bear.append("Financial reporting risk could lead to restatement or loss of confidence")

            if "debt" in text:
                bear.append("Leverage or refinancing risk could emerge under stress")

        return {
            "bull_case": list(set(bull)),
            "bear_case": list(set(bear))
        }
