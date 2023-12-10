from gym import Env
from gym.spaces import Box
import random
from bone import Bone, Muscle
from constants import *
from utils import *
from system_solver import compute_next_state
from energy import total_kinetic_energy, total_potential_energy, p_muscle
from pygame_interface import update_display
import numpy as np


class Environment(Env):
    def __init__(self):
        super().__init__()

        self.render_mode = 'human'

        self.ground = Bone(0, 1, np.pi / 2, 0, bone_color)
        self.tibia = Bone(0, 0.49, 2.76, 6, bone_color)
        self.femur = Bone(1, 0.40, -2.15, 14, bone_color)
        self.back = Bone(2, 0.49, 2.14, 38, bone_color)
        self.arm = Bone(3, 0.65, -0.15, 8, bone_color)

        self.calves = Muscle(0, self.ground, self.tibia, [-0.05, 0], [0.4, 0], 5000, muscle_color)
        self.quadriceps = Muscle(1, self.tibia, self.femur, [0.55, 0], [0.35, 0], 5000, muscle_color)
        self.hamstrings = Muscle(2, self.femur, self.back, [0.1, 0], [-0.05, 0], 5000, muscle_color)
        self.lats = Muscle(3, self.back, self.arm, [0.1, 0], [0.1, 0], 5000, muscle_color)

        self.bones = [self.tibia, self.femur, self.back, self.arm]

        self.muscles = [self.calves, self.quadriceps, self.hamstrings, self.lats]

        self.assign_muscles()

        self.Ec, self.Ep = [], []
        self.l_p_muscle = [[] for _ in range(len(self.muscles))]

        self.state = self.get_state()
        self.observation_space = Box(low=np.float32(np.array(len(self.bones) * [[-np.inf, -np.inf, -np.inf]])),
                                     high=np.float32(np.array(len(self.bones) * [[np.inf, np.inf, np.inf]])))

        self.action_space = Box(low=np.float32(np.array(len(self.muscles) * [0])),
                                high=np.float32(np.array(len(self.muscles) * [1])))

        self.episode_length = 2000

        self.current_action = len(self.muscles) * [0]

    def step(self, action):

        x = compute_next_state(self.bones, action)

        for bone in self.bones:
            bone.theta = x[bone.index]
            bone.l_theta.append(bone.theta)

        self.update_energy()  # record the kinetic and potential energy of the system
        self.update_muscle_power(self.bones)  # record the power given to the bone by the muscle

        # G above the feets and above the ground
        if len(self.bones[0].l_theta) < self.episode_length and \
                0 < self.get_gravity_center()[0] < 0.26 and 0 < self.get_gravity_center()[1]:
            done = False
        else:
            done = True

        state = self.get_state()
        reward = self.compute_reward()
        info = {}

        self.current_action = action

        return state, reward, done, info

    def get_state(self):
        return np.array([[mod_angle(bone.theta), bone.theta_dot(), bone.theta_2dot()] for bone in self.bones])

    def compute_reward(self):
        return self.get_gravity_center()[1]

    def render(self, mode=None):
        update_display(self.bones, self.muscles, self.current_action, self.get_gravity_center())

    def reset(self):
        for bone in self.bones:
            bone.theta = bone.l_theta[0]
            bone.l_theta = 3 * [bone.theta]
        self.set_ep0()
        return self.get_state()

    def assign_muscles(self):
        for bone in self.bones:
            for muscle in self.muscles:
                if muscle.bone0 == bone or muscle.bone1 == bone:
                    bone.muscles.append(muscle)

    def get_gravity_center(self):  # compute the center of mass of the system
        return scalar_mul(1 / sum(bone.m for bone in self.bones),
                          v_list_sum([scalar_mul(bone.m, bone.G(self.bones)) for bone in self.bones]))

    def set_ep0(self):  # so that for t = 0 Ep(t) = Ep(0) - Ep0 = 0
        for bone in self.bones:
            bone.Ep0 = bone.m * g * bone.G(self.bones)[1]

    def update_energy(self):
        self.Ec.append(total_kinetic_energy(self.bones))
        self.Ep.append(total_potential_energy(self.bones))

    def update_muscle_power(self, bones):
        for i in range(len(self.muscles)):
            self.l_p_muscle[i].append(p_muscle(bones, self.muscles[i]))
