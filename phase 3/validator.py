import json
import re


def parse_json(raw: str) -> dict:
    """
    Extract and parse JSON from model output.
    """
    cleaned = re.sub(r"```(?:json)?", "", raw)
    cleaned = cleaned.replace("```", "").strip()
    return json.loads(cleaned)
