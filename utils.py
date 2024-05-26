from constants import t


def N2(v):
    return sum(x ** 2 for x in v) ** 0.5


def Ninf(v):
    return max(abs(x) for x in v)


def differentiate(f):
    return [(f[i+1] - f[i]) / t for i in range(len(f) - 1)]


def integrate(f):
    F = [0]
    for i in range(len(f)):
        F.append(F[-1] + t * f[i])
    return F


def dot_product(x, y):
    return sum(x[i] * y[i] for i in range(len(x)))


def l_copy(v):
    return [e for e in v]


def least_squares_method(x, y):  # gives the slope
    s = sum(x)
    n = len(x)
    return (n * dot_product(x, y) - s * sum(y)) / (n * dot_product(x, x) - s ** 2)
