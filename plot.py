from energy import total_kinetic_energy, total_potential_energy, P_muscle
import matplotlib.pyplot as plt
from constants import *
from utils import l_sum, generalized_l_sum, differentiate, integrate
from environment import Enrironment

plt.style.use('dark_background')


def plot_movement(bones, Ec, Ep):  # plot each graph

    fig, axs = plt.subplots(2, 2)
    t_axis = [i * t for i in range(N)]

    for i in range(len(bones)):
        axs[0, 0].plot(t_axis, bones[i].l_theta[2:N+2], label='theta' + str(i))
        axs[0, 1].plot(t_axis, differentiate(bones[i].l_theta[1:N+2]), label='theta' + str(i) + '_dot')
        axs[1, 0].plot(t_axis[1:N],
                       differentiate(differentiate(bones[i].l_theta)[2:N+2]), label='theta' + str(i) + '_dotdot')

    axs[1, 1].plot(t_axis, Ec, label='Ec', color='magenta')
    axs[1, 1].plot(t_axis, Ep, label='Ep', color='cyan')
    axs[1, 1].plot(t_axis, l_sum(Ec, Ep), label='E', color='white')

    axs[0, 0].set_title('Angle')
    axs[0, 1].set_title('Angular velocity')
    axs[1, 0].set_title('Angular acceleration')
    axs[1, 1].set_title('Energy')

    axs[0, 0].set_xlabel('time (s)')
    axs[0, 1].set_xlabel('time (s)')
    axs[1, 0].set_xlabel('time (s)')
    axs[1, 1].set_xlabel('time (s)')

    axs[0, 0].set_ylabel('angle (rad)')
    axs[0, 1].set_ylabel('angular velocity (rad/s)')
    axs[1, 0].set_ylabel('angular acceleration (rad/s2)')
    axs[1, 1].set_ylabel('Energy (J)')

    for ax in fig.get_axes():
        ax.legend()

    plt.show()


def plot_energies(bones, Ec, Ep, l_P_muscle):
    fig, axs = plt.subplots(2, 2)
    t_axis = [i * t for i in range(N)]

    axs[0, 0].plot(t_axis, Ec, label='Ec', color='magenta')
    axs[0, 0].plot(t_axis, Ep, label='Ep', color='cyan')
    axs[0, 0].plot(t_axis, l_sum(Ec, Ep), label='E', color='white')

    for i in range(len(l_P_muscle)):
        axs[0, 1].plot(t_axis, integrate(l_P_muscle[i])[0:N], label='E_muscle_' + str(i))

    axs[1, 0].plot(t_axis, l_sum(Ec, Ep), label='E', color='white')
    axs[1, 0].plot(t_axis, integrate(generalized_l_sum(l_P_muscle))[0:N], label='E_tot_muscle', color='magenta')

    axs[1, 1].plot(t_axis[0:N-1], differentiate((l_sum(Ec, Ep))), label='P_system', color='white')
    axs[1, 1].plot(t_axis, generalized_l_sum(l_P_muscle), label='P_tot_muscle', color='magenta')

    axs[0, 0].set_title('system energy')
    axs[0, 1].set_title('muscle energy')
    axs[1, 0].set_title('mechanical energy and total muscle energy')
    axs[1, 1].set_title('accuracy')

    axs[0, 0].set_xlabel('time (s)')
    axs[0, 1].set_xlabel('time (s)')
    axs[1, 0].set_xlabel('time (s)')
    axs[1, 1].set_xlabel('time (s)')

    axs[0, 0].set_ylabel('Energy (J)')
    axs[0, 1].set_ylabel('Energy (J)')
    axs[1, 0].set_ylabel('Energy (J)')
    axs[1, 1].set_ylabel('Energy (J)')

    for ax in fig.get_axes():
        ax.legend()

    plt.show()


def plot_phase_portrait(bones):
    for bone in bones:
        plt.plot(bone.l_theta[0:N], differentiate(bone.l_theta[1:N+2]))
    plt.show()
