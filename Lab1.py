from collections import namedtuple
from numpy import unique


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
    m = max(data_set.count(d) for d in unique(data_set))

    if len([d for d in unique(data_set) if data_set.count(d) == m]) > 1:
        return None
    else:
        return m


def median(data_set: list):
    middle = len(data_set) / 2

    if middle % 1:
        return data_set[int(middle)]
    else:
        return data_set[int(middle):int(middle) + 2]


def dispersion(data_set: list, corrected: bool = False):
    res = moment(data_set, 2)
    data_size = len(data_set)

    return res * data_size / (data_size - 1) if corrected else res


def asymmetry(data_set: list):
    return moment(data_set, 3) / (dispersion(data_set) ** 1.5)


def excess(data_set: list):
    return moment(data_set, 4) / (dispersion(data_set) ** 2) - 3


def cumulate(data_set: list):
    high = 0
    result = []
    for i in unique(data_set):
        result.append(high + data_set.count(i))
        high += data_set.count(i)  # TODO: refactor||delete
    return result


def cumulate_freq(data_set: list):
    high = 0
    result = []
    for i in unique(data_set):
        result.append(high + data_set.count(i)/len(data_set))
        high += data_set.count(i)/len(data_set)  # TODO: refactor||delete
    return result


StatDataSet = namedtuple(
    "StatDataSet",
    ["data", "unique", "count", "freq_count", "cumulate", "freq_cumulate", "mean", "mode", "median", "spread",
     "dispersion", "deviation", "corrected_dispersion", "corrected_deviation", "asymmetry", "excess"]
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
        unique=[list(unique(data))],
        count=[data.count(i) for i in unique(data)],
        freq_count=[data.count(i) / len(data) for i in unique(data)],
        cumulate=cumulate(data),
        freq_cumulate=cumulate_freq(data),
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
