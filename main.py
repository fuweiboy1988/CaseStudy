import os
from src.pipeline.phase4_analyst_brief import AnalystBriefBuilder

# You likely already have these modules (adjust imports if needed)
from src.ingestion.run_ingestion import run_ingestion
from src.rag.dossier import build_dossier


OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def run_pipeline(company="SABLE_OFFSHORE"):
    print("\n🚀 Starting full investment research pipeline...\n")

    # =========================
    # Phase 1: Ingestion
    # =========================
    print("📦 Phase 1: Running ingestion...")
    phase1_output = run_ingestion(company)

    ingestion_path = os.path.join(OUTPUT_DIR, "ingestion_report.md")
    save_file(ingestion_path, phase1_output["report"])

    print(f"✅ Phase 1 complete → {ingestion_path}")

    # =========================
    # Phase 2: Dossier
    # =========================
    print("\n🧠 Phase 2: Building deep research dossier...")
    phase2_output = build_dossier(phase1_output)

    dossier_path = os.path.join(OUTPUT_DIR, "dossier.md")
    save_file(dossier_path, phase2_output["report"])

    print(f"✅ Phase 2 complete → {dossier_path}")

    # =========================
    # Phase 3: Analyst Brief
    # =========================
    print("\n📊 Phase 3: Generating analyst brief...")
    builder = AnalystBriefBuilder()

    phase3_output = builder.build(
        phase1_output,
        phase2_output
    )

    brief_path = os.path.join(OUTPUT_DIR, "analyst_brief.md")
    save_file(brief_path, phase3_output["report"])

    print(f"✅ Phase 3 complete → {brief_path}")

    print("\n🎯 PIPELINE COMPLETE — All outputs generated.\n")

    return {
        "phase1": phase1_output,
        "phase2": phase2_output,
        "phase3": phase3_output
    }


if __name__ == "__main__":
    run_pipeline()
