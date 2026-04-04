from typing import Tuple, List

import pygame as pg
from pygame.gfxdraw import filled_circle, aacircle

import state
from bone import Bone, Muscle
from config import *

if show_model:
    pg.font.init()
    my_font = pg.font.SysFont('Calibri', 50)
    screen = pg.display.set_mode((screen_size_x, screen_size_y))
    screen.fill(background_color)


def pos_to_screen(pos: np.ndarray) -> Tuple[int, int]:
    """
    Converts simulation coordinates to screen coordinates.
    """
    return (int((pos[0] - focus[0]) * pixel_per_meter * ratio_screen_reality) + screen_size_x // 2,
            int(-(pos[1] - focus[1]) * pixel_per_meter * ratio_screen_reality) + screen_size_y // 2)


def draw_line(p1: np.ndarray, p2: np.ndarray, color: Tuple[int, int, int]) -> None:
    """
    Draws an anti-aliased line on the screen.
    """
    pg.draw.aaline(screen, color, pos_to_screen(p1), pos_to_screen(p2))


def draw_bone(bone: Bone) -> None:
    """
    Draws a bone on the screen.
    """
    draw_line(bone.origin, bone.end, bone.color)


def draw_muscle(muscle: Muscle, effort: float) -> None:
    """
    Draws a muscle with color intensity based on effort.
    """
    draw_line(muscle.origin(), muscle.end(), color_gradient(effort))


def draw_head(bones: List[Bone]) -> None:
    """
    Draws the head of the character.
    """
    x, y = pos_to_screen(bones[2].end + r_head * bones[2].e_r)
    r = int(r_head * pixel_per_meter * ratio_screen_reality)
    aacircle(screen, x, y, r, bone_color)


def draw_vector(start: np.ndarray, v: np.ndarray, color: Tuple[int, int, int]) -> None:
    """
    Draws a vector arrow.
    """
    pg.draw.aaline(screen, color, pos_to_screen(start), pos_to_screen(start + v))


def draw_ground() -> None:
    """
    Draws the ground line.
    """
    y = pos_to_screen(np.array([0, 0]))[1]
    pg.draw.aaline(screen, ground_color, [0, y], [screen_size_x, y])


def draw_point(pos: np.ndarray) -> None:
    """
    Draws a small circle at a specific position.
    """
    x, y = pos_to_screen(pos)
    filled_circle(screen, x, y, 5, (100, 100, 255))


def draw_time(time: float) -> None:
    """
    Displays the simulation time on the screen.
    """
    text_surface = my_font.render(str(round(time, 2)) + 's', True, (220, 220, 220))
    screen.blit(text_surface, (40, screen_size_y - 54))


def draw_bar(bones: List[Bone]) -> None:
    """
    Draws the barbell.
    """
    x, y = pos_to_screen(bones[-1].end)
    r = int(r_bar * pixel_per_meter * ratio_screen_reality)
    filled_circle(screen, x, y, r, background_color)
    aacircle(screen, x, y, r, bone_color)


def color_gradient(x: float) -> Tuple[int, int, int]:
    """
    Returns a color tuple shading from white to red based on intensity x (0 to 1).
    """
    return int(139 + x * (255 - 139)), int(255 * x) if x >= 0 else 0, int(-255 * x) if x <= 0 else 0


def update_display(bones: List[Bone], muscles: List[Muscle], efforts: np.ndarray, time: float) -> bool:
    """
    Updates the PyGame display with the current state of the simulation.
    Returns False if the quit event is triggered, True otherwise.
    """
    screen.fill(background_color)
    if show_ground:
        draw_ground()

    for muscle in muscles:
        draw_muscle(muscle, efforts[muscle.index])

    if show_time:
        draw_time(time)

    for bone in bones:
        draw_bone(bone)
    draw_head(bones)

    if show_bar:
        draw_bar(bones)

    if show_gravity_center:
        draw_point(state.l_gravity_center[-1])

    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
    return True
