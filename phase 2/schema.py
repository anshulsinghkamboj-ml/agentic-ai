from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class Step(BaseModel):
    id: int
    action: str
    input: str
    expected_output: str


class Plan(BaseModel):
    objective: str
    steps: List[Step]
    confidence: float = Field(..., ge=0.0, le=1.0)


class CriticDecision(str, Enum):
    ACCEPT = "ACCEPT"
    REPLAN = "REPLAN"
    FAIL = "FAIL"


class CriticReport(BaseModel):
    decision: CriticDecision
    reasoning: str
    confidence: float = Field(..., ge=0.0, le=1.0)
