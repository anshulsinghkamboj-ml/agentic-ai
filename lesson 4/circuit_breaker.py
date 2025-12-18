import time
from failures import FailureType

class CircuitBreaker:
    def __init__(
        self,
        failure_type: FailureType,
        threshold: int,
        cooldown_s: int,
    ):
        self.failure_type = failure_type
        self.threshold = threshold
        self.cooldown_s = cooldown_s

        self.failure_count = 0
        self.last_failure_ts = None

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_ts = time.time()

    def allow(self) -> bool:
        if self.failure_count < self.threshold:
            return True

        elapsed = time.time() - self.last_failure_ts
        return elapsed > self.cooldown_s