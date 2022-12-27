import numpy as np


def __L_R_points_interpreter(lmf, umf, L, R):
    if L > R:
        L, R = R, L

    res = np.zeros(len(lmf))
    for i in range(L):
        res[i] = umf[i]
    for i in range(L, R):
        res[i] = lmf[i]
    for i in range(R, len(lmf)):
        res[i] = umf[i]
    return res


def __search_switch_point(x, y: float):
    return np.argmax(x >= y)


def EKM(x, lmf, umf, periods=100):
    if not max(lmf):
        return umf
    # EKM algorithm for L point.
    L = 0
    # Step 1.
    a, b, = 0, 0
    k = round(len(x) / 2.4)

    a += sum(x[i] * umf[i] for i in range(k))
    b += sum(umf[i] for i in range(k))
    a += sum(x[i] * lmf[i] for i in range(k, len(x)))
    b += sum(lmf[i] for i in range(k, len(x)))

    y = a / b if b else 0

    k_1, iteration = 0, 0
    while iteration <= periods:
        # Step 2.
        k_1 = __search_switch_point(x, y)

        # Step 3.
        if k == k_1:
            break

        # Step 4.
        # Signum Function.
        s = (lambda x: x and (1, -1)[x < 0])(k_1 - k)

        a_1 = sum(x[i] * (umf[i] - lmf[i]) for i in range(min(k, k_1), max(k, k_1) - 1))
        b_1 = sum(umf[i] - lmf[i] for i in range(min(k, k_1), max(k, k_1) - 1))

        a_1 = a + s * a_1
        b_1 = b + s * b_1
        y_1 = a_1 / b_1 if b_1 else 0

        # Step 5.
        a, b, k, y = a_1, b_1, k_1, y_1
        iteration += 1

    # Step 6
    L = round((k + k_1) / 2) if iteration == periods else k

    # EKM algorithm for R point.
    R = 0
    # Step 1.
    a, b = 0, 0

    k = round(len(x) / 1.7)
    for i in range(k):
        a += x[i] * lmf[i]
        b += lmf[i]

    for i in range(k, len(x)):
        a += x[i] * umf[i]
        b += umf[i]

    y = a / b if b else 0

    k_1, iteration = 0, 0
    while iteration <= periods:
        # Step 2.
        k_1 = __search_switch_point(x, y)

        # Step 3.
        if k == k_1:
            break

        # Step 4.
        # Signum Function.
        s = (lambda x: x and (1, -1)[x < 0])(k_1 - k)

        a_1, b_1 = 0, 0
        for i in range(min(k, k_1), max(k, k_1) - 1):
            a_1 -= x[i] * (umf[i] - lmf[i])
            b_1 -= umf[i] - lmf[i]

        a_1 = a + s * a_1
        b_1 = b + s * b_1
        y_1 = a_1 / b_1 if b_1 else 0

        # Step 5.
        a, b, k, y = a_1, b_1, k_1, y_1
        iteration += 1
    # Step 6
    R = round((k + k_1) / 2) if iteration == periods else k
    return __L_R_points_interpreter(lmf, umf, L, R)