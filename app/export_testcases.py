# export_testcases.py
import json
import csv
from pathlib import Path
from app.config import Config


def export_json(data):
    out = Path(Config.get_exports_dir()) / "testcases.json"
    out.write_text(json.dumps(data, indent=4), encoding="utf-8")
    print("[OK] Exported JSON →", out)

def export_csv(data):
    out = Path(Config.get_exports_dir()) / "testcases.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Title", "Preconditions", "Steps"])
        for tc in data:
            steps = "\n".join(
                f"{i+1}. {step.get('content','')} → {step.get('expected','')}"
                for i, step in enumerate(tc.get("custom_steps_separated", []))
            )
            w.writerow([tc.get("title",""), tc.get("custom_preconds", ""), steps])

    print("[OK] Exported CSV →", out)

def export_md(data):
    out = Path(Config.get_exports_dir()) / "testcases.md"
    md = "# Test Cases\n\n"
    for tc in data:
        md += f"## {tc.get('title','No Title')}\n"
        md += f"**Preconditions:** {tc.get('custom_preconds', '')}\n\n"
        md += "**Steps:**\n"
        for step in tc.get("custom_steps_separated", []):
            md += f"- {step.get('content','')} → *{step.get('expected','')}*\n"
        md += "\n---\n"
    out.write_text(md, encoding="utf-8")
    print("[OK] Exported Markdown →", out)

def main():
    print("=== EXPORT TESTCASES ===")
    Config.ensure_dirs()
    clean_path = Path(Config.OUTPUT_DIR) / "testcases_clean.json"
    if not clean_path.exists():
        print("❌ No cleaned JSON found:", clean_path)
        return

    data = json.loads(clean_path.read_text())
    exports_dir = Path(Config.get_exports_dir())
    exports_dir.mkdir(parents=True, exist_ok=True)

    export_json(data)
    export_csv(data)
    export_md(data)

    print("[OK] Done Exporting")

if __name__ == "__main__":
    main()
