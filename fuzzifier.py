import numpy as np


def normalization(x, _range):
    x_min, x_max, dx = _range
    return (x - x_min) / (x_max - x_min) * 10


def fuzzification(crisp_values, input_lvs):
    """
    Returns the result of Fuzzification.
    """
    result = {}
    for index, crisp_value in enumerate(crisp_values):
        x = normalization(crisp_value, input_lvs[index]['X'])
        x_curr = np.argmax(input_lvs[index]['U'] >= x)
        result[index] = {}
        for term_name, term in input_lvs[index]['terms'].items():
            if term['umf'][x_curr] > 0:
                result[index][term_name] = term['lmf'][x_curr], term['umf'][x_curr]

    return result
