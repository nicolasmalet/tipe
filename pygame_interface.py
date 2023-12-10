import pygame as pg
from utils import v_sum, scalar_mul
from constants import *
from pygame.gfxdraw import filled_circle


if simulation:
    screen_size_x = 800
    screen_size_y = 900
    screen = pg.display.set_mode((screen_size_x, screen_size_y))

    screen.fill(background_color)


def pos_to_screen(pos):  # ! for pg the y_axis is oriented towards the bottom
    return (int((pos[0] - focus[0]) * pixel_per_meter * ratio_screen_reality) + screen_size_x // 2,
            int(-(pos[1] - focus[1]) * pixel_per_meter * ratio_screen_reality) + screen_size_y // 2)


def draw_line(p1, p2, color):
    pg.draw.aaline(screen, color, pos_to_screen(p1), pos_to_screen(p2))


def draw_bone(bones, bone):
    draw_line(bone.origin(bones), bone.end(bones), bone.color)


def draw_muscle(bones, muscle):
    draw_line(muscle.origin(bones), muscle.end(bones), muscle.color)


def draw_vector(start, v, color):
    pg.draw.aaline(screen, color, pos_to_screen(start), pos_to_screen(v_sum(start, v)))


def draw_force(bones, muscle, efforts):
    draw_vector(muscle.tendon_position(bones, muscle.bone0),
                scalar_mul(1 / 20000, muscle.bone0.F_muscle(bones, muscle, efforts[muscle.index])), 'yellow')
    draw_vector(muscle.tendon_position(bones, muscle.bone1),
                scalar_mul(1 / 20000, muscle.bone1.F_muscle(bones, muscle, efforts[muscle.index])), 'yellow')


def draw_tendon_speed(muscle):
    draw_vector(muscle.tendon_position(muscle.bone0), scalar_mul(1 / 10, muscle.bone0.v_tendon(muscle)), 'green')
    draw_vector(muscle.tendon_position(muscle.bone1), scalar_mul(1 / 10, muscle.bone1.v_tendon(muscle)), 'green')


def draw_ground():
    pg.draw.aaline(screen, ground_color, [0, pos_to_screen([0, 0])[1]], [screen_size_x, pos_to_screen([0, 0])[1]])


def draw_point(pos):
    x, y = pos_to_screen(pos)
    print(x, y)
    filled_circle(screen, x, y, 5, (100, 100, 255))


def update_display(bones, muscles, efforts, gravity_center):
    if simulation:
        screen.fill(background_color)
        if draw_ground:
            draw_ground()
        for bone in bones:
            draw_bone(bones, bone)
        for muscle in muscles:
            draw_muscle(bones, muscle)
        if draw_v_tendon:
            for muscle in muscles:
                draw_tendon_speed(muscle)
        if draw_forces:
            for muscle in muscles:
                draw_force(bones, muscle, efforts)
        draw_point(gravity_center)
        pg.display.update()
