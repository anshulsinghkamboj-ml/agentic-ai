import json
import asyncio
from llm import get_plan, critique
from executor import execute
from logger import log


async def main():
    task = "read a text file at local address 'quotes.txt' "

    plan = await get_plan(task)
    log("PLAN", plan.model_dump_json(indent=2))

    results = execute(plan)
    log("EXECUTION", json.dumps(results, indent=2))

    report = await critique(
        plan.objective,
        plan.model_dump_json(),
        json.dumps(results),
    )

    log("CRITIC", report.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
