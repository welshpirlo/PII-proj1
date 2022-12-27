import numpy as np


def __trapmf(x, a, b, c, d, h):
    if a <= x < b:
        return min((x - a) / (b - a), h)
    elif b <= x <= c:
        return min(1., h)
    elif c < x <= d:
        return min((d - x) / (d - c), h)
    return 0.


def trapmf(x, a: float, b: float, c: float, d: float, h=1):
    iterable = (__trapmf(item, a, b, c, d, h) for item in x)
    mf = np.fromiter(iterable, float)
    return np.nan_to_num(mf)