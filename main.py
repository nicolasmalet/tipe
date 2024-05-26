import pygame as pg
from pygame_interface import update_display
from bone import bones, muscles, reset_bones
from plot import plot_movement, plot_energies, plot_phase_portrait, plot_efforts, plot_Q
from constants import *
from update import update_model, reset_energy
from brain import make_decision, l_efforts


i = 0
global efforts

while True:
    efforts = make_decision()
    update_model(efforts)
    if show_model:
        run = update_display(bones, muscles, efforts, i * t)
        if not run:
            break

    i += 1


if review:
    reset_bones()
    reset_energy()
    for i in range(1, len(l_efforts)):
        efforts = l_efforts[i]
        update_model(efforts)
        update_display(bones, muscles, efforts, i*t)

pg.quit()

if plot_m:
    plot_movement()
if plot_e:
    plot_energies()
if plot_p:
    plot_phase_portrait()
if plot_eff:
    plot_efforts()
if plot_Q_function:
    plot_Q()
