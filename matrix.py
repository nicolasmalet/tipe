from numpy import cos, sin
from constants import g, t


def a_ij(i, j, n, bones):  # return the aij coefficient of A

    # we will work on nxn blocs
    qi, qj = i // n, j // n
    ri, rj = i % n, j % n

    if qi == 0:  # first equation
        if qj == 0:  # set thetas
            if ri == rj:
                return bones[ri].m * bones[ri].r * cos(bones[ri].theta) / 2 / t ** 2
            if ri > rj:
                return bones[ri].m * bones[rj].r * cos(bones[rj].theta) / t ** 2
        if qj == 1:  # set Rxs
            if rj == ri:
                return -1
            if rj == ri + 1:
                return 1

    if qi == 1:  # second equation
        if qj == 0:  # set thetas
            if ri == rj:
                return bones[ri].m * bones[ri].r * sin(bones[ri].theta) / 2 / t ** 2
            if ri > rj:
                return bones[ri].m * bones[rj].r * sin(bones[rj].theta) / t ** 2
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
                return bones[ri].r * cos(bones[ri].theta) / 2
            if rj == ri + 1:
                return bones[ri].r * cos(bones[ri].theta) / 2
        if qj == 2:  # set Ry
            if rj == ri:
                return bones[ri].r * sin(bones[ri].theta) / 2
            if rj == ri + 1:
                return bones[ri].r * sin(bones[ri].theta) / 2
    return 0  # everywhere else


def b_i(i, n, bones, efforts):  # return the bi coefficient of b

    q, rest = i // n, i % n
    bone = bones[rest]
    efforts = efforts
    m = bone.m
    r = bone.r
    th = bone.l_theta[-1]  # is theta_k in euler's method
    _th = bone.l_theta[-2]  # is theta_k-1 in euler's method
    th_dot = bone.theta_dot()
    j = bone.J

    fm = bone.F_tot_muscle(bones, efforts)
    tm = bone.C_tot_muscle(bones, efforts)

    if q == 0:
        return (fm[0] + m * r / 2 / t ** 2 * (cos(th) * (2 * th - _th) + sin(th) * (t * th_dot) ** 2) +
                m / t ** 2 * sum(bones[p].r * (cos(bones[p].theta) * (2 * bones[p].theta - bones[p].l_theta[-2]) +
                                               sin(bones[p].theta) * (bones[p].theta - bones[p].l_theta[-2]) ** 2)
                                 for p in range(0, rest)))
    if q == 1:
        return (fm[1] + m * r / 2 / t ** 2 * (sin(th) * (2 * th - _th) - cos(th) * (t * th_dot) ** 2) - m * g +
                m / t ** 2 * sum(bones[p].r * (sin(bones[p].theta) * (2 * bones[p].theta - bones[p].l_theta[-2]) -
                                               cos(bones[p].theta) * (bones[p].theta - bones[p].l_theta[-2]) ** 2)
                                 for p in range(0, rest)))
    else:
        return j / t ** 2 * (2 * th - _th) + tm
