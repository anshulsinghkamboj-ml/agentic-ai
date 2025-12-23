import json
import asyncio
from llm import get_plan, critique
from executor import execute
from logger import log


# async def main():
#     task = "read a text file at local address 'quotes.txt' "

#     plan = await get_plan(task)
#     log("PLAN", plan.model_dump_json(indent=2))

#     results = execute(plan)
#     log("EXECUTION", json.dumps(results, indent=2))

#     report = await critique(
#         plan.objective,
#         plan.model_dump_json(),
#         json.dumps(results),
#     )

#     log("CRITIC", report.model_dump_json(indent=2))


# if __name__ == "__main__":
#     asyncio.run(main())

#---------------------------------------------------------
# from run_state import RunState
# async def main():
#     task = "read a text file at local address 'quotes.txt'"

#     state = RunState(task)

#     # PLAN
#     state.plan = await get_plan(state.task)
#     log("PLAN", state.plan.model_dump_json(indent=2))

#     # EXECUTE
#     state.results = execute(state.plan)
#     log("EXECUTION", json.dumps(state.results, indent=2))

#     # CRITIQUE
#     report = await critique(
#         state.plan.objective,
#         state.plan.model_dump_json(),
#         json.dumps(state.results),
#     )

#     log("CRITIC", report.model_dump_json(indent=2))


# if __name__ == "__main__":
#     asyncio.run(main())

#-------------------------------------------------------------
# from run_state import RunState
# async def main():
#     task = "read a text file at local address 'quotes.txt'"

#     state = RunState(task)

#     # PLAN
#     state.plan = await get_plan(state.task)
#     log("PLAN", state.plan.model_dump_json(indent=2))

#     # EXECUTE
#     execution = execute(state.plan)

#     if not execution["ok"]:
#         state.record_failure(
#             execution["failure_type"],
#             execution["error"]
#         )
#         log("FAILURE", execution["error"])
#         return

#     state.results = execution["results"]
#     log("EXECUTION", json.dumps(state.results, indent=2))

#     # CRITIQUE
#     report = await critique(
#         state.plan.objective,
#         state.plan.model_dump_json(),
#         json.dumps(state.results),
#     )

#     log("CRITIC", report.model_dump_json(indent=2))


# if __name__ == "__main__":
#     asyncio.run(main())

#------------------------------------------
# from run_state import RunState
# from schema import CriticDecision

# MAX_STEPS = 3


# async def main():
#     task = "read a text file at local address 'q2.txt'"
#     state = RunState(task)

#     for step in range(1, MAX_STEPS + 1):
#         log("STEP", f"Attempt {step}")

#         # PLAN
#         state.plan = await get_plan(state.task)
#         log("PLAN", state.plan.model_dump_json(indent=2))

#         # EXECUTE
#         execution = execute(state.plan)

#         if not execution["ok"]:
#             state.record_failure(
#                 execution["failure_type"],
#                 execution["error"]
#             )
#             log("FAILURE", execution["error"])
#             return

#         state.results = execution["results"]
#         log("EXECUTION", json.dumps(state.results, indent=2))

#         # CRITIQUE
#         report = await critique(
#             state.plan.objective,
#             state.plan.model_dump_json(),
#             json.dumps(state.results),
#         )

#         log("CRITIC", report.model_dump_json(indent=2))

#         # DECISION
#         if report.decision == CriticDecision.ACCEPT:
#             log("DONE", "Task accepted")
#             return

#         if report.decision == CriticDecision.FAIL:
#             log("DONE", "Task failed")
#             return

#         if report.decision == CriticDecision.REPLAN:
#             state.metrics.record("replan")
#             continue

#     log("DONE", "Max steps exceeded")

#-----------------------------------------------
# from run_state import RunState
# from schema import CriticDecision
# from memory import write_run_memory

# MAX_STEPS = 3


# async def main():
#     task = "read a text file at local address 'q2.txt'"
#     state = RunState(task)

#     for step in range(1, MAX_STEPS + 1):
#         log("STEP", f"Attempt {step}")

#         # PLAN
#         state.plan = await get_plan(state.task)
#         log("PLAN", state.plan.model_dump_json(indent=2))

#         # EXECUTE
#         execution = execute(state.plan)

#         if not execution["ok"]:
#             state.record_failure(
#                 execution["failure_type"],
#                 execution["error"]
#             )
#             log("FAILURE", execution["error"])
#             return

#         state.results = execution["results"]
#         log("EXECUTION", json.dumps(state.results, indent=2))

#         # CRITIQUE
#         report = await critique(
#             state.plan.objective,
#             state.plan.model_dump_json(),
#             json.dumps(state.results),
#         )

#         log("CRITIC", report.model_dump_json(indent=2))

#         # DECISION
#         if report.decision == CriticDecision.ACCEPT:
#             write_run_memory(state, "ACCEPT")
#             log("DONE", "Task accepted")
#             return

#         if report.decision == CriticDecision.FAIL:
#             write_run_memory(state, "FAIL")
#             log("DONE", "Task failed")
#             return

#         if report.decision == CriticDecision.REPLAN:
#             state.metrics.record("replan")
#             continue

#     log("DONE", "Max steps exceeded")
#     write_run_memory(state, "TIMEOUT")
#-----------------------------------------------------

# from run_state import RunState
# from schema import CriticDecision
# from memory import write_run_memory
# from failures import FailureType

# MAX_STEPS = 3


# async def main():
#     task = "read a text file at local address 'q2.txt'"
#     state = RunState(task)

#     for step in range(1, MAX_STEPS + 1):
#         log("STEP", f"Attempt {step}")

#         # PLAN
#         state.plan = await get_plan(state.task)
#         log("PLAN", state.plan.model_dump_json(indent=2))

#         # EXECUTE
#         execution = execute(state.plan)

#         if not execution.get("ok"):
#             failure_type = execution["failure_type"]
#             error = execution["error"]

#             state.record_failure(failure_type, error)
#             log("FAILURE", f"{failure_type.name}: {error}")

#             # --- RECOVERY POLICY ---
#             if failure_type == FailureType.TOOL:
#                 retries = state.metrics.snapshot().get("tool_retry", 0)
#                 if retries < 1:
#                     state.metrics.record("tool_retry")
#                     log("RECOVERY", "Retrying same plan after tool failure")
#                     continue
#                 else:
#                     log("RECOVERY", "Tool retry limit exceeded")
#                     write_run_memory(state, "FAIL")
#                     return

#             if failure_type in (FailureType.MODEL, FailureType.SCHEMA):
#                 log("RECOVERY", "Regenerating plan after model/schema failure")
#                 state.metrics.record("replan")
#                 continue

#             # UNKNOWN or anything else
#             log("RECOVERY", "Unrecoverable failure")
#             write_run_memory(state, "FAIL")
#             return

#         state.results = execution["results"]
#         log("EXECUTION", json.dumps(state.results, indent=2))

#         # CRITIQUE
#         report = await critique(
#             state.plan.objective,
#             state.plan.model_dump_json(),
#             json.dumps(state.results),
#         )

#         log("CRITIC", report.model_dump_json(indent=2))

#         # DECISION
#         if report.decision == CriticDecision.ACCEPT:
#             write_run_memory(state, "ACCEPT")
#             log("DONE", "Task accepted")
#             return

#         if report.decision == CriticDecision.FAIL:
#             write_run_memory(state, "FAIL")
#             log("DONE", "Task failed")
#             return

#         if report.decision == CriticDecision.REPLAN:
#             state.metrics.record("replan")
#             continue

#     log("DONE", "Max steps exceeded")
#     write_run_memory(state, "TIMEOUT")
#---------------------------------------------

from run_state import RunState
from schema import CriticDecision
from memory import write_run_memory
from failures import FailureType

MAX_STEPS = 3
MAX_REPLANS = 2
MIN_CONFIDENCE = 0.4



async def main():
    task = "read a text file at local address 'q2.txt'"
    state = RunState(task)

    for step in range(1, MAX_STEPS + 1):
        log("STEP", f"Attempt {step}")

        # PLAN
        state.plan = await get_plan(state.task)
        log("PLAN", state.plan.model_dump_json(indent=2))

        # EXECUTE
        execution = execute(state.plan)

        if not execution.get("ok"):
            failure_type = execution["failure_type"]
            error = execution["error"]

            state.record_failure(failure_type, error)
            log("FAILURE", f"{failure_type.name}: {error}")

            # --- RECOVERY POLICY ---
            if failure_type == FailureType.TOOL:
                retries = state.metrics.snapshot().get("tool_retry", 0)
                if retries < 1:
                    state.metrics.record("tool_retry")
                    log("RECOVERY", "Retrying same plan after tool failure")
                    continue
                else:
                    log("RECOVERY", "Tool retry limit exceeded")
                    write_run_memory(state, "FAIL")
                    return

            if failure_type in (FailureType.MODEL, FailureType.SCHEMA):
                log("RECOVERY", "Regenerating plan after model/schema failure")
                state.metrics.record("replan")
                continue

            # UNKNOWN or anything else
            log("RECOVERY", "Unrecoverable failure")
            write_run_memory(state, "FAIL")
            return

        state.results = execution["results"]
        log("EXECUTION", json.dumps(state.results, indent=2))

        # CRITIQUE
        report = await critique(
            state.plan.objective,
            state.plan.model_dump_json(),
            json.dumps(state.results),
        )

        log("CRITIC", report.model_dump_json(indent=2))

        # DECISION
        if report.decision == CriticDecision.ACCEPT:
            write_run_memory(state, "ACCEPT")
            log("DONE", "Task accepted")
            return

        if report.decision == CriticDecision.FAIL:
            write_run_memory(state, "FAIL")
            log("DONE", "Task failed")
            return

        if report.decision == CriticDecision.REPLAN:
            replans = state.metrics.snapshot().get("replan", 0)

            if replans >= MAX_REPLANS:
                log("QUALITY", "Replan budget exhausted")
                write_run_memory(state, "FAIL")
                return

            if report.confidence < MIN_CONFIDENCE:
                log(
                    "QUALITY",
                    f"Confidence too low to continue ({report.confidence})"
                )
                write_run_memory(state, "FAIL")
                return

            state.metrics.record("replan")
            log("QUALITY", "Replanning with constraints")
            continue

    log("DONE", "Max steps exceeded")
    write_run_memory(state, "TIMEOUT")