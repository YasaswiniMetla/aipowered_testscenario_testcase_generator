# utils/prompts.py

def scenario_prompt(context: str, num: int, temperature: float = 0.3) -> str:
    """
    Build the prompt to generate test scenarios.
    """

    return f"""
Generate {num} high-quality QA test scenarios based on the context below.

CONTEXT:
\"\"\"{context}\"\"\"

Instructions:
- Return ONLY numbered scenarios (1., 2., 3., etc.)
- One scenario per line
- Do NOT include explanations
- Scenarios should be crisp, clear, and testable
- Use professional QA language
Temperature: {temperature}
"""


def improve_scenario_prompt(context: str, scenario: str) -> str:
    """
    Build the prompt to improve one scenario.
    """

    return f"""
Improve the following QA test scenario with more clarity and professional wording,
while keeping the intent the same.

CONTEXT:
\"\"\"{context}\"\"\"

SCENARIO TO IMPROVE:
\"\"\"{scenario}\"\"\"

Rules:
- Keep it a SINGLE scenario sentence
- Make it clear, specific, testable
- No fluff, no extra explanation
- Do NOT output a list, only the improved scenario
"""


def testcase_prompt(context: str, scenario: str) -> str:
    """
    Build the prompt for generating detailed testcases in JSON.
    """

    return f"""
Generate a detailed software QA testcase in pure JSON format.

CONTEXT:
\"\"\"{context}\"\"\"

SCENARIO:
\"\"\"{scenario}\"\"\"

Rules:
- Return ONLY valid JSON (no markdown)
- JSON must contain:
  - title
  - priority_id
  - custom_preconds
  - custom_steps_separated[]:
      - content (step description)
      - expected (expected result)
- All steps must include expected results
- Use professional QA formatting
- Do not generate additional comments
"""
