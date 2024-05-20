import matplotlib.pyplot as plt
from constants import *
from utils import l_sum, generalized_l_sum, differentiate, integrate
from energy import total_kinetic_energy, total_potential_energy, p_muscle
from bone import bones, muscles

plt.style.use('dark_background')

l_Q = [[0, 0, 0, 0, 13.51, 0]]

Ec, Ep = [0], [total_potential_energy(bones)]
l_p_muscle = [[0] for _ in range(len(muscles))]

efforts = [1, 0.14, 0.62, 0.63, 0.45]
l_efforts = [efforts]


def reset_energy():
    global Ec, Ep, l_p_muscle
    Ec, Ep = [0], [total_potential_energy(bones)]
    l_p_muscle = [[0] for _ in range(len(muscles))]


def update_energy(_bones):
    Ec.append(total_kinetic_energy(_bones))
    Ep.append(total_potential_energy(_bones))


def update_muscle_power(_efforts):
    for i in range(len(muscles)):
        l_p_muscle[i].append(p_muscle(muscles[i], _efforts[i]))


def reverse_energy_changes():
    Ec.pop()
    Ep.pop()
    for i in range(len(l_p_muscle)):
        l_p_muscle[i].pop()


def plot_movement():  # plot each graph

    n = len(bones[0].l_theta) - 2

    fig, axs = plt.subplots(2, 2)
    t_axis = [i * t for i in range(n)]

    for i in range(len(bones)):
        axs[0, 0].plot(t_axis, bones[i].l_theta[2:], label='theta' + str(i), linewidth=3)
        axs[0, 1].plot(t_axis, differentiate(bones[i].l_theta[1:]), label='theta' + str(i) + '_dot', linewidth=3)
        axs[1, 0].plot(t_axis[:-1],
                       differentiate(differentiate(bones[i].l_theta[1:])), label='theta' + str(i) + '_dotdot',
                       linewidth=3)

    axs[1, 1].plot(t_axis, Ec, label='Ec', color='magenta', linewidth=3)
    axs[1, 1].plot(t_axis, Ep, label='Ep', color='cyan', linewidth=3)
    axs[1, 1].plot(t_axis, l_sum(Ec, Ep), label='E', color='white', linewidth=3)

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


def plot_energies():
    n = len(bones[0].l_theta) - 2

    fig, axs = plt.subplots(2, 2)
    t_axis = [i * t for i in range(n)]

    axs[0, 0].plot(t_axis, Ec, label='Ec', color='magenta', linewidth=3)
    axs[0, 0].plot(t_axis, Ep, label='Ep', color='cyan', linewidth=3)
    axs[0, 0].plot(t_axis, l_sum(Ec, Ep), label='E', color='white', linewidth=3)

    for i in range(len(l_p_muscle)):
        axs[0, 1].plot(t_axis, integrate(l_p_muscle[i])[1:n + 1], label=muscles[i].name, linewidth=3)

    axs[1, 0].plot(t_axis, l_sum(Ec, Ep), label='E', color='white', linewidth=3)
    axs[1, 0].plot(t_axis, integrate(generalized_l_sum(l_p_muscle))[1:n + 1],
                   label='E tot muscle', color='magenta', linewidth=3)

    axs[1, 1].plot(t_axis[1:-1], differentiate((l_sum(Ec[1:], Ep[1:]))), label='P system', color='white', linewidth=3)
    axs[1, 1].plot(t_axis, generalized_l_sum(l_p_muscle), label='P tot muscle', color='magenta', linewidth=3)

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
    axs[1, 1].set_ylabel('Power (W)')

    for ax in fig.get_axes():
        ax.legend()

    plt.show()


def plot_phase_portrait():
    n = len(bones[0].l_theta) - 2

    for bone in bones:
        plt.plot(bone.l_theta[1:n], differentiate(bone.l_theta[2:n + 2]), linewidth=3)
    plt.show()


def plot_efforts():
    fig, axs = plt.subplots(2, 3)

    n = len(bones[0].l_theta) - 2

    t_axis = [i * t for i in range(0, n)]

    calves, quadriceps, hamstrings, low_back, lats_and_delt = muscles
    axs[0, 0].plot(t_axis[1:], [l_efforts[i][low_back.index] for i in range(1, len(l_efforts))], label=low_back.name,
                   color='#8dd3c7', linewidth=3)
    axs[0, 1].plot(t_axis[1:], [l_efforts[i][quadriceps.index] for i in range(1, len(l_efforts))],
                   label=quadriceps.name, color='#feffb3', linewidth=3, )
    axs[0, 2].plot(t_axis[1:], [l_efforts[i][lats_and_delt.index] for i in range(1, len(l_efforts))],
                   label=lats_and_delt.name, color='#bfbbd9', linewidth=3)
    axs[1, 0].plot(t_axis[1:], [l_efforts[i][hamstrings.index] for i in range(1, len(l_efforts))],
                   label=hamstrings.name, color='#fa8174', linewidth=3)
    axs[1, 1].plot(t_axis[1:], [l_efforts[i][calves.index] for i in range(1, len(l_efforts))], label=calves.name,
                   color='#81b1d2', linewidth=3)

    name = {0: 'Q', 1: ' - potential energy', 2: 'gravity center pos', 3: 'gravity center speed',
            4: 'g', 5: 'dg/dt'}  # where g is defined in brain.py

    for j in range(len(l_Q[0])):
        axs[1, 2].plot(t_axis[1:], [l_Q[i][j] for i in range(1, len(l_Q))], label=name[j], linewidth=3)

    axs[0, 0].set_xlabel('time (s)')
    axs[0, 1].set_xlabel('time (s)')
    axs[0, 2].set_xlabel('time (s)')
    axs[1, 0].set_xlabel('time (s)')
    axs[1, 1].set_xlabel('time (s)')
    axs[1, 2].set_xlabel('time (s)')

    axs[0, 0].set_ylabel('normalized force')
    axs[0, 1].set_ylabel('normalized force')
    axs[0, 1].set_ylabel('normalized force')
    axs[1, 0].set_ylabel('normalized force')
    axs[1, 1].set_ylabel('normalized force')
    axs[1, 2].set_ylabel('score')

    for ax in fig.get_axes():
        ax.legend()

    plt.show()


def plot_Q():

    fig, ax = plt.subplots(1, 1)

    n = len(bones[0].l_theta) - 2

    t_axis = [i * t for i in range(0, n)]

    name = {0: 'Q', 1: ' - potential energy', 2: 'gravity center pos', 3: 'gravity center speed',
            4: 'g', 5: 'dg/dt'}  # where g is defined in brain.py

    for j in range(len(l_Q[0])):
        ax.plot(t_axis[1:], [l_Q[i][j] for i in range(1, len(l_Q))], label=name[j], linewidth=3)

    ax.legend()
    plt.show()
