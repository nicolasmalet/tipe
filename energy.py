from utils import norm, dot_product
from constants import g


def kinetic_energy(bone, bones):
    return 0.5 * bone.J * bone.theta_dot() ** 2 + 0.5 * bone.m * norm(bone.G_dot(bones)) ** 2


def potential_energy(bone, bones):
    return bone.m * g * bone.G(bones)[1] - bone.Ep0


def total_kinetic_energy(bones):
    return sum(kinetic_energy(bone, bones) for bone in bones)


def total_potential_energy(bones):
    return sum(potential_energy(bone, bones) for bone in bones)


def P_muscle(bones, muscle):
    return (dot_product(muscle.bone0.F_muscle(bones, muscle, 1), muscle.bone0.v_tendon(bones, muscle)) +
            dot_product(muscle.bone1.F_muscle(bones, muscle, 1), muscle.bone1.v_tendon(bones, muscle)))
