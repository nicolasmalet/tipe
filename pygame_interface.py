import pygame as pg
from utils import v_sum, scalar_mul
from bone import bones, muscles
from constants import *


if simulation:
    screen_size_x = 1300
    screen_size_y = 900
    screen = pg.display.set_mode((screen_size_x, screen_size_y))

    background_color = (20, 20, 20)
    screen.fill(background_color)

    focus = [0, -1]
    pixel_per_meter = 3176  # the ratio of my screen
    ratio_screen_reality = 1/10


def pos_to_screen(pos):  # ! for pg the y_axis is oriented towards the bottom
    return (int((pos[0] - focus[0]) * pixel_per_meter * ratio_screen_reality) + screen_size_x // 2,
            int(- (pos[1] - focus[1]) * pixel_per_meter * ratio_screen_reality) + screen_size_y // 2 - focus[1])


def draw_line(p1, p2, color):
    pg.draw.aaline(screen, color, pos_to_screen(p1), pos_to_screen(p2))


def draw_bone(bone):
    draw_line(bone.origin(), bone.end(), bone.color)


def draw_muscle(muscle):
    draw_line(muscle.origin(), muscle.end(), muscle.color)


def draw_vector(start, v, color):
    pg.draw.aaline(screen, color, pos_to_screen(start), pos_to_screen(v_sum(start, v)))


def draw_force(muscle):
    draw_vector(muscle.bone0.tendon_position(muscle), scalar_mul(1 / 200, muscle.bone0.F_muscle(muscle, 1)), 'blue')
    draw_vector(muscle.bone1.tendon_position(muscle), scalar_mul(1 / 200, muscle.bone1.F_muscle(muscle, 1)), 'blue')


def draw_tendon_speed(muscle):
    draw_vector(muscle.tendon_position(muscle.bone0), scalar_mul(1 / 10, muscle.bone0.v_tendon(muscle)), 'green')
    draw_vector(muscle.tendon_position(muscle.bone1), scalar_mul(1 / 10, muscle.bone1.v_tendon(muscle)), 'green')


def update_display():
    if simulation:
        screen.fill(background_color)
        for bone in bones:
            draw_bone(bone)
        for muscle in muscles:
            draw_muscle(muscle)
        if draw_v_tendon:
            for muscle in muscles:
                draw_tendon_speed(muscle)
        if draw_forces:
            for muscle in muscles:
                draw_force(muscle)
        pg.display.update()
