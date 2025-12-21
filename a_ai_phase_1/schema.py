from pydantic import BaseModel,Field
from typing import List


class Step(BaseModel):
    id: int = Field(..., description="Step number starting from 1")
    action: str = Field(..., description="What the agent should do")
    input: str = Field(..., description="Input required for this step")
    expected_output: str = Field(..., description="What success looks like")


class Plan(BaseModel):
    objective: str = Field(..., description="Overall goal")
    steps: List[Step] = Field(..., min_items=1)
    confidence: float = Field(..., ge=0.0, le=1.0)