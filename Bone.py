from numpy import sin, cos, pi
from utils import v_sum, v_sub, scalar_mul, v_list_sum, change_basis, norm
from constants import g, t

bone_color = (255, 255, 255)
muscle_color = (255, 0, 0)


class Bone:
    def __init__(self, index, length, theta0, mass, color):
        self.index = index
        self.r = length
        self.m = mass
        self.theta = theta0
        self.l_theta = [theta0, theta0, theta0]
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

    def theta_dot_dot(self):
        return (self.l_theta[-1] - 2 * self.l_theta[-2] + self.l_theta[-3]) / t ** 2

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


bone0 = Bone(0, 0.5, 1, 1, bone_color)
bone1 = Bone(1, 0.5, 1, 1, bone_color)
bone2 = Bone(2, 0.5, 1, 1, bone_color)
bone3 = Bone(3, 0.5, 1, 1, bone_color)

muscle01 = Muscle(bone0, bone1, [0.25, 0], [0.25, 0], 30, muscle_color)
muscle12 = Muscle(bone1, bone2, [0.25, 0], [0.25, 0], 20, muscle_color)
muscle23 = Muscle(bone2, bone3, [0.25, 0], [0.25, 0], 10, muscle_color)

bones = [bone0, bone1, bone2, bone3]
muscles = [muscle01, muscle12, muscle23]

bone0.muscles = [muscle01]
bone1.muscles = [muscle01, muscle12]
bone2.muscles = [muscle12, muscle23]
bone3.muscles = [muscle23]

set_Ep0()
