from typing import Optional, Any
from metrics import Metrics
from failures import FailureType


class RunState:
    def __init__(self, task: str):
        self.task = task

        # planning
        self.plan = None

        # execution
        self.results = None

        # failure handling
        self.failure_type: Optional[FailureType] = None
        self.failure_payload: Optional[Any] = None

        # observability
        self.metrics = Metrics()

    def record_failure(self, failure_type: FailureType, payload: Any):
        self.failure_type = failure_type
        self.failure_payload = payload
        self.metrics.record(f"failure_{failure_type.name.lower()}")
