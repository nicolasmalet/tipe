from constants import t
from bone import bones


def a_ij(i, j, n, c, s):  # return the aij coefficient of A a 3nx3n matrix

    # we will work on nxn blocs
    qi, qj = i // n, j // n
    ri, rj = i % n, j % n

    if qi == 0:  # first equation
        if qj == 0:  # set thetas
            if ri == rj:
                return bones[ri].m * bones[ri].r * c[ri] / 2 / t ** 2
            if ri > rj:
                return bones[ri].m * bones[rj].r * c[rj] / t ** 2
        if qj == 1:  # set Rxs
            if rj == ri:
                return -1
            if rj == ri + 1:
                return 1

    if qi == 1:  # second equation
        if qj == 0:  # set thetas
            if ri == rj:
                return bones[ri].m * bones[ri].r * s[ri] / 2 / t ** 2
            if ri > rj:
                return bones[ri].m * bones[rj].r * s[rj] / t ** 2
        if qj == 2:  # set Rys
            if rj == ri:
                return -1
            if rj == ri + 1:
                return 1

    if qi == 2:  # third equation
        if qj == 0:  # set thetas
            if ri == rj:
                return bones[ri].J / t ** 2
        if qj == 1:  # set Rx
            if rj == ri:
                return bones[ri].r * c[ri] / 2
            if rj == ri + 1:
                return bones[ri].r * c[ri] / 2
        if qj == 2:  # set Ry
            if rj == ri:
                return bones[ri].r * s[ri] / 2
            if rj == ri + 1:
                return bones[ri].r * s[ri] / 2
    return 0  # everywhere else


def b_i(i, n, c, s, l_forces, l_torques):  # return the bi coefficient of b

    q, index = i // n, i % n
    bone = bones[index]
    th = bone.l_theta[-1]  # is theta_k in euler's method
    _th = bone.l_theta[-2]  # is theta_k-1 in euler's method

    if q == 2:  # third equation
        return bone.J / t ** 2 * (2 * th - _th) + l_torques[index]

    m = bone.m
    r = bone.r
    th_dot = bone.theta_dot

    if q == 0:  # first equation
        return (l_forces[index][0] + m * r / 2 / t ** 2 * (c[index] * (2 * th - _th) + s[index] * (t * th_dot) ** 2) +
                m / t ** 2 * sum(bones[p].r * (c[p] * (2 * bones[p].theta - bones[p].l_theta[-2]) +
                                               s[p] * (bones[p].theta - bones[p].l_theta[-2]) ** 2)
                                 for p in range(0, index)))

    # second equation

    return (l_forces[index][1] + m * r / 2 / t ** 2 * (s[index] * (2 * th - _th) - c[index] * (t * th_dot) ** 2) +
            m / t ** 2 * sum(bones[p].r * (s[p] * (2 * bones[p].theta - bones[p].l_theta[-2]) -
                                           c[p] * (bones[p].theta - bones[p].l_theta[-2]) ** 2)
                             for p in range(0, index)))
