from energy import total_kinetic_energy, total_potential_energy
from bone import bones
import matplotlib.pyplot as plt
from constants import t, N
from utils import l_sum

fig, axs = plt.subplots(2, 2)

Ec, Ep = [], []
velocities = []
accelerations = []


def update_energy():
    Ec.append(total_kinetic_energy(bones))
    Ep.append(total_potential_energy(bones))


def update_velocity():
    velocities.append([bone.angular_velocity() for bone in bones])


def update_acceleration():
    accelerations.append([bone.angular_acceleration() for bone in bones])


def unpack(l, i):
    return [l[j][i] for j in range(len(l))]


def plot_all():  # plot each graph
    t_axis = [i * t for i in range(N)]

    for i in range(len(bones)):
        axs[0, 0].plot(t_axis, bones[i].angles[0:N], label='theta' + str(i))
        axs[0, 1].plot(t_axis, unpack(velocities, i), label='theta' + str(i) + '_dot')
        axs[1, 0].plot(t_axis, unpack(accelerations, i), label='theta' + str(i) + '_dotdot')

    axs[1, 1].plot(t_axis, Ec, label='Ec', color='red')
    axs[1, 1].plot(t_axis, Ep, label='Ep', color='blue')
    axs[1, 1].plot(t_axis, l_sum(Ec, Ep), label='E', color='black')

    for ax in fig.get_axes():
        ax.legend()

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

    plt.show()
