from constants import *
from utils import N2
from copy import deepcopy


class Bone:
    def __init__(self, name, previous_bone, muscles, length, theta0, mass, color):
    
        self.name = name
        self.previous_bone = previous_bone
        self.index = self.get_index()
        self.r = length
        self.m = mass
        self.color = color
        self.J = 1 / 12 * mass * length ** 2  # moment of inertia for the axis around the center of gravity
        self.muscles = muscles  # set it later
        self.Ep0 = 0  # set it later
        
        self.theta = theta0
        self.l_theta = [theta0, theta0, theta0]
        
        self.e_r, self.e_theta = self.get_e_r_and_e_theta()
        
        self.origin = self.get_origin()
        self.end = self.get_end()

        self.theta_dot = self.get_theta_dot()

        self.G = self.get_G()
        self.G_dot = [0, 0]

        self.P = self.get_P()

        self.F_max_muscles = {}
        self.C_max_muscles = {}

        self.first_statet = None # set it later

    def update(self, shallow_update=False):
        self.e_r, self.e_theta = self.get_e_r_and_e_theta()

        self.origin = self.get_origin()
        self.end = self.get_end()

        self.P = self.get_P()

        self.G = self.get_G()

        if not shallow_update:

            self.theta_dot = self.get_theta_dot()

            self.G_dot = self.get_G_dot()

            for muscle in self.muscles:
                self.F_max_muscles[muscle.name] = self.get_F_max_muscle(muscle)
                self.C_max_muscles[muscle.name] = self.get_C_max_muscle(muscle)

    def get_state(self):
        return [self.e_r, self.e_theta, self.origin, self.end, self.theta_dot, self.G, self.G_dot, self.P, self.F_max_muscles, self.C_max_muscles]

    def set_state(self, state):
        self.F_max_muscles, self.C_max_muscles = {}, {}
        self.e_r, self.e_theta, self.origin, self.end, self.theta_dot, self.G, self.G_dot, self.P, self.F_max_muscles, self.C_max_muscles = state

    def get_index(self):
        if self.previous_bone is None:
            return -1
        return self.previous_bone.index + 1

    def get_origin(self):
        if self.previous_bone is None:
            return [0, 0]
        return self.previous_bone.end

    def get_end(self):
        return self.origin + self.r * self.e_r

    def get_e_r_and_e_theta(self):  # coordinates of the eth vector
        s, c = np.sin(self.theta), np.cos(self.theta)
        return np.array([s, -c]), np.array([c, s])

    def get_G(self):  # coordinates of the gravity center
        return 0.5 * (self.origin + self.end)

    def get_P(self):  # change of basis matrix
        return np.array([self.e_r, self.e_theta]).T

    def get_theta_dot(self):
        return (self.l_theta[-1] - self.l_theta[-2]) / t

    def get_G_dot(self):  # velocity of the center of gravity
        return 0.5 * self.r * self.theta_dot * self.e_theta + \
               np.sum(np.array([bones[i].r * bones[i].theta_dot * bones[i].e_theta for i in range(self.index)]), axis=0)

    def get_F_max_muscle(self, muscle):  # maximum force exerted by a muscle on this bone
        u = muscle.tendon_position(muscle.other_bone(self)) - muscle.tendon_position(self)
        if (norm := N2(u)) != 0:
            u = u / norm  # normalize vector
        return muscle.max_force * u

    def F_tot(self, efforts):  # add up the forces exerted by the muscles on this bone
        F_tot_muscle = np.sum(np.array([efforts[muscle.index] * self.F_max_muscles[muscle.name] for muscle in self.muscles]), axis=0)
        F_gravity = np.array([0, - self.m * g])
        return F_tot_muscle + F_gravity

    def get_C_max_muscle(self, muscle):  # torque exerted by a muscle on this bone
        OM = muscle.tendon_position(self) - self.G
        F = self.F_max_muscles[muscle.name]
        return OM[0] * F[1] - OM[1] * F[0]

    def C_tot(self, efforts):  # add up the torque exerted by the muscles on this bone
        C_tot_muscle = sum(efforts[muscle.index] * self.C_max_muscles[muscle.name] for muscle in self.muscles)
        return C_tot_muscle


class Muscle:
    def __init__(self, name, index, relative_start, relative_end, max_force, color):

        self.name = name
        self.index = index
        self.bone0 = None
        self.bone1 = None
        self.relative_0 = relative_start
        self.relative_1 = relative_end
        self.max_force = max_force
        self.color = color

    def origin(self):
        return self.bone0.origin + np.dot(self.bone0.P, self.relative_0)

    def end(self):
        return self.bone1.origin + np.dot(self.bone1.P, self.relative_1)

    def other_bone(self, bone):
        return self.bone1 if bone == self.bone0 else self.bone0

    def tendon_position(self, bone):
        return bone.origin + np.dot(bone.P, self.relative_tendon_position(bone))

    def relative_tendon_position(self, bone):
        if bone == self.bone0:
            return self.relative_0
        else:
            return self.relative_1

    def origin_to_tendon_length(self, bone):
        return N2(self.relative_tendon_position(bone))


def assign_muscles_to_bones():
    for bone in [ground] + bones:
        for muscle in muscles:
            if muscle in bone.muscles:
                if muscle.bone0 is None:
                    muscle.bone0 = bone
                else:
                    muscle.bone1 = bone


def reset_bones():
    for bone in bones:
        bone.l_theta = bone.l_theta[0:3]
        bone.theta = bone.l_theta[-1]
        bone.set_state(bone.first_state)


def set_Ep0():  # so that for t = 0 Ep(t) = Ep(0) - Ep0 = 0
    for bone in bones:
        bone.Ep0 = bone.m * g * bone.G[1]


#


calves = Muscle('calves', 0, [-0.05, 0], [0.4, 0], 10000, muscle_color)
quadriceps = Muscle('quadriceps', 1, [0.55, 0], [0.35, 0], 10000, muscle_color)
hamstrings = Muscle('hamstrings', 2, [0.05, 0], [-0.05, 0], 10000, muscle_color)
low_back = Muscle('low back', 3, [0.45, 0], [0.44, 0], 10000, muscle_color)
lats = Muscle('lats', 4, [0.05, 0], [0.05, 0], 2000, muscle_color)


ground = Bone('ground', None, [calves], 0, np.pi / 2, 0, bone_color)
tibia = Bone('tibia', ground, [calves, quadriceps], 0.49, 2.758207465905639, 6, bone_color)
femur = Bone('femur', tibia, [quadriceps, hamstrings, low_back], 0.40, -1.8630010384296538, 14, bone_color)
back = Bone('back', femur, [hamstrings, low_back, lats], 0.49, 2.2435477244889137, 38, bone_color)
arm = Bone('arm', back, [lats], 0.65, -0.005690488236282301, 8 + bar_mass, bone_color)  # we condider the mass of the bar here


bones = [tibia, femur, back, arm]

muscles = [calves, quadriceps, hamstrings, low_back, lats]

assign_muscles_to_bones()

for bone in bones:
    bone.update()
    bone.first_state = deepcopy(bone.get_state())

set_Ep0()
