from collections import defaultdict

def generate_report(documents, company_name: str):
    stats = defaultdict(int)

    for d in documents:
        stats[d.get("form", "UNKNOWN")] += 1

    report = []
    report.append(f"# Ingestion Report: {company_name}\n")
    report.append("## Document Summary\n")

    total = sum(stats.values())

    for k, v in stats.items():
        report.append(f"- {k}: {v} documents")

    report.append(f"\nTotal documents: {total}\n")

    # Missing data heuristic
    expected = ["10-K", "10-Q", "8-K"]
    missing = [x for x in expected if x not in stats]

    report.append("## Missing Critical Documents\n")
    if missing:
        for m in missing:
            report.append(f"- {m} (IMPORTANT GAP)")
    else:
        report.append("- None detected")

    report.append("\n## Risk Notes\n")
    if missing:
        report.append("- Incomplete regulatory coverage may bias analysis")

    return "\n".join(report)
