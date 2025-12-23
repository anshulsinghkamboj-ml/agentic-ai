import json
from openai import AsyncOpenAI
from prompts import SYSTEM_PROMPT, PLAN_PROMPT, CRITIC_PROMPT
from schema import Plan, CriticReport
from validator import parse_json

client = AsyncOpenAI(
    api_key="lm-studio",
    base_url="http://localhost:1234/v1"
)


async def get_plan(task: str) -> Plan:
    response = await client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": PLAN_PROMPT.format(task=task)},
        ],
        temperature=0,
    )
    parsed = parse_json(response.choices[0].message.content)
    return Plan.model_validate(parsed)


async def critique(objective: str, plan: str, results: str) -> CriticReport:
    response = await client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": CRITIC_PROMPT.format(
                objective=objective,
                plan=plan,
                results=results,
            )},
        ],
        temperature=0,
    )
    return CriticReport.model_validate(
        json.loads(response.choices[0].message.content)
    )
