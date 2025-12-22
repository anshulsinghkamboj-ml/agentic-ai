from textwrap import dedent

SYSTEM_PROMPT = dedent("""
You are an AI planning engine.
You MUST output valid JSON.
No markdown. No explanations.
""")

PLAN_PROMPT = dedent("""
Create a TASK EXECUTION PLAN.

You MUST follow these rules EXACTLY:

1. The "action" field MUST be one of the following exact strings:
   - read_file
   - write_file

2. Do NOT invent new actions.
3. Do NOT describe actions in English.
4. If the task is to read a file, use ONLY one step with action "read_file".
5. The "input" field MUST be exactly the file path string.

Schema:
{{
  "objective": "string",
  "steps": [
    {{
      "id": 1,
      "action": "read_file | write_file",
      "input": "string",
      "expected_output": "string"
    }}
  ],
  "confidence": 0.0
}}

Task:
{task}

Return ONLY valid JSON.
""")

CRITIC_PROMPT = dedent("""
OBJECTIVE:
{objective}

PLAN:
{plan}

EXECUTION RESULTS:
{results}

Decide:
- ACCEPT
- REPLAN
- FAIL

Return JSON:
{{
  "decision": "ACCEPT | REPLAN | FAIL",
  "reasoning": "string",
  "confidence": 0.0
}}
""")
