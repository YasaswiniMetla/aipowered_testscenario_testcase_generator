import json
import sys

from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import Config



def main():
    print("=== CLEAN JSON ===")

    raw_path = Path(Config.OUTPUT_DIR) / "testcases_output.json"
    if not raw_path.exists():
        print("❌ Raw output JSON not found.")
        return

    raw_data = json.loads(raw_path.read_text())

    clean = []
    for tc in raw_data:
        if isinstance(tc, dict) and "title" in tc:
            clean.append(tc)

    out = Path(Config.OUTPUT_DIR) / "testcases_clean.json"
    out.write_text(json.dumps(clean, indent=4), encoding="utf-8")

    print(f"[OK] Clean JSON saved → {out}")


if __name__ == "__main__":
    main()
