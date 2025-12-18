import json
from pydantic import ValidationError
from llm_async import LLMTimeoutError
from openai import APIConnectionError,APITimeoutError
from enum import Enum, auto


class FailureType(Enum):
    TIMEOUT = auto()
    SCHEMA_JSON = auto()
    SCHEMA_VALIDATION = auto()
    CONNECTION = auto()
    UNKNOWN = auto()


def classify_failure(exc:Exception)->FailureType:
    if isinstance(exc,LLMTimeoutError):
        return FailureType.TIMEOUT
    if isinstance(exc,json.JSONDecodeError):
        return FailureType.SCHEMA_JSON
    if isinstance(exc,ValidationError):
        return FailureType.SCHEMA_VALIDATION
    if isinstance(exc,(APIConnectionError,APITimeoutError)):
        return FailureType.CONNECTION
    
    return FailureType.UNKNOWN