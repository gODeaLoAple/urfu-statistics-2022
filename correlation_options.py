class CorrelationOptions:
    def __init__(self, alpha, critical_t: float = None):
        self.alpha = alpha
        self.critical_t = critical_t
