import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Create a task execution plan for the following objective.

Objective:
{task}

Output JSON ONLY.
"""
            }
        ],
        temperature=0,
    )

    return response.choices[0].message.content


def repair_plan(bad_output: str, error: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Your previous output was INVALID.

Validation error:
{error}

You MUST fix the JSON so that it EXACTLY matches this schema:

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

Rules:
- Return ONLY valid JSON
- Do NOT add or remove fields
- Do NOT explain anything

Previous invalid JSON:
{bad_output}
"""
            }
        ],
        temperature=0,
    )

    return response.choices[0].message.content