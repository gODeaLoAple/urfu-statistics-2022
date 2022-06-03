from typing import List


class BaseInterval:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __contains__(self, item):
        return self.left <= item < self.right


class Interval(BaseInterval):
    def __init__(self, left, right, values: List[float]):
        super().__init__(left, right)
        self.middle = (right + left) / 2
        self.values = values
        self.count = len(values)
