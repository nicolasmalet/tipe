from gym import Env
from gym.spaces import Box
import numpy as np
import random
from bone import Bone, Muscle
from constants import*
from system_solver import compute_next_state
from energy import total_kinetic_energy, total_potential_energy, P_muscle
from pygame_interface import update_display


class Enrironment(Env):
    def __init__(self):

        self.bone0 = Bone(0, 1, np.pi*random.random() - np.pi/2, 10, bone_color)
        self.ground = Bone(0, 1, np.pi/2, 0, bone_color)
        self.muscle0 = Muscle(self.ground, self.bone0, [0.5, 0], [0.5, 0], 200, muscle_color)

        self.bones = [self.bone0]
        self.muscles = [self.muscle0]

        self.assign_muscles()

        self.Ec, self.Ep = [], []
        self.l_P_muscle = [[] for i in range(len(self.muscles))]

        self.state = self.get_state()

        self.observation_space = Box(low=np.array([-10., -10., -100.]), high=np.array([10., 10., 100.]))
        self.action_space = Box(low=np.array([0.]), high=np.array([1.]))

        self.episode_length = 10000

        #self.initial

    def step(self, efforts):

        X = compute_next_state(self.bones, efforts)
        for bone in self.bones:
            bone.theta = X[bone.index]
            bone.l_theta.append(bone.theta)

        self.update_energy()  # record the kinetic and potential energy of the system
        self.update_muscle_power(self.bones)  # record the power given to the bone by the muscle

        if len(self.bones[0].l_theta) > self.episode_length:
            done = True
        else:
            done = False

        state = self.get_state()
        reward = self.compute_reward()
        info = {}

        return state, reward, done, info

    def get_state(self):
        return [[bone.theta, bone.theta_dot(), bone.theta_2dot()] for bone in self.bones]

    def compute_reward(self):
        return -total_kinetic_energy(self.bones)

    def render(self):
        update_display(self.bones, self.muscles)

    def reset(self):
        for bone in self.bones:
            bone.theta = np.pi*random.random() - np.pi/2
            bone.l_theta = 3*[bone.theta]
        self.set_Ep0()
        return self.get_state()

    def assign_muscles(self):
        for bone in self.bones:
            for muscle in self.muscles:
                if muscle.bone0 == bone or muscle.bone1 == bone:
                    bone.muscles.append(muscle)

    def set_Ep0(self):  # so that for t = 0 Ep(t) = Ep(0) - Ep0 = 0
        for bone in self.bones:
            bone.Ep0 = bone.m * g * bone.G(self.bones)[1]

    def update_energy(self):
        self.Ec.append(total_kinetic_energy(self.bones))
        self.Ep.append(total_potential_energy(self.bones))

    def update_muscle_power(self, bones):
        for i in range(len(self.muscles)):
            self.l_P_muscle[i].append(P_muscle(bones, self.muscles[i]))
