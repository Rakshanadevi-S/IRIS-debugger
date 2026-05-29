def build_prompt(error_text: str) -> str:
    """
    Formats the user's raw Python error into a structured prompt for the LLM.
    """
    return (
        "Analyze this Python error and return a structured JSON response:\n\n"
        f"{error_text}"
    )
