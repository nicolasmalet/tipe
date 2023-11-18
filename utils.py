from constants import t


def v_sum(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def v_sub(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]


def v_list_sum(v_list):
    return sum(v_list[i][0] for i in range(len(v_list))), sum(v_list[i][1] for i in range(len(v_list)))


def scalar_mul(x, v):
    return x * v[0], x * v[1]


def change_basis(p, x):
    return [p[0][0] * x[0] + p[0][1] * x[1], p[1][0] * x[0] + p[1][1] * x[1]]


def norm(v):
    return (v[0] ** 2 + v[1] ** 2) ** 0.5


def l_sum(l1, l2):
    return [l1[i] + l2[i] for i in range(len(l1))]


def differentiate(l):
    return [(l[i+1] - l[i]) / t for i in range(len(l) - 1)]


def integrate(l):
    I = [0]
    for i in range(len(l)):
        I.append(I[-1] + t * l[i])
    return I


def generalized_l_sum(l):
    return [sum(l[i][j] for i in range(len(l))) for j in range(len(l[0]))]


def dot_product(x, y):
    return x[0] * y[0] + x[1] * y[1]


