from openai import AsyncOpenAI
import asyncio
from prompt import TASK_EXECUTION_PLAN_TEMPLATE ,SYSTEM_PROMPT,FIX_INVALID_JSON_TEMPLATE

client =AsyncOpenAI(
    api_key="lm-studio",
    base_url="http://localhost:1234/v1"
)

class LLMTimeoutError(RuntimeError):
    pass

async def _call_model(task:str)->str:
    response=await client.chat.completions.create(
        model='chatgpt-4o-latest',
        messages=[
            {'role':'system','content':SYSTEM_PROMPT},
            {'role':'user','content':TASK_EXECUTION_PLAN_TEMPLATE.format(task=task)}
        ],temperature=0,
    )
    return response.choices[0].message.content


async def get_plan_async(task:str,timeout_s:float=200.0)->str:
    try:
        return await asyncio.wait_for(_call_model(task),timeout=timeout_s)
    
    except asyncio.TimeoutError:
        raise LLMTimeoutError(f"LLM call exceeded {timeout_s}s timeout")


def repair_plan(bad_output: str, error: str) -> str:
    response = client.chat.completions.create(
        model="",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": FIX_INVALID_JSON_TEMPLATE.format(error=error, bad_output=bad_output)}
        ],
        temperature=0,
    )
    return response.choices[0].message.content

async def repair_plan(bad_output: str, error: str) -> str:
    response = await client.chat.completions.create(
        model="",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": FIX_INVALID_JSON_TEMPLATE.format(
                error=error,
                bad_output=bad_output
            )}
        ],
        temperature=0,
    )
    return response.choices[0].message.content