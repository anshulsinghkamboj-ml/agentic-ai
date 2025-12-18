import asyncio

from llm_async import get_plan_async
from llm import repair_plan
from backoff_async import retry_with_backoff_async
from validator import validate_plan
from logger import log_event

from failures import classify_failure, FailureType
from metrics import FailureMetrics
from retry_policy import RETRY_POLICY
from circuit_breaker import CircuitBreaker


MAX_SCHEMA_REPAIRS = 2


async def main():
    task = "Build a CLI tool that summarizes a text file"

    metrics = FailureMetrics()

    breakers = {
        FailureType.TIMEOUT: CircuitBreaker(
            FailureType.TIMEOUT, threshold=3, cooldown_s=60
        ),
        FailureType.CONNECTION: CircuitBreaker(
            FailureType.CONNECTION, threshold=3, cooldown_s=120
        ),
    }

    raw_output = None

    try:
        # ---------- MODEL CALL (policy-governed) ----------
        raw_output = await retry_with_backoff_async(
            lambda: get_plan_async(task, timeout_s=15),
            max_retries=RETRY_POLICY[FailureType.TIMEOUT]["max_retries"],
        )

        log_event("raw_model_output", raw_output)

        # ---------- SCHEMA / REPAIR LOOP ----------
        for attempt in range(1, MAX_SCHEMA_REPAIRS + 1):
            try:
                plan = validate_plan(raw_output)
                log_event(
                    "validated_plan",
                    plan.model_dump_json(indent=2),
                )
                print("PLAN ACCEPTED")
                print(plan.model_dump_json(indent=2))
                return

            except Exception as e:
                failure_type = classify_failure(e)
                metrics.record(failure_type)

                log_event(
                    "failure",
                    f"TYPE: {failure_type.name}\nATTEMPT: {attempt}\nERROR:\n{e}",
                )

                # ---- CIRCUIT BREAKER CHECK ----
                breaker = breakers.get(failure_type)
                if breaker:
                    breaker.record_failure()
                    if not breaker.allow():
                        raise RuntimeError(
                            f"CIRCUIT OPEN for {failure_type.name}"
                        )

                # ---- SCHEMA FAILURES CAN BE REPAIRED ----
                if failure_type in (
                    FailureType.SCHEMA_JSON,
                    FailureType.SCHEMA_VALIDATION,
                ):
                    if attempt == MAX_SCHEMA_REPAIRS:
                        raise RuntimeError(
                            "Schema repair attempts exhausted"
                        )

                    raw_output = repair_plan(raw_output, str(e))
                    log_event("repaired_output", raw_output)
                    continue

                # ---- EVERYTHING ELSE FAILS FAST ----
                raise

    except Exception as e:
        failure_type = classify_failure(e)
        metrics.record(failure_type)

        log_event(
            "fatal_failure",
            f"TYPE: {failure_type.name}\nERROR:\n{e}",
        )
        raise

    finally:
        print("\nFAILURE METRICS:")
        for k, v in metrics.snapshot().items():
            print(f"{k.name}: {v}")


if __name__ == "__main__":
    asyncio.run(main())
