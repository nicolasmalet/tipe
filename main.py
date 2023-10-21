import pygame as pg
import numpy as np

screen_size_x = 1000
screen_size_y = 500
screen = pg.display.set_mode((screen_size_x, screen_size_y))
running = True


class Bone:
    def __init__(self, start, end, length, angle, mass, width, color,):
        self.start = start
        self.end = end
        self.length = length
        self.mass = mass
        self.angle = angle
        self.color = color
        self.width = width


class Force:
    def __init__(self, start, coord):
        self.start = start
        self.coord = coord


bone1 = Bone([0, 0], [100, 0], 100, 1, 0, 5, 'black')
bone2 = Bone([100, 0], [200, 0], 100, 1, 0, 5, 'black')

bones = [bone1, bone2]

unknown_forces = [Force(bones[i].end) for i in range(0, len(bones))]


def sub(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]


def v_sum(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def slide(bone, v):
    bone.start = v_sum(bone.start, v)
    bone.end = v_sum(bone.end, v)


def rotate(bone, angle):
    bone.angle += angle
    bone.end = [bone.start[0] + bone.length * np.cos(bone.angle), bone.start[1] + bone.length * np.sin(bone.angle)]


def pos_to_screen(pos):
    return pos[0] + screen_size_x//2, pos[1] + screen_size_y//2


def draw_bone(bone):
    pg.draw.line(screen, bone.color, pos_to_screen(bone.start), pos_to_screen(bone.end), bone.width)


def update():
    rotate(bone2, 0.001)


def update_display():
    screen.fill('white')
    for bone in bones:
        draw_bone(bone)
    pg.display.update()


while running:
    for event in pg.event.get():
        if event == pg.QUIT:
            pg.quit()
    update()
    update_display()
