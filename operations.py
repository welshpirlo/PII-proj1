import numpy
import numpy as np


def t2_fuzzy_min(term, lmf, umf):
    lmf = np.minimum(lmf, term['lmf'])
    umf = np.minimum(umf, term['umf'])

    return lmf, umf


def t2_fuzzy_union(*mfs):
    """
    Returns the Union of T2 MF
    """

    lmfs = [lmf for lmf, _ in mfs]
    umfs = [umf for _, umf in mfs]

    lmf = np.amax(np.array(lmfs), axis=0)
    umf = np.amax(np.array(umfs), axis=0)
    return lmf, umf
