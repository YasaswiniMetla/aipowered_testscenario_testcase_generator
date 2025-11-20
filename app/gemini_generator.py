# gemini_generator.py
import json
from pathlib import Path
import google.generativeai as genai
import sys
from app.config import Config

def load_context():
    path = Path(Config.BASE_DIR) / "samples" / "context.txt"
    if not path.exists():
        raise FileNotFoundError(f"Context not found: {path}")
    return path.read_text().strip()

def save_scenarios(scenarios):
    out = Path(Config.OUTPUT_DIR) / "generated_scenarios.txt"
    out.write_text("\n".join(scenarios), encoding="utf-8")
    print(f"[OK] Scenarios saved → {out}")

def save_raw_testcases(testcases):
    out = Path(Config.OUTPUT_DIR) / "testcases_output.json"
    out.write_text(json.dumps(testcases, indent=4), encoding="utf-8")
    print(f"[OK] Raw testcases saved → {out}")

def generate_scenarios(model, context, num=10):
    prompt = f"""
Generate {num} QA test scenarios.

CONTEXT:
\"\"\"{context}\"\"\"

Rules:
- Only numbered scenarios (1., 2., 3.)
- One scenario per line
"""
    response = model.generate_content(prompt)
    text = getattr(response, "text", "") or ""
    lines = [line.strip() for line in text.splitlines() if line.strip() and line.strip()[0].isdigit()]
    if not lines:
        raise RuntimeError("No scenarios returned from Gemini.")
    return lines

def generate_testcase(model, scenario, context):
    prompt = f"""
Create a QA test case in JSON format.

CONTEXT:
\"\"\"{context}\"\"\"

SCENARIO:
\"\"\"{scenario}\"\"\"

Rules:
- Only JSON output
- Must include title, custom_preconds, priority_id, custom_steps_separated[]
"""
    response = model.generate_content(prompt, generation_config={"response_mime_type":"application/json"})
    text = getattr(response, "text", "") or ""
    try:
        return json.loads(text)
    except Exception as e:
        raise RuntimeError("Invalid JSON returned for scenario:\n" + scenario + "\nError: " + str(e))

def main():
    print("=== GEMINI GENERATOR ===")
    Config.ensure_dirs()
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model_name = Config.GEMINI_MODEL
    model = genai.GenerativeModel(model_name)

    context = load_context()

    print("Generating scenarios...")
    scenarios = generate_scenarios(model, context, num=Config.DEFAULT_NUM_SCENARIOS)
    save_scenarios(scenarios)

    print("Generating testcases...")
    testcases = []
    for sc in scenarios:
        try:
            tc = generate_testcase(model, sc, context)
            testcases.append(tc)
        except Exception as e:
            print("❌ Failed:", sc)
            print(e)

    save_raw_testcases(testcases)
    print("=== DONE ===")

if __name__ == "__main__":
    main()
