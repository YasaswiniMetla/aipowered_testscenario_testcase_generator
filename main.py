# main.py
import subprocess
from pathlib import Path
import sys

# Absolute folder where main.py exists
BASE_DIR = Path(__file__).resolve().parent
print(">>> MAIN running from:", BASE_DIR)

def run(script_name, desc):
    print("\n" + "=" * 60)
    print(desc)
    print("=" * 60)

    script_path = BASE_DIR / script_name

    if not script_path.exists():
        print(f"❌ Script NOT found: {script_path}")
        return False

    # Build command using LIST form (Windows-safe)
    cmd = [sys.executable, str(script_path)]
    print("👉 Running:", cmd)

    try:
        result = subprocess.run(cmd, shell=False)
    except Exception as e:
        print("❌ Subprocess error:", e)
        return False

    if result.returncode != 0:
        print(f"❌ FAILED: {desc} (exit {result.returncode})")
        return False

    print(f"✔ SUCCESS: {desc}")
    return True


def main():
    steps = [
        ("gemini_generator.py", "Step 1: Generate Test Cases"),
        ("json_cleanup.py", "Step 2: Clean JSON"),
        ("export_testcases.py", "Step 3: Export Testcases")
    ]

    for script, desc in steps:
        if not run(script, desc):
            print("\n❌ Pipeline stopped.")
            return

    print("\n🎉 Pipeline completed successfully!")
    print("📁 Outputs saved in outputs/ folder.")


if __name__ == "__main__":
    main()
