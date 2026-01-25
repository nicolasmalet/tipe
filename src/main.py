from plot import plot_movement, plot_energies, plot_phase_portrait, plot_efforts, plot_Q
from update import update_model, reset_energy
from pygame_interface import update_display
from brain import make_decision
from state import reset_bones
from config import *

import pygame as pg
import state


i = 0

while True:
    state.efforts = make_decision()
    update_model(state.efforts)
    if show_model:
        run = update_display(state.bones, state.muscles, state.efforts, i * t)
        if not run:
            break

    i += 1


if review:
    reset_bones()
    reset_energy()
    for i in range(1, len(state.l_efforts)):
        state.efforts = state.l_efforts[i]
        update_model(state.efforts)
        update_display(state.bones, state.muscles, state.efforts, i * t)

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
