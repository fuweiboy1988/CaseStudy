from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class EvidenceChunk:
    text: str
    metadata: Dict[str, Any]


class ResearchDossierBuilder:
    """
    Phase 2: Deep Research Dossier

    Converts raw retrieval context into a structured, reusable
    research object for downstream analyst reasoning.
    """

    def __init__(self):
        pass

    def build(self, structured_context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Build a normalized dossier from retrieved chunks.
        """

        themes = {}
        cleaned_evidence = []

        for chunk in structured_context:
            if not isinstance(chunk, dict):
                continue

            text = chunk.get("text", "")
            metadata = chunk.get("metadata", {})
            chunk_themes = chunk.get("themes", []) or []

            cleaned_evidence.append(
                EvidenceChunk(
                    text=text,
                    metadata=metadata
                ).__dict__
            )

            for t in chunk_themes:
                themes[t] = themes.get(t, 0) + 1

        ranked_themes = sorted(
            themes.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {
            "evidence": cleaned_evidence,
            "ranked_themes": ranked_themes,
            "theme_summary": [t[0] for t in ranked_themes]
        }


# ---- compatibility wrapper for main.py ----

def build_dossier(structured_context):
    builder = ResearchDossierBuilder()
    dossier = builder.build(structured_context)

    themes = dossier.get("theme_summary", [])
    evidence_count = len(dossier.get("evidence", []))

    report = f"""# Deep Research Dossier

## Evidence Coverage
- Evidence chunks reviewed: {evidence_count}

## Dominant Themes
"""

    if themes:
        for t in themes[:5]:
            report += f"- {t}\n"
    else:
        report += "- No dominant themes identified\n"

    report += """

## Key Observations
- Research generated from retrieved filing evidence
- Further adversarial reasoning modules can expand this dossier

## Remaining Gaps
- Management tone analysis not yet implemented
- Contradiction detection not yet implemented
- Verdict logic still preliminary
"""

    return {
        **dossier,
        "report": report
    }