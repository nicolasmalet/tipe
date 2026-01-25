from state import bones
from config import t

from typing import List
import numpy as np


def a_ij(i: int, j: int, n: int, c: List[float], s: List[float]) -> float:
    """
    Computes the coefficient A[i, j] for the system matrix A.
    """
    qi, qj = i // n, j // n
    ri, rj = i % n, j % n

    if qi == 0:
        if qj == 0:
            if ri == rj:
                return bones[ri].m * bones[ri].r * c[ri] / 2 / t ** 2
            if ri > rj:
                return bones[ri].m * bones[rj].r * c[rj] / t ** 2
        if qj == 1:
            if rj == ri:
                return -1
            if rj == ri + 1:
                return 1

    if qi == 1:
        if qj == 0:
            if ri == rj:
                return bones[ri].m * bones[ri].r * s[ri] / 2 / t ** 2
            if ri > rj:
                return bones[ri].m * bones[rj].r * s[rj] / t ** 2
        if qj == 2:
            if rj == ri:
                return -1
            if rj == ri + 1:
                return 1

    if qi == 2:
        if qj == 0:
            if ri == rj:
                return bones[ri].J / t ** 2
        if qj == 1:
            if rj == ri:
                return bones[ri].r * c[ri] / 2
            if rj == ri + 1:
                return bones[ri].r * c[ri] / 2
        if qj == 2:
            if rj == ri:
                return bones[ri].r * s[ri] / 2
            if rj == ri + 1:
                return bones[ri].r * s[ri] / 2
    return 0


def b_i(i: int, n: int, c: List[float], s: List[float], l_forces: List[np.ndarray], l_torques: List[float]) -> float:
    """
    Computes the coefficient B[i] for the system vector B.
    """
    q, index = i // n, i % n
    bone = bones[index]
    th = bone.l_theta[-1]
    _th = bone.l_theta[-2]

    if q == 2:
        return bone.J / t ** 2 * (2 * th - _th) + l_torques[index]

    m = bone.m
    r = bone.r
    th_dot = bone.theta_dot

    if q == 0:
        return (l_forces[index][0] + m * r / 2 / t ** 2 * (c[index] * (2 * th - _th) + s[index] * (t * th_dot) ** 2) +
                m / t ** 2 * sum(bones[p].r * (c[p] * (2 * bones[p].theta - bones[p].l_theta[-2]) +
                                               s[p] * (bones[p].theta - bones[p].l_theta[-2]) ** 2)
                                 for p in range(0, index)))

    return (l_forces[index][1] + m * r / 2 / t ** 2 * (s[index] * (2 * th - _th) - c[index] * (t * th_dot) ** 2) +
            m / t ** 2 * sum(bones[p].r * (s[p] * (2 * bones[p].theta - bones[p].l_theta[-2]) -
                                           c[p] * (bones[p].theta - bones[p].l_theta[-2]) ** 2)
                             for p in range(0, index)))