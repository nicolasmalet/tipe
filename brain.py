import bone
from update import update_model
import plot
from plot import Ep, Ec, l_p_muscle, l_efforts, l_Q
from utils import *
from bone import muscles, l_gravity_center
from constants import *
from copy import deepcopy


def reverse_changes():
    Ec.pop()
    Ep.pop()
    for i in range(len(l_p_muscle)):
        l_p_muscle[i].pop()
    bone.l_gravity_center.pop()
    

def bound1(x):
    if x < 0:
        return 0
    else:
        return min(1, x)


def bound2(x):
    if x < -1:
        return -1
    else:
        return min(1, x)


def e_i(i, j):
    e = [0 for i in range(j)]
    e[i] = 1
    return e


def g(x, y, z):
    return ((x - y) ** 2 + (x - z) ** 2 + (y - z) ** 2) ** 0.5


def Q(bones, explicit=False):

    a = - 20
    b = 10 ** 7
    c = 10 ** 3
    d = 1 * 10 ** 4
    e = 2 * 10 ** - 6

    y1 = a * Ep[-1]
    y2 = b * (l_gravity_center[-1][0] - 0.145) ** 2
    y3 = c * ((l_gravity_center[-1][0] - l_gravity_center[-2][0]) / t) ** 2
    y4 = d * g(bones[2].end[0], bones[3].end[0], bones[0].end[0])
    y5 = e * ((y4 - l_Q[-1][4])/t) ** 2
    y = y1 + y2 + y3 + y4 + y5

    if explicit:
        return y, y1, y2, y3, y4, y5

    return y


preset1 = [Q, 0.001, 99, 10 ** 3 * t, 0.7]  # k needs to be larger for smaller t


def make_decision(bones):
    l_Q.append(Q(bones, True))
    efforts = gradient_descent(bones, plot.efforts, preset1)
    l_efforts.append(copy(efforts))

    return efforts


def gradient_descent(bones, v, preset, i=0):

    f, accuracy, imax, k, gamma = preset
    
    x = copy(v)

    l_dN = [i / 1000 for i in range(-1, 2)]
    
    for muscle_index in range(len(muscles)):
        values = []

        for dN in l_dN:
            c_bones = deepcopy(bones)  # create a copy in order to not change the real model
            update_model(c_bones, l_sum(x, scalar_mul(dN, e_i(muscle_index, len(muscles)))))
            values.append(f(c_bones))
            reverse_changes()

        a = least_squares_method(l_dN, values)  # compute df/dxi
        
        if muscle_index < 4:
            v[muscle_index] = bound1(v[muscle_index] - k * gamma ** i * a)

        else:
            v[muscle_index] = bound2(v[muscle_index] - k * gamma ** i * a)

    if Ninf(l_sub(v, x)) < accuracy:
        return v

    if i > imax:
        return scalar_mul(0.5, l_sum(v, x))  # average between the oscilating values

    return gradient_descent(bones, v, preset, i + 1)
