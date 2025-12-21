from textwrap import dedent

SYSTEM_PROMPT = dedent("""
You are an AI planning engine.

RULES:
- You MUST output valid JSON
- Output MUST conform EXACTLY to the provided schema
- Do NOT include explanations, markdown, or extra text
- If unsure, make best assumptions but NEVER break schema
""")

TASK_EXECUTION_PLAN_TEMPLATE = dedent("""
Create a TASK EXECUTION PLAN.

The JSON MUST follow this EXACT structure:

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
- steps MUST be a list of OBJECTS, not strings
- Do NOT add extra fields
- Do NOT explain anything

Objective:
{task}

Return ONLY valid JSON.
"""
)

FIX_INVALID_JSON_TEMPLATE=dedent(
    """
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
"""
)