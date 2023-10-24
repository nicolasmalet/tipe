import pygame as pg
from utils import v_sum


simulation = False  # show the pendulum


if simulation:
    screen_size_x = 1300
    screen_size_y = 900
    screen = pg.display.set_mode((screen_size_x, screen_size_y))

    background_color = (20, 20, 20)
    screen.fill(background_color)

    focus = [0, -1]
    pixel_per_meter = 3176  # the ratio of my screen
    ratio_screen_reality = 1/15


def pos_to_screen(pos):  # ! for pg the y_axis is oriented towards the bottom
    return (int((pos[0] - focus[0]) * pixel_per_meter * ratio_screen_reality) + screen_size_x // 2 ,
            int(- (pos[1] - focus[1]) * pixel_per_meter * ratio_screen_reality) + screen_size_y // 2 - focus[1])


def draw_bone(bone):
    pg.draw.aaline(screen, bone.color, pos_to_screen(bone.start()), pos_to_screen(bone.end()))


def draw_vector(start, v):
    pg.draw.aaline(screen, 'red', pos_to_screen(start), pos_to_screen(v_sum(start, v)))


def update_display(bones):
    if simulation:
        screen.fill(background_color)
        for bone in bones:
            draw_bone(bone)
        pg.display.update()
