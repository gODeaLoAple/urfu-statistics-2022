class StatisticsData:
    def __init__(self,
                 sample_mean: float,
                 sample_variance: float,
                 sigma: float,
                 s_2: float,
                 mode: float,
                 median: float,
                 sigma_2: float):
        self.sigma_2 = sigma_2
        self.mode = mode
        self.s_2 = s_2
        self.sigma = sigma
        self.sample_variance = sample_variance
        self.sample_mean = sample_mean
        self.median = median
