from schema import Plan
from pydantic import ValidationError


def validate_plan(raw_json: str) -> Plan:
    return Plan.model_validate_json(raw_json)


# def validate_plan(raw_json: str) -> Plan:
#     try:
#         plan = Plan.model_validate_json(raw_json)
#         return plan
#     except ValidationError as e:
#         raise RuntimeError(
#             f"SCHEMA VALIDATION FAILED:\n{e}\n\nRAW OUTPUT:\n{raw_json}"
#         )

# import json
# import re
# from schema import Plan
# from pydantic import ValidationError


# def extract_json(text: str) -> str:
#     """
#     Removes markdown fences if present and returns raw JSON string.
#     """
#     # Remove ```json or ``` fences
#     cleaned = re.sub(r"```(?:json)?", "", text)
#     cleaned = cleaned.replace("```", "").strip()
#     return cleaned


# def validate_plan(raw_output: str) -> Plan:
#     try:
#         json_str = extract_json(raw_output)

#         # This forces a real JSON parse BEFORE Pydantic
#         parsed = json.loads(json_str)

#         return Plan.model_validate(parsed)

#     except (json.JSONDecodeError, ValidationError) as e:
#         raise RuntimeError(
#             f"SCHEMA VALIDATION FAILED\n\nERROR:\n{e}\n\nRAW OUTPUT:\n{raw_output}"
#         )