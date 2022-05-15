class Intervals:
    def __init__(self, start: int, end: int, step: int):
        self.start = start
        self.end = end
        self.step = step
        self.intervals = list(map(lambda i: (i, i + self.step - 1), range(self.start, self.end, self.step)))

    def get_index(self, point: int) -> int:
        for i in range(0, len(self.intervals)):
            if self.intervals[i][0] <= point <= self.intervals[i][1]:
                return i
        raise Exception(f"point {point} not in intervals")

    def get_items(self):
        return self.intervals

    def get_by_index(self, index: int) -> (int, int):
        return self.intervals[index]

    def to_discrete_values(self) -> [float]:
        return map(lambda x: (x[0] + x[1]) / 2, self.intervals)
