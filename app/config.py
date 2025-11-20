"""
Configuration for AI Test Case Generator (Gemini-ready)
No side-effects on import. Call Config.ensure_dirs() explicitly when needed.
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env
load_dotenv()

class Config:
    BASE_DIR = Path(__file__).parent.resolve()

    # Gemini / Google GenAI config
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    GEMINI_TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
    GEMINI_MAX_RETRIES = int(os.getenv("GEMINI_MAX_RETRIES", "2"))

    # App settings
    DEFAULT_NUM_SCENARIOS = int(os.getenv("DEFAULT_NUM_SCENARIOS", "10"))
    MIN_SCENARIOS = int(os.getenv("MIN_SCENARIOS", "5"))
    MAX_SCENARIOS = int(os.getenv("MAX_SCENARIOS", "30"))

    # Directories (expect `samples/` at repo root)
    SAMPLES_DIR = BASE_DIR / "samples"
    OUTPUT_DIR = BASE_DIR / "outputs"
    EXPORTS_DIR = OUTPUT_DIR / "exports"

    # Filenames
    TESTCASES_OUTPUT = "testcases_output.json"
    TESTCASES_CLEAN = "testcases_clean.json"
    SCENARIOS_OUTPUT = "generated_scenarios.txt"
    RAW_RESPONSES_LOG = "gpt_raw_responses.txt"  # generic name; still used for responses

    @classmethod
    def ensure_dirs(cls):
        cls.SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_sample_path(cls, filename: str):
        return cls.SAMPLES_DIR / filename

    @classmethod
    def get_output_path(cls, filename: str):
        return cls.OUTPUT_DIR / filename

    @classmethod
    def get_exports_dir(cls):
        return cls.EXPORTS_DIR
