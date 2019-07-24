import random
from enum import Enum


class Distribution(object):

    class Method(Enum):
        NONE = 0
        UNIFORM = 1
        EXPONENTIAL = 2
        NORMAL = 3

    def __init__(self, distribution_method):
        if not isinstance(distribution_method, Distribution.Method):
            raise Exception("Method of distribution must be of type '" + str(Distribution.Method) + "'!")
        self.distribution_method = distribution_method
        self.state = random.getstate()

    def next(self):
        r = None
        func = self.get_distribution_func()
        if func is not None:
            saved_state = random.getstate()
            random.setstate(self.state)
            r = func()
            self.state = random.getstate()
            random.setstate(saved_state)
        return r

    def next_batch(self, batch_sizes):
        r = None
        func = self.get_distribution_func()
        if func is not None:
            saved_state = random.getstate()
            random.setstate(self.state)
            r = Distribution.generate_batch(batch_sizes, func)
            self.state = random.getstate()
            random.setstate(saved_state)
        return r

    def get_distribution_func(self):
        if self.distribution_method == Distribution.Method.NONE:
            return None
        if self.distribution_method == Distribution.Method.UNIFORM:
            return Distribution.next_uniform
        if self.distribution_method == Distribution.Method.NORMAL:
            return Distribution.next_normal
        if self.distribution_method == Distribution.Method.EXPONENTIAL:
            return Distribution.next_exp

    @classmethod
    def next_uniform(cls, _min=0.0, _max=1.0, calc_distance=False):
        if calc_distance:
            return abs(random.uniform(_min, _max) - ((_min+_max)/2.0))
        return random.uniform(_min, _max)

    @classmethod
    def next_exp(cls, _mean=0.5, calc_distance=False):
        lambd = 1.0 / _mean
        if calc_distance:
            return abs(random.expovariate(lambd) - _mean)
        return random.expovariate(lambd)

    @classmethod
    def next_normal(cls, _mu=0.5, _n_sigma=0.2, calc_distance=False):
        if calc_distance:
            return abs(random.normalvariate(_mu, _n_sigma) - _mu)
        return random.normalvariate(_mu, _n_sigma)

    @classmethod
    def generate_batch(cls, batch_sizes, distribution_func, calc_distance=False):
        if not isinstance(batch_sizes, list):
            raise Exception("Batch description must be in the form of '[<num_1>,<num_2>,...,<num_n>]'!")
        if not callable(distribution_func):
            raise Exception("Method of distribution must be callable!")
        random_batch = [[] for _ in range(len(batch_sizes))]
        for i in range(len(batch_sizes)):
            for j in range(batch_sizes[i]):
                random_batch[i].append(distribution_func(calc_distance=calc_distance))
        return random_batch

    @classmethod
    def sort_batch_by_distance(cls, batch, distance_metric=None):
        sorted_entries = []
        if distance_metric == Distribution.DISTANCE_METRIC_MAX or distance_metric == Distribution.DISTANCE_METRIC_MIN:
            entries = []
            # roll up batch...
            for i in range(len(batch)):
                for j in range(len(batch[i])):
                    entries.append((i, batch[i][j]))
            sorted_entries = sorted(entries, reverse=(distance_metric == Distribution.DISTANCE_METRIC_MAX), key=lambda entry: entry[1])
        return sorted_entries
    DISTANCE_METRIC_MAX = max
    DISTANCE_METRIC_MIN = min
