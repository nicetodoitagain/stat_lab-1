from collections import namedtuple
from math import log
from random import randint


def float_range(start, stop, step=1):
    while start <= stop:
        yield start

        start += step


def average(data_set: list):
    return sum(data_set) / len(data_set)


def moment(data_set: list, power=1):
    mean = average(data_set)
    return sum((i - mean) ** power for i in data_set) / len(data_set)


def mode(data_set: list):
    return max(set(data_set), key=lambda d: data_set.count(d))


def median(data_set: list):
    middle = len(data_set) / 2

    if middle % 1:
        return data_set[int(middle)]
    else:
        return data_set[int(middle):int(middle) + 2]


def group_data(data_set: list):  # TODO діапазон -  півсума максимального і мінімального
    distance = int(log(len(data_set), 2)) + 1
    grouped_data_set = {}

    for i in float_range(min(data_set), max(data_set), distance):
        count = sum(i <= j < i + distance for j in data_set)
        if count:
            grouped_data_set[i + distance / 2] = count

    return grouped_data_set


def dispersion(data_set: list, corrected: bool = False):
    res = moment(data_set, 2)
    data_size = len(data_set)

    return res * data_size / (data_size - 1) if corrected else res


def asymmetry(data_set: list):
    return moment(data_set, 3) / (dispersion(data_set) ** 1.5)


def excess(data_set: list):
    return moment(data_set, 4) / (dispersion(data_set) ** 2) - 3


StatDataSet = namedtuple(
    "StatDataSet",
    ["data", "mean", "mode", "median", "spread", "dispersion",
     "deviation", "corrected_dispersion", "corrected_deviation",
     "asymmetry", "excess"]
)


def str_statdata_set(self):
    res = str()
    for key, value in self._asdict().items():
        res += '{} = {}\n'.format(key, value)
    return res


StatDataSet.__str__ = str_statdata_set


def get_data_set(data):
    return StatDataSet(
        data=data,
        mean=average(data),
        mode=mode(data),
        median=median(data),
        spread=max(data) - min(data),
        dispersion=dispersion(data),
        deviation=dispersion(data) ** 0.5,
        corrected_dispersion=dispersion(data, True),
        corrected_deviation=dispersion(data, True) ** 0.5,
        asymmetry=asymmetry(data),
        excess=excess(data))

