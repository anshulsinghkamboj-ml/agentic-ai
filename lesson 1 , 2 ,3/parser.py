import json
from schema import AGENT_SCHEMA
from validate_schema import validate_schema

def parse_validate_or_die(text: str) -> dict:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            "Invalid JSON syntax\n"
            f"{text}\n\n{e}"
        )

    validate_schema(data, AGENT_SCHEMA)
    return data
