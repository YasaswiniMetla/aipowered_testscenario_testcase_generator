# utils/validations.py

def validate_context(text: str) -> tuple[bool, str]:
    """
    Validate requirement/context input before sending to Gemini.
    Returns (is_valid, message)
    """

    if not text or len(text.strip()) == 0:
        return False, "Context cannot be empty."

    if len(text.strip()) < 10:
        return False, "Context is too short. Add at least one full sentence."

    if len(text) > 8000:
        return False, "Context is too long (limit ~8000 characters)."

    return True, ""


def validate_num_scenarios(num: int) -> tuple[bool, str]:
    """
    Validate number of scenarios to generate.
    """
    if num < 1:
        return False, "Number of scenarios must be at least 1."

    if num > 20:
        return False, "Limit exceeded. Max 20 scenarios allowed."

    return True, ""


def validate_scenario_text(text: str) -> tuple[bool, str]:
    """
    Validate a single edited scenario before generating testcases.
    """

    if not text or len(text.strip()) == 0:
        return False, "Scenario text cannot be empty."

    if len(text.strip()) < 5:
        return False, "Scenario too short. Please add more detail."

    return True, ""
