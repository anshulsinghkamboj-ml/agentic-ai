from openai import OpenAI

client = OpenAI(
    api_key="lm-studio",
    base_url="http://localhost:1234/v1"
)

SYSTEM_PROMPT = """
You are an AI planning engine.

RULES:
- You MUST output valid JSON
- Output MUST conform EXACTLY to the provided schema
- Do NOT include explanations, markdown, or extra text
- If unsure, make best assumptions but NEVER break schema
"""


def get_plan(task: str) -> str:
    response = client.chat.completions.create(
        model="",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Objective: {task}\nReturn JSON only."}
        ],
        temperature=0,
    )
    return response.choices[0].message.content


def repair_plan(bad_output: str, error: str) -> str:
    response = client.chat.completions.create(
        model="",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""
Your previous output was INVALID.

Validation error:
{error}

Fix the JSON so it EXACTLY matches this schema:

{{
  "objective": "string",
  "steps": [
    {{
      "id": 1,
      "action": "string",
      "input": "string",
      "expected_output": "string"
    }}
  ],
  "confidence": 0.0
}}

Return ONLY valid JSON.
Previous output:
{bad_output}
"""}
        ],
        temperature=0,
    )
    return response.choices[0].message.content
