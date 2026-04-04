from copy import copy
from typing import Callable, List, Union

import numpy as np

import state
from config import t
from update import update_model, reverse_l_gravity_center_changes
from utils import least_squares_method


def make_decision() -> np.ndarray:
    """
    Determines the next set of muscle efforts to optimize the movement using gradient descent.
    """
    state.efforts = gradient_descent(state.efforts, Q, 0.001, 10 ** - 3 / t, 0.7)
    state.l_efforts.append(copy(state.efforts))
    state.l_Q.append(Q(True))

    return state.efforts


def gradient_descent(v: np.ndarray, f: Callable, epsilon: float, k: float, gamma: float, n: int = 0) -> np.ndarray:
    """
    Performs gradient descent optimization to minimize the function f.
    """
    m = len(state.muscles)

    x = v.copy()
    l_dN = np.array([-1, 0, 1]) / 1000
    bone_states = [bone.get_state() for bone in state.bones]
    nabla = np.zeros(m)

    for i in range(m):
        values = np.zeros(3)

        for j, dN in enumerate(l_dN):
            update_model(x + dN * e_i(i, m), shallow_update=True)
            values[j] = f()
            reverse_changes(bone_states)

        nabla[i] = least_squares_method(l_dN, values)

    v = np.clip(v + k * gamma ** n * nabla, 0, 1)

    if np.linalg.norm(v - x, ord=np.inf) < epsilon:
        return v

    return gradient_descent(v, f, epsilon, k, gamma, n + 1)


def Q(explicit: bool = False) -> Union[float, List[float]]:
    """
    The cost/quality function to be optimized. Evaluates the current state of the simulation.
    """
    a = 50 / t
    b = - 1 * 10 ** 7
    c = - 1 * 10 ** 3
    d = - 1 * 10 ** 4
    e = - 2 * 10 ** - 6

    y1 = a * (state.bones[2].end[1] - 0.8)
    y2 = b * (state.l_gravity_center[-1][0] - 0.14) ** 2
    y3 = c * ((state.l_gravity_center[-1][0] - state.l_gravity_center[-2][0]) / t) ** 2
    y4 = d * g(state.bones[2].end[0], state.bones[3].end[0], state.bones[0].end[0])
    y5 = e * ((y4 + state.l_Q[-1][4]) / t) ** 2
    y = y1 + y2 + y3 + y4 + y5

    if explicit:
        return [y, y1, -y2, -y3, -y4, -y5]

    return y


def g(x: float, y: float, z: float) -> float:
    """
    Helper geometry function used in the cost function.
    """
    return ((x - y) ** 2 + (x - z) ** 2 + (y - z) ** 2) ** 0.5


def e_i(i: int, j: int) -> np.ndarray:
    """
    Returns a basis vector with 1 at index i and length j.
    """
    e = np.zeros(j)
    e[i] = 1
    return e


def reverse_changes(saved_bone_states: List[List[np.ndarray]]) -> None:
    """
    Reverts the simulation state to the provided saved state.
    """
    for bone in state.bones:
        bone.l_theta.pop()
        bone.theta = bone.l_theta[-1]
        bone.set_state(saved_bone_states[bone.index])
    reverse_l_gravity_center_changes()
