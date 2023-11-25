from numpy import sin, cos, pi
from utils import v_sum, v_sub, scalar_mul, v_list_sum, change_basis, norm
from constants import *


class Bone:
    def __init__(self, index, length, theta0, mass, color):
        self.index = index
        self.r = length
        self.m = mass
        self.theta = theta0
        self.l_theta = [theta0, theta0]
        self.color = color
        self.J = 1 / 12 * mass * length ** 2  # moment of inertia for the axis around the center of gravity
        self.Ep0 = 0  # set it later
        self.muscles = []  # set it later

    def origin(self):
        if self.index == 0:
            return [0, 0]
        else:
            return bones[self.index - 1].end()

    def end(self):
        return v_sum(self.origin(), [self.r * sin(self.theta), - self.r * cos(self.theta)])

    def e_theta(self):  # coordinates of the eth vector
        return [cos(self.theta), sin(self.theta)]

    def e_r(self):  # coordinates of the eth vector
        return [sin(self.theta), -cos(self.theta)]

    def G(self):  # coordinates of the gravity center
        return scalar_mul(0.5, v_sum(self.origin(), self.end()))

    def relative_to_absolute_matrix(self):
        return [[sin(self.theta), cos(self.theta)], [- cos(self.theta), sin(self.theta)]]

    def theta_dot(self):
        return (self.l_theta[-1] - self.l_theta[-2]) / t

    def G_dot(self):  # velocity of the center of gravity
        return v_sum(scalar_mul(0.5 * self.r * self.theta_dot(), self.e_theta()),
                     v_list_sum([scalar_mul(bones[i].r * bones[i].theta_dot(), bones[i].e_theta())
                                 for i in range(self.index)]))

    def tendon_position(self, muscle):
        return muscle.tendon_position(self)

    def v_tendon(self, muscle):  # velocity of the tendon linking those specific bone and muscle
        return v_sum(v_list_sum([scalar_mul(bones[i].r * bones[i].theta_dot(), bones[i].e_theta())
                                 for i in range(self.index)]),
                     scalar_mul(self.theta_dot() * muscle.origin_to_tendon_length(self), self.e_theta()))

    def F_muscle(self, muscle, effort):  # force exerted by a muscle on this bone
        u = v_sub(muscle.tendon_position(muscle.other_bone(self)), muscle.tendon_position(self))
        u = scalar_mul(1 / norm(u), u)  # unit vector
        return scalar_mul(effort * muscle.max_force, u)

    def F_tot_muscle(self, effort):  # add up the forces exerted by the muscles on this bone
        return v_list_sum([self.F_muscle(muscle, effort) for muscle in self.muscles])

    def C_muscle(self, muscle, effort):  # torque exerted by a muscle on this bone
        OM = v_sub(muscle.tendon_position(self), self.G())
        F = self.F_muscle(muscle, effort)
        return OM[0] * F[1] - OM[1] * F[0]

    def C_tot_muscle(self, effort):  # add up the torque exerted by the muscles on this bone
        return sum([self.C_muscle(muscle, effort) for muscle in self.muscles])


def set_Ep0():  # so that for t = 0 Ep(t) = Ep(0) - Ep0 = 0
    for bone in bones:
        bone.Ep0 = bone.m * g * bone.G()[1]


class Muscle:
    def __init__(self, bone0, bone1, relative_start, relative_end, max_force, color):
        self.bone0 = bone0
        self.bone1 = bone1
        self.relative_0 = relative_start
        self.relative_1 = relative_end
        self.max_force = max_force
        self.color = color

    def origin(self):
        return v_sum(self.bone0.origin(), change_basis(self.bone0.relative_to_absolute_matrix(), self.relative_0))

    def end(self):
        return v_sum(self.bone1.origin(), change_basis(self.bone1.relative_to_absolute_matrix(), self.relative_1))

    def other_bone(self, bone):
        return self.bone1 if bone == self.bone0 else self.bone0

    def tendon_position(self, bone):
        return v_sum(bone.origin(),
                     change_basis(bone.relative_to_absolute_matrix(), self.relative_tendon_position(bone)))

    def relative_tendon_position(self, bone):
        if bone == self.bone0:
            return self.relative_0
        else:
            return self.relative_1

    def origin_to_tendon_length(self, bone):
        return norm(self.relative_tendon_position(bone))


#

ground = Bone(0, 1, pi/2, 0, bone_color)
tibia = Bone(0, 0.49, - 5 * pi / 6, 6, bone_color)
femur = Bone(1, 0.43, 4 * pi / 6, 14, bone_color)
back = Bone(2, 0.53, -4 * pi / 6, 38, bone_color)
arm = Bone(3, 0.70, 0, 8, bone_color)

calves = Muscle(ground, tibia, [0.05, 0], [0.4, 0], 5000, muscle_color)
quadriceps = Muscle(tibia, femur, [0.55, 0], [0.35, 0], 5000, muscle_color)
hamstrings = Muscle(femur, back, [0.1, 0], [-0.05, 0], 5000, muscle_color)
lats = Muscle(back, arm, [0.1, 0], [0.1, 0], 5000, muscle_color)

bones = [tibia, femur, back, arm]

muscles = [calves, quadriceps, hamstrings, lats]

tibia.muscles = [calves, quadriceps]
femur.muscles = [quadriceps, hamstrings]
back.muscles = [hamstrings, lats]
arm.muscles = [lats]


set_Ep0()
