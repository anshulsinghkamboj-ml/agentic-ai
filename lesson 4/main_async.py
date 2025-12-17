import asyncio
from llm_async import get_plan_async
from llm import repair_plan
from backoff_async import retry_with_backoff_async
from validator import validate_plan
from logger import log_event
from llm_async import LLMTimeoutError

MAX_SCHEMA_REPAIRS = 2


async def main():
    task = "Build a CLI tool that summarizes a text file"

    raw_output = await retry_with_backoff_async(
    lambda: get_plan_async(task, timeout_s=15),
    max_retries=2
)

    log_event("raw_model_output", raw_output)

    for attempt in range(1, MAX_SCHEMA_REPAIRS + 1):
        try:
            plan = validate_plan(raw_output)
            log_event("validated_plan", plan.model_dump_json(indent=2))
            print("PLAN ACCEPTED")
            print(plan.model_dump_json(indent=2))
            return

        except RuntimeError as e:
            log_event("validation_error", f"Attempt {attempt}:\n{e}")

            if attempt == MAX_SCHEMA_REPAIRS:
                raise RuntimeError(
                    "Model failed schema compliance repeatedly. Aborting."
                )

            raw_output = repair_plan(raw_output, str(e))
            log_event("repaired_output", raw_output)


if __name__ == "__main__":
    asyncio.run(main())
