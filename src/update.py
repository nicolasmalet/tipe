from energy import get_gravity_center, total_kinetic_energy, total_potential_energy, p_muscle
from matrix import a_ij, b_i
import state

import numpy as np


n: int = len(state.bones)
m: int = len(state.muscles)


def update_bones(X: np.ndarray, shallow_update: bool = False) -> None:
    """
    Updates the angular position of all bones based on the solution vector X.
    """
    for bone in state.bones:
        bone.theta = X[bone.index]
        bone.l_theta.append(bone.theta)
        bone.update(shallow_update)


def update_model(efforts: np.ndarray, shallow_update: bool = False) -> None:
    """
    Performs a single step of the simulation.
    Constructs and solves the system matrices to find the new state.
    """

    c = [np.cos(bone.theta) for bone in state.bones]
    s = [np.sin(bone.theta) for bone in state.bones]
    l_forces = [bone.F_tot(efforts) for bone in state.bones]
    l_torques = [bone.C_tot(efforts) for bone in state.bones]

    A = np.array([[a_ij(i, j, n, c, s) for j in range(3 * n)] for i in range(3 * n)])
    B = np.array([b_i(i, n, c, s, l_forces, l_torques) for i in range(3 * n)])

    X = np.linalg.solve(A, B)

    update_bones(X, shallow_update)
    update_gravity_center()

    if not shallow_update:
        update_muscle_power(efforts)
        update_energy()


def update_energy() -> None:
    """
    Records the current kinetic and potential energy of the system.
    """
    state.Ec.append(total_kinetic_energy(state.bones))
    state.Ep.append(total_potential_energy(state.bones))


def update_muscle_power(_efforts: np.ndarray) -> None:
    """
    Records the power exerted by each muscle.
    """
    for i in range(m):
        state.l_p_muscle[i].append(p_muscle(state.muscles[i], _efforts[i]))


def update_gravity_center() -> None:
    """
    Calculates and records the position of the center of mass of the entire system.
    """
    state.l_gravity_center.append(get_gravity_center(state.bones))


def reverse_l_gravity_center_changes() -> None:
    """
    Undoes the last gravity center recording.
    """
    state.l_gravity_center.pop()


def reset_energy() -> None:
    """
    Resets the energy recording lists.
    """
    state.Ec[:] = [0.0]
    state.Ep[:] = [total_potential_energy(state.bones)]
    state.l_p_muscle[:] = [[0.0] for _ in range(len(state.muscles))]
