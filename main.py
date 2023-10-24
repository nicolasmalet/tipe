import pygame as pg
import matplotlib.pyplot as plt
from system_solver import gaussian_algorithm
from matrix import a, b
from pygame_interface import update_display
from bone import bones
from plot import update_velocity, update_acceleration, update_energy, plot_all
from constants import N


fig, axs = plt.subplots(2, 2)


running = True
plotting = True


n = len(bones)


def update():

    # set the motion and reaction forces system
    A = [[a(i, j, n, bones) for j in range(3 * n)] for i in range(3 * n)]
    B = [b(i, n, bones) for i in range(3 * n)]

    # solve the system
    X = gaussian_algorithm(A, B)

    update_bones(X)  # set the next angles
    update_energy()  # record the kinetic and potential energy of the system
    update_velocity()  # record the angular velocity of each bone
    update_acceleration()  # record the acceleration of each bone


def update_bones(x):
    for bone in bones:
        bone.angle = x[bone.index]
        bone.angles.append(bone.angle)


if not plotting:  # pygame simulation alone
    while running:
        for event in pg.event.get():
            if event == pg.QUIT:
                pg.quit()
        update()
        update_display(bones)

else:  # simulation + graphs
    for i in range(N):
        update()
        update_display(bones)
    pg.quit()
    plot_all()

