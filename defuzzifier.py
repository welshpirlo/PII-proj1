import numpy as np
import sys

__all__ = ['defuzzification',]


def defuzzification(x, mf, defuzz_type='cog') -> float:
    """
    Defuzzifying the output fuzzy set.

    :param x: Universe
    :param mf: Membership Function
    :param defuzz_type:
     'cog' - Center of Gravity,
     'fom' - First of Maximum,
     'lom' - Last of Maximum,
     'mom' - Middle of Maximum,
    :return: crisp value
    """

    method = getattr(sys.modules[__name__], f'__{defuzz_type}', None)
    return method(x, mf) if method else None


def __cog(x, mf) -> float:
    """
    Returns the center of gravity of the fuzzy set along the x-axis.
    """

    if len(x) != len(mf):
        raise ValueError("The number of items in 'x' does not math with 'mfs'")

    return np.sum(x * mf) / np.sum(mf)


def __fom(x, mf) -> float:
    """
    Returns the First of Maximum of the fuzzy set along the x-axis.
    """

    if len(x) != len(mf):
        raise ValueError("The number of items in 'x' does not math with 'mfs'")

    return x[np.argmax(mf)]


def __lom(x, mf) -> float:
    """
    Returns the Last of Maximum of the fuzzy set along the x-axis.
    """

    if len(x) != len(mf):
        raise ValueError("The number of items in 'x' does not math with 'mfs'")

    y = np.where(mf == mf.max())
    return x[y[0][-1]]


def __mom(x, mf) -> float:
    """
    Returns the Middle of Maximum of the fuzzy set along the x-axis.
    """

    if len(x) != len(mf):
        raise ValueError("The number of items in 'x' does not math with 'mfs'")

    y = np.where(mf == mf.max())
    return (x[y[0][0]] + x[y[0][-1]]) / 2
