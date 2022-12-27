def jaccard_measure(a, b):
    min_lmf = (min(a, b) for a, b in zip(a['lmf'], b['lmf']))
    max_lmf = (max(a, b) for a, b in zip(a['lmf'], b['lmf']))
    min_umf = (min(a, b) for a, b in zip(a['umf'], b['umf']))
    max_umf = (max(a, b) for a, b in zip(a['umf'], b['umf']))

    return (sum(min_umf) + sum(min_lmf)) / (sum(max_umf) + sum(max_lmf))