from utils import norm
from constants import g


def kinetic_energy(bone):
    return (0.5 * bone.moment_of_inertia * bone.angular_velocity() ** 2
            + 0.5 * bone.mass * norm(bone.absolute_velocity()) ** 2)


def potential_energy(bone):
    return bone.mass * g * bone.gravity_center()[1] - bone.Ep0


def total_kinetic_energy(bones):
    return sum(kinetic_energy(bone) for bone in bones)


def total_potential_energy(bones):
    return sum(potential_energy(bone) for bone in bones)

