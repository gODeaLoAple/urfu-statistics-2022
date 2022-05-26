class Interval:
    def __init__(self, left, right, values):
        self.left = left
        self.right = right
        self.middle = (right + left) / 2
        self.values = values
        self.count = len(values)

    def __contains__(self, item):
        return self.left <= item <= self.right
