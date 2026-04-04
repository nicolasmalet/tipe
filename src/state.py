from copy import deepcopy

import numpy as np

from bone import Bone, Muscle
from config import g, bar_mass, muscle_color, bone_color
from energy import total_potential_energy, get_gravity_center

calves = Muscle('calves', 0, [-0.05, 0], [0.4, 0], 10000, muscle_color)
quadriceps = Muscle('quadriceps', 1, [0.55, 0], [0.35, 0], 10000, muscle_color)
hamstrings = Muscle('hamstrings', 2, [0.05, 0], [-0.05, 0], 10000, muscle_color)
low_back = Muscle('low back', 3, [0.45, 0], [0.44, 0], 10000, muscle_color)
lats = Muscle('lats', 4, [0.05, 0], [0.05, 0], 2000, muscle_color)

ground = Bone('ground', None, [calves], 0, np.pi / 2, 0, bone_color)
tibia = Bone('tibia', ground, [calves, quadriceps], 0.49, 2.758207465905639, 6, bone_color)
femur = Bone('femur', tibia, [quadriceps, hamstrings, low_back], 0.40, -1.8630010384296538, 14, bone_color)
back = Bone('back', femur, [hamstrings, low_back, lats], 0.49, 2.2435477244889137, 38, bone_color)
arm = Bone('arm', back, [lats], 0.65, -0.005690488236282301, 8 + bar_mass, bone_color)

bones: list[Bone] = [tibia, femur, back, arm]
muscles: list[Muscle] = [calves, quadriceps, hamstrings, low_back, lats]


def assign_muscles_to_bones() -> None:
    """
    Links muscles to their respective bones based on the global muscles and bones lists.
    """
    for bone in [ground] + bones:
        for muscle in muscles:
            if muscle in bone.muscles:
                if muscle.bone0 is None:
                    muscle.bone0 = bone
                else:
                    muscle.bone1 = bone


def reset_bones() -> None:
    """
    Resets all bones to their initial state.
    """
    for bone in bones:
        bone.l_theta = bone.l_theta[0:3]
        bone.theta = bone.l_theta[-1]
        bone.set_state(bone.first_state)


def set_Ep0() -> None:
    """
    Sets the initial potential energy reference for each bone so that Ep(0) is 0.
    """
    for bone in bones:
        bone.Ep0 = bone.m * g * bone.G[1]


assign_muscles_to_bones()

for bone in bones:
    bone.update()
    bone.first_state = deepcopy(bone.get_state())

set_Ep0()

efforts: np.ndarray = np.array([0.36, 0.68, 1, 1, 0])
l_efforts: list[np.ndarray] = [efforts]

l_Q: list[list[float]] = [
    [-1532.1913424428103, 3749.6096493863097, 24.366758337800864, 0.0, 51.02162584457079, 5206.412607646748]]

Ec: list[float] = [0.0]
Ep: list[float] = [total_potential_energy(bones)]
l_p_muscle: list[list[float]] = [[0.0] for _ in range(len(muscles))]

l_gravity_center: list[np.ndarray] = [get_gravity_center(bones), get_gravity_center(bones)]
