from failures import FailureType
from collections import defaultdict


class FailureMetrics:
    def __init__(self):
        self.counts = defaultdict(int)

    def record(self, failure_type: FailureType):
        self.counts[failure_type] += 1

    def snapshot(self) -> dict:
        return dict(self.counts)