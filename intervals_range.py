class IntervalsRange:
    def __init__(self, start: int, end: int, step: int):
        self.start = start
        self.end = end
        self.step = step

    def range(self):
        for i in range(self.start, self.end + 1, self.step):
            yield i, i + self.step - 1
