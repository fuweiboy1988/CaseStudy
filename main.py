from pathlib import Path

from src.ingestion.run_ingestion import run_ingestion
from src.rag.dossier import build_dossier
from src.pipeline.phase4_analyst_brief import AnalystBriefBuilder


OUTPUT_DIR = Path("outputs")


def save_file(path, content):
    with open(path, "w") as f:
        f.write(content)


def run_pipeline(company_key):

    print(f"\n=== {company_key} ===")

    phase1_output = run_ingestion(company_key)

    phase1_path = (
        OUTPUT_DIR /
        f"{company_key.lower()}_ingestion_report.md"
    )

    save_file(
        phase1_path,
        phase1_output["report"]
    )
    print("DEBUG PHASE1 OUTPUT:", phase1_output)
    print(
        f"Phase 1 complete -> {phase1_path}"
    )

    phase2_output = build_dossier(
        phase1_output.get("context", [])
    )

    dossier_path = (
        OUTPUT_DIR /
        f"{company_key.lower()}_dossier.md"
    )

    save_file(
        dossier_path,
        phase2_output["report"]
    )

    print(
        f"Phase 2 complete -> {dossier_path}"
    )

    brief_builder = AnalystBriefBuilder()

    phase3_output = brief_builder.build(
        phase1_output,
        phase2_output
    )

    brief_path = (
        OUTPUT_DIR /
        f"{company_key.lower()}_analyst_brief.md"
    )

    save_file(
        brief_path,
        phase3_output["report"]
    )

    print(
        f"Phase 3 complete -> {brief_path}"
    )


if __name__ == "__main__":

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    run_pipeline(
        "SABLE_OFFSHORE"
    )

    run_pipeline(
        "AKER_SOLUTIONS"
    )
