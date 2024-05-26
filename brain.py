from bone import bones, muscles
from update import efforts, update_model, l_gravity_center, l_efforts, l_Q
from utils import *
from constants import *


def make_decision():

    global efforts

    preset1 = [Q, 0.001, 10 ** - 3 / t, 0.7]  # k needs to be larger for smaller t
    l_Q.append(Q(True))
    efforts = gradient_descent(efforts, Q, 0.001, 10 ** - 3 / t, 0.7)
    l_efforts.append(l_copy(efforts))

    return efforts


def gradient_descent(v, f, epsilon, k, gamma, n=0):

    m = len(muscles)
    
    x = v.copy()
    l_dN = [i / 1000 for i in range(-1, 2)]
    state = [bone.get_state() for bone in bones]
    nabla = np.zeros(m)  # gradient to compute

    for i in range(m):
        values = []

        for dN in l_dN:
            update_model(x + dN * e_i(i, m), shallow_update=True)  # shallow to enhance performances
            values.append(f())
            reverse_changes(state)

        nabla[i] = least_squares_method(l_dN, values)  # compute df/dxi

    v = bound(v + k * gamma ** n * nabla)

    if Ninf(v - x) < epsilon:
        return v

    return gradient_descent(v, f, epsilon, k, gamma, n + 1)


def Q(explicit=False):

    a = 50 / t
    b = - 1 * 10 ** 7
    c = - 1 * 10 ** 3
    d = - 1 * 10 ** 4
    e = - 2 * 10 ** - 6

    y1 = a * (bones[2].end[1] - 0.8)  # - 0.8 to get better graphs later
    y2 = b * (l_gravity_center[-1][0] - 0.14) ** 2
    y3 = c * ((l_gravity_center[-1][0] - l_gravity_center[-2][0]) / t) ** 2  # dy3/dt
    y4 = d * g(bones[2].end[0], bones[3].end[0], bones[0].end[0])
    y5 = e * ((y4 + l_Q[-1][4])/t) ** 2  # dy4/dt '+' because  l_Q[-1][4] = - y4
    y = y1 + y2 + y3 + y4 + y5

    if explicit:
        return y, y1, -y2, -y3, -y4, -y5

    return y


def g(x, y, z):
    return ((x - y) ** 2 + (x - z) ** 2 + (y - z) ** 2) ** 0.5


def e_i(i, j):
    e = np.zeros(j)
    e[i] = 1
    return e


def bound(x):
    n = len(x)
    y = np.zeros(n)
    for i in range(n):
        if x[i] > 0:
            y[i] = min(x[i], 1)
    return y


def reverse_changes(state):
    for bone in bones:
        bone.l_theta.pop()
        bone.theta = bone.l_theta[-1]
        bone.set_state(state[bone.index])
    l_gravity_center.pop()
