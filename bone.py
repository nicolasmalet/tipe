from numpy import sin, cos, pi
from utils import *
from constants import *


class Bone:
    def __init__(self, name, previous_bone, length, theta0, mass, color):
    
        self.name = name
        self.previous_bone = previous_bone
        self.index = self.get_index()
        self.r = length
        self.m = mass
        self.color = color
        self.J = 1 / 12 * mass * length ** 2  # moment of inertia for the axis around the center of gravity
        self.muscles = []  # set it later
        self.Ep0 = 0  # set it later
        
        self.theta = theta0
        self.l_theta = [theta0, theta0, theta0]
        
        self.e_r = self.compute_e_r()
        self.e_theta = self.compute_e_theta()
        
        self.origin = self.compute_origin()
        self.end = self.compute_end()

        self.theta_dot = self.compute_theta_dot()

        self.G = self.compute_G()
        self.G_dot = [0, 0]

        self.relative_to_absolute_matrix = self.compute_relative_to_absolute_matrix()

    def update(self):
        self.e_r = self.compute_e_r()
        self.e_theta = self.compute_e_theta()
        
        self.origin = self.compute_origin()
        self.end = self.compute_end()
    
        self.theta_dot = self.compute_theta_dot()
    
        self.G = self.compute_G()
        self.G_dot = self.compute_G_dot()
    
        self.relative_to_absolute_matrix = self.compute_relative_to_absolute_matrix()
    
    def get_index(self):
        if self.previous_bone is None:
            return -1
        return self.previous_bone.index + 1

    def compute_origin(self):
        if self.previous_bone is None:
            return [0, 0]
        return self.previous_bone.end

    def compute_end(self):
        return v_sum(self.origin, [self.r * sin(self.theta), - self.r * cos(self.theta)])

    def compute_e_theta(self):  # coordinates of the eth vector
        return [cos(self.theta), sin(self.theta)]

    def compute_e_r(self):  # coordinates of the eth vector
        return [sin(self.theta), -cos(self.theta)]

    def compute_G(self):  # coordinates of the gravity center
        return scalar_mul(0.5, v_sum(self.origin, self.end))

    def compute_relative_to_absolute_matrix(self):
        s = sin(self.theta)
        c = cos(self.theta)
        return [[s, c], [- c, s]]

    def compute_theta_dot(self):
        return (self.l_theta[-1] - self.l_theta[-2]) / t

    def compute_theta_2dot(self):
        return (self.l_theta[-1] - 2 * self.l_theta[-2] + self.l_theta[-3]) / t ** 2

    def compute_G_dot(self):  # velocity of the center of gravity
        return v_sum(scalar_mul(0.5 * self.r * self.theta_dot, self.e_theta),
                     v_list_sum([scalar_mul(bones[i].r * bones[i].theta_dot, bones[i].e_theta)
                                 for i in range(self.index)]))

    def compute_tendon_position(self, muscle):
        return muscle.tendon_position(self, bones)

    def compute_v_tendon(self, muscle):  # velocity of the tendon linking those specific bone and muscle
        return v_sum(v_list_sum([scalar_mul(bones[i].r * bones[i].theta_dot, bones[i].e_theta)
                                 for i in range(self.index)]),
                     scalar_mul(self.theta_dot * muscle.origin_to_tendon_length(self), self.e_theta))

    def F_muscle(self, muscle, effort):  # force exerted by a muscle on this bone
        u = v_sub(muscle.tendon_position(muscle.other_bone(self)), muscle.tendon_position(self))
        if (norm := N2(u)) != 0:
            u = scalar_mul(1 / norm, u)  # normalize vector
        return scalar_mul(effort * muscle.max_force, u)

    def F_tot(self, efforts):  # add up the forces exerted by the muscles on this bone
        F_tot_muscle = v_list_sum([self.F_muscle(muscle, efforts[muscle.index]) for muscle in self.muscles])
        F_gravity = [0, - self.m * g]
        return v_sum(F_tot_muscle, F_gravity)

    def C_muscle(self, muscle, effort):  # torque exerted by a muscle on this bone
        OM = v_sub(muscle.tendon_position(self), self.G)
        F = self.F_muscle(muscle, effort)
        return OM[0] * F[1] - OM[1] * F[0]

    def C_tot(self, efforts):  # add up the torque exerted by the muscles on this bone
        C_tot_muscle = sum([self.C_muscle(muscle, efforts[muscle.index]) for muscle in self.muscles])
        return C_tot_muscle


class Muscle:
    def __init__(self, name, index, bone0, bone1, relative_start, relative_end, max_force, color):

        self.name = name
        self.index = index
        self.bone0 = bone0
        self.bone1 = bone1
        self.relative_0 = relative_start
        self.relative_1 = relative_end
        self.max_force = max_force
        self.color = color

    def origin(self):
        return v_sum(self.bone0.origin, change_basis(self.bone0.relative_to_absolute_matrix, self.relative_0))

    def end(self):
        return v_sum(self.bone1.origin, change_basis(self.bone1.relative_to_absolute_matrix, self.relative_1))

    def other_bone(self, bone):
        return self.bone1 if bone == self.bone0 else self.bone0

    def tendon_position(self, bone):
        return v_sum(bone.origin,
                     change_basis(bone.relative_to_absolute_matrix, self.relative_tendon_position(bone)))

    def relative_tendon_position(self, bone):
        if bone == self.bone0:
            return self.relative_0
        else:
            return self.relative_1

    def origin_to_tendon_length(self, bone):
        return N2(self.relative_tendon_position(bone))


l_gravity_center = []


def update_gravity_center(_bones):  # compute the center of mass of the system
    l_gravity_center.append(scalar_mul(1 / (sum([bone.m for bone in _bones])),
                                       v_list_sum([scalar_mul(bone.m, bone.G) for bone in _bones])))


def reverse_l_gravity_center_changes():
    l_gravity_center.pop()


def assign_muscles():
    for bone in bones:
        for muscle in muscles:
            if muscle.bone0 == bone or muscle.bone1 == bone:
                bone.muscles.append(muscle)


def reset_bones():
    for bone in bones:
        bone.l_theta = bone.l_theta[0:3]
        bone.theta = bone.l_theta[-1]
        bone.e_r = bone.compute_e_r()
        bone.e_theta = bone.compute_e_theta()
        
        bone.origin = bone.compute_origin()
        bone.end = bone.compute_end()
    
        bone.theta_dot = bone.compute_theta_dot()
    
        bone.G = bone.compute_G()
        bone.G_dot = [0, 0]
    
        bone.relative_to_absolute_matrix = bone.compute_relative_to_absolute_matrix()


def set_Ep0():  # so that for t = 0 Ep(t) = Ep(0) - Ep0 = 0
    for bone in bones:
        bone.Ep0 = bone.m * g * bone.G[1]


#


ground = Bone('ground', None, 0, pi / 2, 0, bone_color)
tibia = Bone('tibia', ground, 0.49, 2.741458842809701, 6, bone_color)
femur = Bone('femur', tibia, 0.40, -1.8715338360867622, 14, bone_color)
back = Bone('back', femur, 0.49, 2.2449909691894687, 38, bone_color)
arm = Bone('arm', back, 0.65, -0.0016569258724953163, 8 + bar_mass, bone_color)  # we condider the mass of the bar here

calves = Muscle('calves', 0, ground, tibia, [-0.05, 0], [0.4, 0], 10000, muscle_color)
quadriceps = Muscle('quadriceps', 1, tibia, femur, [0.55, 0], [0.35, 0], 10000, muscle_color)
hamstrings = Muscle('hamstrings', 2, femur, back, [0.05, 0], [-0.05, 0], 10000, muscle_color)
low_back = Muscle('low back', 3, femur, back, [0.45, 0], [0.44, 0], 10000, muscle_color)
lats_and_delt = Muscle('lats_and_delt', 4, back, arm, [0.05, 0], [0.05, 0], 2000, muscle_color)

bones = [tibia, femur, back, arm]

muscles = [calves, quadriceps, hamstrings, low_back, lats_and_delt]

n = len(bones)

assign_muscles()

update_gravity_center(bones)
update_gravity_center(bones)

set_Ep0()
