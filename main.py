import pygame as pg
from system_solver import gaussian_algorithm
from matrix import a_ij, b_i
from pygame_interface import update_display
from bone import bones, muscles
from plot import update_energy, update_muscle_power, plot_movement, plot_energies, plot_phase_portrait
from constants import *


n = len(bones)
efforts = [1] * len(bones) * 2


def update():

    # set the motion and reaction forces system
    A = [[a_ij(i, j, n, bones) for j in range(3 * n)] for i in range(3 * n)]
    B = [b_i(i, n, bones, efforts) for i in range(3 * n)]

    # solve the system
    X = gaussian_algorithm(A, B)

    update_bones(X)  # set the next thetas
    update_energy(bones)  # record the kinetic and potential energy of the system
    update_muscle_power(bones, muscles)  # record the power given to the bone by the muscle


def update_bones(X):
    for bone in bones:
        bone.theta = X[bone.index]
        bone.l_theta.append(bone.theta)


if not plotting:  # pygame simulation alone
    while running:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                efforts = [1, 1, 1]
            if event.type == pg.KEYUP:
                efforts = [0, 0, 0]
            if event == pg.QUIT:
                pg.quit()
        update()
        update_display(bones, muscles, efforts)


else:  # simulation + graphs
    for i in range(N):
        update()
        update_display(bones, muscles, efforts)
    pg.quit()
    if plot_e:
        plot_energies()
    if plot_m:
        plot_movement(bones)
    if plot_p:
        plot_phase_portrait(bones)
