import json
import re
from schema import Plan


def _clean_json(text: str) -> str:
    text = re.sub(r"```(?:json)?", "", text)
    return text.replace("```", "").strip()


def validate_plan(raw_output: str) -> Plan:
    cleaned = _clean_json(raw_output)
    parsed = json.loads(cleaned)          # may raise JSONDecodeError
    return Plan.model_validate(parsed)    # may raise ValidationError
