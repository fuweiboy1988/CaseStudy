from src.pipeline.phase4_analyst_brief import AnalystBriefBuilder


def run_pipeline(phase1_output, phase2_output):
    if not phase1_output or not phase2_output:
        raise ValueError("Phase 1 or Phase 2 missing")

    builder = AnalystBriefBuilder()
    return builder.build(phase1_output, phase2_output)


if __name__ == "__main__":
    # Placeholder for testing
    print("Pipeline ready. Plug in Phase 1 and Phase 2 outputs.")
