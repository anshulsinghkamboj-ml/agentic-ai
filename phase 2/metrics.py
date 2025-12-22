from collections import defaultdict


class Metrics:
    def __init__(self):
        self.data = defaultdict(int)

    def record(self, key):
        self.data[key] += 1

    def snapshot(self):
        return dict(self.data)
