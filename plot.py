import matplotlib.pyplot as plt
from update import *
from utils import *

plt.style.use('dark_background')


def plot_movement():  # plot each graph

    N = len(bones[0].l_theta) - 2

    fig, axs = plt.subplots(2, 2)
    t_axis = [i * t for i in range(N)]

    for i in range(len(bones)):
        axs[0, 0].plot(t_axis, bones[i].l_theta[2:], label='theta' + str(i), linewidth=1)
        axs[0, 1].plot(t_axis, differentiate(bones[i].l_theta[1:]), label='theta' + str(i) + '_dot', linewidth=1)
        axs[1, 0].plot(t_axis[:-1],
                       differentiate(differentiate(bones[i].l_theta[1:])), label='theta' + str(i) + '_dotdot',
                       linewidth=1)

    axs[1, 1].plot(t_axis, Ec, label='Ec', color='magenta', linewidth=1)
    axs[1, 1].plot(t_axis, Ep, label='Ep', color='cyan', linewidth=1)
    axs[1, 1].plot(t_axis, np.sum(np.array([Ec, Ep]), axis=0), label='Em', color='white', linewidth=1)

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

    fig.patch.set_facecolor(background_color / 255)

    for ax in fig.get_axes():
        ax.legend()
        ax.set_facecolor(background_color / 255)

    plt.show()


def plot_energies():
    N = len(bones[0].l_theta) - 2

    fig, axs = plt.subplots(2, 2)
    t_axis = [i * t for i in range(N)]

    axs[0, 0].plot(t_axis, Ec, label='Ec', color='magenta', linewidth=1)
    axs[0, 0].plot(t_axis, Ep, label='Ep', color='cyan', linewidth=1)
    axs[0, 0].plot(t_axis, np.sum(np.array([Ec, Ep]), axis=0), label='Em', color='white', linewidth=1)

    for i in range(len(l_p_muscle)):
        axs[0, 1].plot(t_axis, integrate(l_p_muscle[i])[1: N + 1], label=muscles[i].name, linewidth=1)

    axs[1, 0].plot(t_axis, np.sum(np.array([Ec, Ep]), axis=0), label='Em', color='white', linewidth=1)
    axs[1, 0].plot(t_axis, integrate(np.sum(np.array(l_p_muscle), axis=0))[1: N + 1],
                   label='E tot muscles', color='magenta', linewidth=1)
    axs[1, 1].plot(t_axis[1:-1], differentiate(np.sum(np.array([Ec[1:], Ep[1:]]), axis=0)), label='P system',
                   color='white', linewidth=1)
    axs[1, 1].plot(t_axis, np.sum(np.array(l_p_muscle), axis=0), label='P tot muscles', color='magenta', linewidth=1)

    axs[0, 0].set_title('system energy')
    axs[0, 1].set_title('muscle energy')
    axs[1, 0].set_title('mechanical energy and total muscle energy')
    axs[1, 1].set_title('system power and total muscle power')

    axs[0, 0].set_xlabel('time (s)')
    axs[0, 1].set_xlabel('time (s)')
    axs[1, 0].set_xlabel('time (s)')
    axs[1, 1].set_xlabel('time (s)')

    axs[0, 0].set_ylabel('Energy (J)')
    axs[0, 1].set_ylabel('Energy (J)')
    axs[1, 0].set_ylabel('Energy (J)')
    axs[1, 1].set_ylabel('Power (W)')

    fig.patch.set_facecolor(background_color / 255)

    for ax in fig.get_axes():
        ax.legend()
        ax.set_facecolor(background_color / 255)
    plt.show()


def plot_phase_portrait():
    N = len(bones[0].l_theta) - 2

    for bone in bones:
        plt.plot(bone.l_theta[1:N], differentiate(bone.l_theta[2:N + 2]), linewidth=1)
    plt.show()


def plot_efforts():
    fig, axs = plt.subplots(2, 3)

    N = len(bones[0].l_theta) - 2

    t_axis = [i * t for i in range(N)]

    calves, quadriceps, hamstrings, low_back, lats = muscles
    axs[0, 0].plot(t_axis[1:], [l_efforts[i][low_back.index] for i in range(1, len(l_efforts))], label=low_back.name,
                   color='#8dd3c7', linewidth=1)
    axs[0, 1].plot(t_axis[1:], [l_efforts[i][quadriceps.index] for i in range(1, len(l_efforts))],
                   label=quadriceps.name, color='#feffb3', linewidth=1, )
    axs[0, 2].plot(t_axis[1:], [l_efforts[i][lats.index] for i in range(1, len(l_efforts))],
                   label=lats.name, color='#bfbbd9', linewidth=1)
    axs[1, 0].plot(t_axis[1:], [l_efforts[i][hamstrings.index] for i in range(1, len(l_efforts))],
                   label=hamstrings.name, color='#fa8174', linewidth=1)
    axs[1, 1].plot(t_axis[1:], [l_efforts[i][calves.index] for i in range(1, len(l_efforts))], label=calves.name,
                   color='#81b1d2', linewidth=1)

    name = {0: 'Q', 1: 'shoulder height', 2: 'gravity center pos', 3: 'gravity center speed',
            4: 'g', 5: 'dg/dt'}

    for j in range(len(l_Q[0])):
        axs[1, 2].plot(t_axis[1:], [l_Q[i][j] for i in range(1, len(l_Q))], label=name[j], linewidth=1)

    axs[0, 0].set_xlabel('time (s)')
    axs[0, 1].set_xlabel('time (s)')
    axs[0, 2].set_xlabel('time (s)')
    axs[1, 0].set_xlabel('time (s)')
    axs[1, 1].set_xlabel('time (s)')
    axs[1, 2].set_xlabel('time (s)')

    axs[0, 0].set_ylabel('normalized force')
    axs[0, 1].set_ylabel('normalized force')
    axs[0, 2].set_ylabel('normalized force')
    axs[1, 0].set_ylabel('normalized force')
    axs[1, 1].set_ylabel('normalized force')

    fig.patch.set_facecolor(background_color / 255)

    for ax in fig.get_axes():
        ax.legend()
        ax.set_facecolor(background_color / 255)

    axs[1, 2].set_yscale('log')

    plt.show()


def plot_Q():
    fig, ax = plt.subplots(1, 1)

    N = len(bones[0].l_theta) - 2

    t_axis = [i * t for i in range(0, N)]

    name = {0: 'Q', 1: 'shoulder height', 2: 'gravity center pos', 3: 'gravity center speed',
            4: 'g', 5: 'dg/dt'}  # where g is defined in brain.py

    fig.patch.set_facecolor(background_color / 255)

    for j in range(len(l_Q[0])):
        ax.plot(t_axis[1:], [l_Q[i][j] for i in range(1, len(l_Q))], label=name[j], linewidth=1)
        ax.set_facecolor(background_color / 255)
    ax.set_yscale('log')

    ax.legend()
    plt.show()
