from utils import N2, dot_product
from constants import *


def kinetic_energy(bone):
    return 0.5 * bone.J * bone.theta_dot ** 2 + 0.5 * bone.m * N2(bone.G_dot) ** 2


def potential_energy(bone):
    return bone.m * g * bone.G[1] - bone.Ep0


def total_kinetic_energy(bones):
    return sum(kinetic_energy(bone) for bone in bones)


def total_potential_energy(bones):
    return sum(potential_energy(bone) for bone in bones)


def p_muscle(muscle, effort):
    p = 0
    for bone in [muscle.bone0, muscle.bone1]:
        p += dot_product(bone.F_muscle(muscle, effort), bone.G_dot) + \
            bone.C_muscle(muscle, effort) * bone.theta_dot
    return p
