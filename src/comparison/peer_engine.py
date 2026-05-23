class PeerComparisonEngine:
    def compare(self, company_outputs):
        comparison = {}

        all_risks = set()
        for c in company_outputs.values():
            for r in c["economic_risk_profile"]:
                all_risks.add(r["risk"])

        for risk in all_risks:
            comparison[risk] = {}

            for company, data in company_outputs.items():
                match = next(
                    (r for r in data["economic_risk_profile"] if r["risk"] == risk),
                    None
                )

                comparison[risk][company] = match["economic_score"] if match else 0

        return comparison
