import pygame as pg
from system_solver import gaussian_algorithm
from matrix import a, b
from pygame_interface import update_display
from plot import*
from constants import *
from environment import Enrironment


n = 1
efforts = [1]

env = Enrironment()
env.set_Ep0()


if learning:
    pass


if plotting:  # simulation + graphs
    for i in range(N):
        env.step([1])
        env.render()
    pg.quit()
    if plot_e:
        plot_energies(env.bones, env.Ec, env.Ep, env.l_P_muscle)
    if plot_m:
        plot_movement(env.bones, env.Ec, env.Ep)
    if plot_p:
        plot_phase_portrait(env.bones)


else:  # pygame simulation alone
    while running:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                efforts = [1, 1, 1]
            if event.type == pg.KEYUP:
                efforts = [0, 0, 0]
            if event == pg.QUIT:
                pg.quit()
        update()
        update_display()


