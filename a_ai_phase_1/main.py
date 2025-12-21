from llm import get_plan, repair_plan
from validator import validate_plan
from logger import log_event
from pydantic import ValidationError

MAX_RETRIES = 3


def main():
    task = "Build a CLI tool that summarizes a text file"

    raw_output = get_plan(task)
    log_event("raw_model_output", raw_output)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            plan = validate_plan(raw_output)
            log_event("validated_plan", plan.model_dump_json(indent=2))
            print("PLAN ACCEPTED\n")
            print(plan.model_dump_json(indent=2))
            break  # ← CRITICAL
        except ValidationError as e:
            log_event("validation_error", f"Attempt {attempt} failed:\n{e}")
            if attempt == MAX_RETRIES:
                raise RuntimeError("Plan failed schema validation after max retries")
            raw_output = repair_plan(raw_output, str(e))
            log_event("repaired_output", raw_output)


if __name__ == "__main__":
    main()
