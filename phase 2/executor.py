from tools import TOOLS
from schema import Plan


def execute(plan: Plan) -> list:
    results = []

    for step in plan.steps:
        tool = TOOLS.get(step.action)
        if not tool:
            raise RuntimeError(f"Unknown tool: {step.action}")

        output = tool(step.input)
        results.append({
            "step": step.id,
            "action": step.action,
            "output": output,
        })

    return results
