from typing import Optional


class NormReportOptions:
    def __init__(self, alpha: float, xi_expected: Optional[float] = None, q: Optional[float] = None):
        self.xi_expected = xi_expected
        self.q = q
        self.alpha = alpha
