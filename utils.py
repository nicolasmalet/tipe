from constants import t


def v_sum(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def v_sub(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]


def v_list_sum(v_list):
    return sum(v_list[i][0] for i in range(len(v_list))), sum(v_list[i][1] for i in range(len(v_list)))


def scalar_mul(a, v):
    return [a * x for x in v]


def change_basis(p, x):
    return [p[0][0] * x[0] + p[0][1] * x[1], p[1][0] * x[0] + p[1][1] * x[1]]


def N2(v):
    return sum(x ** 2 for x in v) ** 0.5


def Ninf(v):
    return max(abs(x) for x in v)


def l_sum(l1, l2):
    return [l1[i] + l2[i] for i in range(len(l1))]


def l_sub(l1, l2):
    return [l1[i] - l2[i] for i in range(len(l1))]


def differentiate(f):
    return [(f[i+1] - f[i]) / t for i in range(len(f) - 1)]


def integrate(f):
    F = [0]
    for i in range(len(f)):
        F.append(F[-1] + t * f[i])
    return F


def generalized_l_sum(m):
    return [sum(m[i][j] for i in range(len(m))) for j in range(len(m[0]))]


def dot_product(x, y):
    return sum(x[i] * y[i] for i in range(len(x)))


def copy(v):
    return [e for e in v]


def barycenter(v1, v2, m1, m2):
    return scalar_mul(1/(m1 + m2), v_sum(scalar_mul(m1, v1), scalar_mul(m2, v2)))


def least_squares_method(x, y):  # gives the slope
    s = sum(x)
    n = len(x)
    return (n * dot_product(x, y) - s * sum(y)) / (n * dot_product(x, x) - s ** 2)
