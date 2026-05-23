from typing import Dict, Any, List


class AnalystBriefBuilder:
    """
    Phase 4: Converts Phase 1 + Phase 2 outputs into a single analyst brief.
    Pure synthesis layer (no retrieval, no embedding, no new inference).
    """

    def build(self, phase1: Dict[str, Any], phase2: Dict[str, Any]) -> Dict[str, Any]:
        merged = self._merge(phase1, phase2)

        verdict = self._verdict(merged)
        confidence = self._confidence(merged)
        key_risks = self._key_risks(merged)
        key_supports = self._key_supports(merged)
        must_hold = self._must_hold(merged)
        watch_items = self._watch_items(merged)
        missing_info = self._missing_info(merged)
        evidence = self._map_evidence(merged)

        report = self._render_report(
            verdict,
            confidence,
            key_risks,
            key_supports,
            must_hold,
            watch_items,
            missing_info
        )

        return {
            "verdict": verdict,
            "confidence": confidence,
            "key_risks": key_risks,
            "key_supports": key_supports,
            "what_must_be_true": must_hold,
            "top_watch_items": watch_items,
            "missing_information": missing_info,
            "supporting_evidence": evidence,
            "report": report,
        }

    def _merge(self, phase1, phase2):
        return {
            "context": phase1.get("context", []),
            "themes": phase1.get("themes", {}),
            "bear_case": phase2.get("bear_case", []),
            "bull_case": phase2.get("bull_case", []),
            "thesis": phase2.get("investment_thesis", {}),
            "risk_profile": phase2.get("economic_risk_profile", {}),
        }

    def _verdict(self, m):
        themes = m["themes"].get("theme_summary", [])
        risk = m["risk_profile"].get("total_risk", 0)

        if risk > 0.7 or "governance" in themes:
            return "High risk / structurally fragile thesis"

        if "liquidity" in themes or risk > 0.4:
            return "Moderate risk / execution-dependent"

        return "Low risk / stable fundamentals"

    def _confidence(self, m):
        n_evidence = len(m.get("context", []))
        return min(1.0, n_evidence / 20)

    def _key_risks(self, m) -> List[str]:
        risks = [c["claim"] for c in m.get("bear_case", [])]
        return self._dedupe_top_k(risks, k=5)

    def _key_supports(self, m) -> List[str]:
        bull = [c["claim"] for c in m.get("bull_case", [])]

        if not bull:
            bull = m["thesis"].get("must_hold_conditions", [])

        return self._dedupe_top_k(bull, k=3)

    def _must_hold(self, m):
        return m["thesis"].get("must_hold_conditions", [])

    def _watch_items(self, m):
        watch = []
        themes = m["themes"].get("theme_summary", [])

        if "liquidity" in themes:
            watch.append(
                "Monitor refinancing and liquidity runway under stress"
            )

        if "governance" in themes:
            watch.append(
                "Watch internal controls and reporting integrity disclosures"
            )

        if "regulatory" in themes:
            watch.append(
                "Track regulatory updates and compliance risk signals"
            )

        if "financial_reporting" in themes:
            watch.append(
                "Monitor audit opinion changes or restatement risk"
            )

        return watch

    def _missing_info(self, m):
        missing = []

        if not m.get("context"):
            missing.append(
                "Insufficient primary disclosure context"
            )

        if "liquidity" not in m["themes"].get("theme_summary", []):
            missing.append(
                "Debt maturity / liquidity structure unclear"
            )

        if "governance" not in m["themes"].get("theme_summary", []):
            missing.append(
                "Limited governance/control structure detail"
            )

        return missing

    def _map_evidence(self, m):
        mapped = []

        for risk in m.get("bear_case", []):
            mapped.append({
                "claim": risk["claim"],
                "evidence_ids": [
                    e.get("metadata", {}).get("accession")
                    for e in risk.get("evidence", [])[:3]
                ]
            })

        return mapped

    def _render_report(
        self,
        verdict,
        confidence,
        key_risks,
        key_supports,
        must_hold,
        watch_items,
        missing_info
    ):
        report = f"""# Analyst Brief

## Verdict
{verdict}

Confidence: {confidence:.2f}

## Key Risks
"""

        if key_risks:
            for r in key_risks[:5]:
                report += f"- {r}\n"
        else:
            report += "- No major risks identified\n"

        report += "\n## Key Supports\n"

        if key_supports:
            for s in key_supports[:3]:
                report += f"- {s}\n"
        else:
            report += "- No strong support factors identified\n"

        report += "\n## What Must Be True\n"

        if must_hold:
            for m in must_hold[:3]:
                report += f"- {m}\n"
        else:
            report += "- No must-hold assumptions defined\n"

        report += "\n## Top Watch Items\n"

        if watch_items:
            for w in watch_items[:3]:
                report += f"- {w}\n"
        else:
            report += "- No active watch items\n"

        report += "\n## Missing Information\n"

        if missing_info:
            for g in missing_info[:3]:
                report += f"- {g}\n"
        else:
            report += "- No major information gaps detected\n"

        return report

    def _dedupe_top_k(self, items, k=3):
        seen = set()
        out = []

        for x in items:
            if x not in seen:
                seen.add(x)
                out.append(x)

            if len(out) == k:
                break

        return out