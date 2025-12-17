import json
import re
from schema import Plan
from pydantic import ValidationError


def _clean_json(text: str) -> str:
    # Remove markdown fences if present
    text = re.sub(r"```(?:json)?", "", text)
    return text.replace("```", "").strip()


def validate_plan(raw_output: str) -> Plan:
    try:
        cleaned = _clean_json(raw_output)
        parsed = json.loads(cleaned)
        return Plan.model_validate(parsed)
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValidationError.from_exception_data(
            title="PlanValidationError",
            line_errors=[],
        )
