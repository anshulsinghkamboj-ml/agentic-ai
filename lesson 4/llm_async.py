import asyncio
from openai import AsyncOpenAI
from llm import SYSTEM_PROMPT

client = AsyncOpenAI()  # uses same OPENAI_API_KEY env var

class LLMTimeoutError(RuntimeError):
    pass


async def get_plan_async(task: str, timeout_s: float = 10.0) -> str:
    try:
        return await asyncio.wait_for(
            _call_model(task),
            timeout=timeout_s
        )
    except asyncio.TimeoutError:
        raise LLMTimeoutError(f"LLM call exceeded {timeout_s}s timeout")


async def _call_model(task: str) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
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
            }
        ],
        temperature=0,
    )

    return response.choices[0].message.content
