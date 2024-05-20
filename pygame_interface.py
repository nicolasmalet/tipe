import pygame as pg
from utils import v_sum, scalar_mul
from constants import *
from pygame.gfxdraw import filled_circle
from bone import l_gravity_center


if show_model:

    pg.font.init()
    my_font = pg.font.SysFont('Calibri', 50)

    screen = pg.display.set_mode((screen_size_x, screen_size_y))

    screen.fill(background_color)


def pos_to_screen(pos):  # ! for pg the y_axis is oriented towards the bottom
    return (int((pos[0] - focus[0]) * pixel_per_meter * ratio_screen_reality) + screen_size_x // 2,
            int(-(pos[1] - focus[1]) * pixel_per_meter * ratio_screen_reality) + screen_size_y // 2)


def draw_line(p1, p2, color):
    pg.draw.aaline(screen, color, pos_to_screen(p1), pos_to_screen(p2))


def draw_bone(bone):
    draw_line(bone.origin, bone.end, bone.color)


def draw_muscle(muscle, effort):
    draw_line(muscle.origin(), muscle.end(), color_gradient(effort))


def draw_head(bones):
    x, y = pos_to_screen(v_sum(bones[2].end, scalar_mul(r_head, bones[2].e_r)))
    r = int(r_head * pixel_per_meter * ratio_screen_reality)
    pg.gfxdraw.aacircle(screen, x, y, r, bone_color)


def draw_vector(start, v, color):
    pg.draw.aaline(screen, color, pos_to_screen(start), pos_to_screen(v_sum(start, v)))


def draw_tendon_speed(muscle):
    draw_vector(muscle.tendon_position(muscle.bone0), scalar_mul(1 / 10, muscle.bone0.v_tendon(muscle)), 'green')
    draw_vector(muscle.tendon_position(muscle.bone1), scalar_mul(1 / 10, muscle.bone1.v_tendon(muscle)), 'green')


def draw_ground():
    pg.draw.aaline(screen, ground_color, [0, pos_to_screen([0, 0])[1]], [screen_size_x, pos_to_screen([0, 0])[1]])


def draw_point(pos):
    x, y = pos_to_screen(pos)
    filled_circle(screen, x, y, 5, (100, 100, 255))


def draw_time(time):
    text_surface = my_font.render(str(round(time, 2)) + 's', True, (220, 220, 220))
    screen.blit(text_surface, (40, screen_size_y - 54))


def draw_bar(bones):
    x, y = pos_to_screen(bones[-1].end)
    r = int(r_bar * pixel_per_meter * ratio_screen_reality)
    pg.gfxdraw.filled_circle(screen, x, y, r, background_color)
    pg.gfxdraw.aacircle(screen, x, y, r, bone_color)


def color_gradient(x):
    return 139 + x * (255 - 139), 255 * x if x >= 0 else 0, -255 * x if x <= 0 else 0


def update_display(bones, muscles, efforts, time):
    screen.fill(background_color)
    if show_ground:
        draw_ground()

    for muscle in muscles:
        draw_muscle(muscle, efforts[muscle.index])

    if show_v_tendon:
        for muscle in muscles:
            draw_tendon_speed(muscle)
    if show_time:
        draw_time(time)

    for bone in bones:
        draw_bone(bone)
    draw_head(bones)

    if show_bar:
        draw_bar(bones)

    if show_gravity_center:
        draw_point(l_gravity_center[-1])

    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
    return True
