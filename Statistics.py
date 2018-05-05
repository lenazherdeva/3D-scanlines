import numpy as np


def normal_likelihood_explicit(value, mean_0, mean_8, std):
    return (value - (mean_0 + mean_8) / 2.) * (mean_0 - mean_8) / std ** 2


class Stat(object):
    def __init__(self, threshold, direction="unknown", init_stat=0.0):
        self._direction = str(direction)
        self._threshold = float(threshold)
        self._stat = float(init_stat)
        self._alarm = self._stat / self._threshold
    
    @property
    def direction(self):
        return self._direction

    @property
    def stat(self):
        return self._stat
        
    @property
    def alarm(self):
        return self._alarm
        
    @property
    def threshold(self):
        return self._threshold
    
    def update(self, **kwargs):
        # Statistics may use any of the following kwargs:
        #   ts - timestamp for the value
        #   value - original value
        #   mean - current estimated mean
        #   std - current estimated std
        #   adjusted_value - usually (value - mean) / std
        # Statistics call this after updating '_stat'
        self._alarm = self._stat / self._threshold
        
class Cusum(Stat):
    def __init__(self, mean_0, mean_8, std,
                 threshold, direction="unknown", init_stat=0.0):
        self.mean_0 = mean_0
        self.mean_8 = mean_8
        self.std = std
        super(Cusum, self).__init__(threshold, direction, init_stat)
        
    def update(self, value):
        zeta_k = normal_likelihood_explicit(value, self.mean_0, self.mean_8,
                                  self.std)
        self._stat = max(0, self._stat + zeta_k)
        super(Cusum, self).update()


class ShiryaevRoberts(Stat):
    def __init__(self, mean_0, mean_8, threshold, max_stat=float("+inf"), init_stat=0.0):
        super(ShiryaevRoberts, self).__init__(threshold,
                                                      direction="up",
                                                      init_stat=init_stat)
        self.mean_0 = mean_0
        self.mean_8 = mean_8
        self._max_stat = max_stat

    def update(self, value, **kwargs):
        mean_diff = self.mean_0 - self.mean_8
        likelihood = np.exp(mean_diff * (value - mean_diff / 2.))
        self._stat = min(self._max_stat, (1. + self._stat) * likelihood)
        Stat.update(self)
        
