from tools import TOOLS
from schema import Plan


# first iteration

# def execute(plan: Plan) -> list:
#     results = []

#     for step in plan.steps:
#         tool = TOOLS.get(step.action)
#         if not tool:
#             raise RuntimeError(f"Unknown tool: {step.action}")

#         output = tool(step.input)
#         results.append({
#             "step": step.id,
#             "action": step.action,
#             "output": output,
#         })

#     return results

from failures import FailureType
def execute(plan: Plan):
    results = []

    try:
        for step in plan.steps:
            tool = TOOLS.get(step.action)
            if not tool:
                return {
                    "ok": False,
                    "failure_type": FailureType.TOOL,
                    "error": f"Unknown tool: {step.action}",
                }

            output = tool(step.input)
            results.append({
                "step": step.id,
                "action": step.action,
                "output": output,
            })

        return {
            "ok": True,
            "results": results,
        }

    except Exception as e:
        return {
            "ok": False,
            "failure_type": FailureType.TOOL,
            "error": str(e),
        }