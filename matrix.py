from numpy import cos, sin
from constants import g, t


def a(i, j, n, bones):

    # we will work on nxn blocs
    qi, qj = i // n, j // n
    ri, rj = i % n, j % n

    if qi == 0:  # first equation
        if qj == 0:  # set thetas
            if ri == rj:
                return bones[ri].mass * bones[ri].length * cos(bones[ri].angle) / 2 / t ** 2
            if ri > rj:
                return bones[ri].mass * bones[rj].length * cos(bones[rj].angle) / t ** 2
        if qj == 1:  # set Rxs
            if rj == ri:
                return -1
            if rj == ri + 1:
                return 1

    if qi == 1:  # second equation
        if qj == 0:  # set thetas
            if ri == rj:
                return bones[ri].mass * bones[ri].length * sin(bones[ri].angle) / 2 / t ** 2
            if ri > rj:
                return bones[ri].mass * bones[rj].length * sin(bones[rj].angle) / t ** 2
        if qj == 2:  # set Rys
            if rj == ri:
                return -1
            if rj == ri + 1:
                return 1

    if qi == 2:  # third equation
        if qj == 0:  # set thetas
            if ri == rj:
                return bones[ri].moment_of_inertia / t ** 2
        if qj == 1:  # set Rx
            if rj == ri:
                return bones[ri].length * cos(bones[ri].angle) / 2
            if rj == ri + 1:
                return bones[ri].length * cos(bones[ri].angle) / 2
        if qj == 2:  # set Ry
            if rj == ri:
                return bones[ri].length * sin(bones[ri].angle) / 2
            if rj == ri + 1:
                return bones[ri].length * sin(bones[ri].angle) / 2
    return 0  # everywhere else


def b(i, n, bones):

    q, r = i // n, i % n

    m = bones[r].mass
    l = bones[r].length
    th = bones[r].angles[-1]  # is θk in euler's method
    _th = bones[r].angles[-2]  # is θk-1 in euler's method
    J = bones[r].moment_of_inertia

    if q == 0:
        return (m * l / 2 / t ** 2 * (cos(th) * (2 * th - _th) + sin(th) * (th - _th) ** 2) +
                m / t ** 2 * sum(bones[p].length * (cos(bones[p].angle) * (2 * bones[p].angle - bones[p].angles[-2]) +
                                                    sin(bones[p].angle) * (bones[p].angle - bones[p].angles[-2]) ** 2)
                                 for p in range(0, r)))
    if q == 1:
        return (m * l / 2 / t ** 2 * (sin(th) * (2 * th - _th) - cos(th) * (th - _th) ** 2) - m * g +
                m / t ** 2 * sum(bones[p].length * (sin(bones[p].angle) * (2 * bones[p].angle - bones[p].angles[-2]) -
                                                    cos(bones[p].angle) * (bones[p].angle - bones[p].angles[-2]) ** 2)
                                 for p in range(0, r)))
    else:
        return J / t ** 2 * (2 * th - _th)
