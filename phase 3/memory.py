import json
from datetime import datetime
from pathlib import Path


MEMORY_PATH = Path("agent_memory.jsonl")


def write_run_memory(state, decision: str):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "task": state.task,
        "decision": decision,
        "metrics": state.metrics.snapshot(),
        "failure_type": (
            state.failure_type.name if state.failure_type else None
        ),
    }

    with MEMORY_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
