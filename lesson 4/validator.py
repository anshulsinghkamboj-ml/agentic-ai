import json
import re
from schema import Plan
from pydantic import ValidationError


def _clean_json(text: str) -> str:
    text = re.sub(r"```(?:json)?", "", text)
    return text.replace("```", "").strip()


def validate_plan(raw_output: str) -> Plan:
    try:
        cleaned = _clean_json(raw_output)
        parsed = json.loads(cleaned)
        return Plan.model_validate(parsed)

    except (json.JSONDecodeError, ValidationError) as e:
        raise RuntimeError(
            f"SCHEMA VALIDATION FAILED\n\nERROR:\n{e}\n\nRAW OUTPUT:\n{raw_output}"
        )
