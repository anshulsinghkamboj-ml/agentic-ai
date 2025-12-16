import json
from model import call_model
from parser import parse_validate_or_die
from repair_prompt import repair_prompt
from logger import log_event

MAX_RETRIES = 2

def run_agent():
    last_error = None
    output = None

    for attempt in range(MAX_RETRIES + 1):
        if attempt == 0:
            output = call_model()
        else:
            output = call_model(
                repair_prompt(output, str(last_error))
            )

        log_event("model_output", output)

        try:
            data = parse_validate_or_die(output)
            log_event("accepted_output", json.dumps(data, indent=2))
            return data

        except Exception as e:
            log_event("rejected_output", str(e))
            last_error = e

    raise RuntimeError("🛑 Agent failed after maximum retries")
