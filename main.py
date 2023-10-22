import pygame as pg
from numpy import pi, sin, cos, arctan, sign
import matplotlib.pyplot as plt

screen_size_x = 1700
screen_size_y = 800
screen = pg.display.set_mode((screen_size_x, screen_size_y))
running = True


pixel_per_meter = 3176
ratio_screen_reality = 1

g = 9.81

T = 0
t = 9*10**(-4)

plotting = True

def v_sum(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]

def v_list_sum(l):
    return sum(l[i][0] for i in range(len(l))), sum(l[i][1] for i in range(len(l)))


def scalar_mul(x, v):
    return x*v[0], x*v[1]


def change_of_basis(p, x):
    return p[0][0]*x[0]+p[0][1]*x[1], p[1][0]*x[0]+p[1][1]*x[1]


class Bone:
    def __init__(self, start, length, angle, mass, color):
        self.start = start
        self.length = length
        self.pixel_length = length * pixel_per_meter
        self.mass = mass
        self.angle = angle
        self.angles = [angle, angle, angle]
        self.color = color
        self.J = 1/3*mass*length**2

    def matrix_relative_to_absolute(self):
        return [[sin(self.angle), cos(self.angle)], [cos(self.angle), -sin(self.angle)]]

    def end(self):
        return v_sum(self.start, [self.length*sin(self.angle), self.length*cos(self.angle)])

    def gravity_center(self):
        return scalar_mul(0.5, v_sum(self.start, self.end()))


class Force:
    def __init__(self, bone, start, matrix):
        self.str_start = start
        self.bone = bone
        self.matrix = matrix

    def start(self):
        if self.str_start == 'bone.start':
            return self.bone.start
        if self.str_start == 'bone.end':
            return self.bone.end()
        if self.str_start == 'center of gravity':
            return self.bone.gravity_center()


bone1 = Bone([0, -0.10], 0.20, pi/100, 1, (0, 0, 0))
#bone2 = Bone([0, 0], 0.10, pi/4, 1, (0, 0, 0))

bones = [bone1]#, bone2]

weight = [Force(bone, 'center of gravity', [0, -bone.mass*g]) for bone in bones]


# unknown_forces = [Force(bones[i].end) for i in range(0, len(bones))]


def v_sub(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]


def norm(v):
    return (v[0] ** 2 + v[1] ** 2) ** 0.5


def angle(v):
    if v[0] > 0:
        return arctan(v[1] / v[0])
    if v[0] < 0 and v[1] >= 0:
        return arctan(v[1] / v[0]) + pi
    if v[0] < 0 and v[1] < 0:
        return arctan(v[1] / v[0]) - pi
    return sign(v[1]) * pi / 2


def moment(origin, force: Force) -> float:
    v = v_sub(force.start(), origin)
    return v[0] * force.matrix[1] - v[1] * force.matrix[0]


def angular_velocity(bone):
    return (bone.angles[-1] - bone.angles[-2])/t


def angular_acceleration(bone):
    return (bone.angles[-1] - 2*bone.angles[-2] + bone.angles[-3])/(t**2)


def relative_acceleration(bone):
    return [bone.length*angular_acceleration(bone), bone.length*angular_velocity(bone)**2]


def relative_kinetic_energy(bone):
    return


def acceleration(bone):
    n = bones.index(bone)
    return v_list_sum(
        [change_of_basis(bones[i].matrix_relative_to_absolute(), relative_acceleration(bones[i])) for i in range(n)])


def TMC(origin, bone, force):
    next_angle = moment(origin, force)/bone.J*t**2 + 2*bone.angles[-1] - bone.angles[-2]
    bone.angle = next_angle
    bone.angles.append(next_angle)


def pos_to_screen(pos):
    return (int(pos[0]*pixel_per_meter*ratio_screen_reality) + screen_size_x // 2,
            int(pos[1]*pixel_per_meter*ratio_screen_reality) + screen_size_y // 2)


def draw_bone(bone):
    pg.draw.aaline(screen, bone.color, pos_to_screen(bone.start), pos_to_screen(bone.end()))


def update():
    TMC(bone1.start, bone1, weight[0])
    #print(bone1.angle, pi/100*cos((g/bone1.length)**0.5*T))


def update_display():
    screen.fill('white')
    for bone in bones:
        draw_bone(bone)
    pg.display.update()


if not plotting:
    while running:
        for event in pg.event.get():
            if event == pg.QUIT:
                pg.quit()

        update()
        T += t
        update_display()

else:
    N = int(3 / t)
    velocity = []
    for i in range(N):
        update()
        # velocity.append(acceleration(bone2))
        update_display()
    pg.quit()
    plt.plot([i*t for i in range(N)], bone1.angles[0:N], color='blue')
    #plt.plot([i * t for i in range(N)], velocity, color='red')
    plt.show()

