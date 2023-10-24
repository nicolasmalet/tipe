from numpy import sin, cos, pi
from utils import v_sum, scalar_mul, v_list_sum
from constants import g, t


bone_color = (200, 200, 200)


class Bone:
    def __init__(self, index, length, angle, mass, color):
        self.index = index
        self.length = length
        self.mass = mass
        self.angle = angle
        self.angles = [angle, angle, angle]
        self.color = color
        self.moment_of_inertia = 1 / 12 * mass * length ** 2  # around the center of gravity
        self.Ep0 = 0  # set it later

    def start(self):
        if self.index == 0:
            return [0, 0]
        else:
            return bones[self.index - 1].end()

    def end(self):
        return v_sum(self.start(), [self.length * sin(self.angle), - self.length * cos(self.angle)])

    def gravity_center(self):
        return scalar_mul(0.5, v_sum(self.start(), self.end()))

    def angular_velocity(self):
        return (self.angles[-1] - self.angles[-2]) / t

    def angular_acceleration(self):
        return (self.angles[-1] - 2*self.angles[-2] + self.angles[-3]) / t ** 2

    def absolute_velocity(self):  # velocity of the center of gravity
        return v_sum([0.5 * self.length * sin(self.angle) * self.angular_velocity(),
                      0.5 * self.length * cos(self.angle) * self.angular_velocity()],
                     v_list_sum([[bones[i].length * sin(bones[i].angle) * bones[i].angular_velocity(),
                                  bones[i].length * cos(bones[i].angle) * bones[i].angular_velocity()]
                                 for i in range(self.index)]))


def set_Ep0():  # so that for t = 0 Ep(t) = Ep(0) - Ep0 = 0
    for bone in bones:
        bone.Ep0 = bone.mass * g * bone.gravity_center()[1]


bone0 = Bone(0, 1, pi / 2, 10, bone_color)
bone1 = Bone(1, 1, pi / 2, 10, bone_color)
bone2 = Bone(2, 1, pi / 2, 10, bone_color)

bones = [bone0, bone1, bone2]

set_Ep0()
