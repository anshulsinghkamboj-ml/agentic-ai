def repair_prompt(bad_output: str, error: str) -> str:
    return (
        "Your previous output violated the required JSON schema.\n\n"
        f"ERROR:\n{error}\n\n"
        "You MUST return ONLY valid JSON matching:\n"
        "{ goal: string, steps: list of strings, done: boolean }\n\n"
        "Previous output:\n"
        f"{bad_output}"
    )
