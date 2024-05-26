from matrix import a_ij, b_i               
from bone import bones, muscles
from numpy.linalg import solve
from energy import *


n = len(bones)
m = len(muscles)


def update_bones(X, shallow_update=False):
    
    for bone in bones:
        bone.theta = X[bone.index]
        bone.l_theta.append(bone.theta)
        bone.update(shallow_update)  # argument increases performances


def update_model(efforts, shallow_update=False):

    # precompute to enhance performances

    c = [np.cos(bone.theta) for bone in bones]
    s = [np.sin(bone.theta) for bone in bones]
    l_forces = [bone.F_tot(efforts) for bone in bones]
    l_torques = [bone.C_tot(efforts) for bone in bones]

    # set the motion and reaction forces system

    A = np.array([[a_ij(i, j, n, c, s) for j in range(3 * n)] for i in range(3 * n)])  # n = len(bones)
    B = np.array([b_i(i, n, c, s, l_forces, l_torques) for i in range(3 * n)])

    # solve the system
    X = solve(A, B)
    
    update_bones(X, shallow_update)
    update_gravity_center()

    if not shallow_update:
        update_muscle_power(efforts)  # record the power given to the bone by the muscle
        update_energy()  # record the kinetic and potential energy of the system


def update_energy():
    Ec.append(total_kinetic_energy(bones))
    Ep.append(total_potential_energy(bones))


def update_muscle_power(_efforts):
    for i in range(m):
        l_p_muscle[i].append(p_muscle(muscles[i], _efforts[i]))


def update_gravity_center():  # get the center of mass of the system
    l_gravity_center.append(1 / sum([bone.m for bone in bones]) * np.sum(np.array([bone.m * bone.G for bone in bones]), axis=0))


def reverse_energy_changes():
    Ec.pop()
    Ep.pop()
    for i in range(len(l_p_muscle)):
        l_p_muscle[i].pop()


def reverse_l_gravity_center_changes():
    l_gravity_center.pop()


def reset_energy():
    global Ec, Ep, l_p_muscle
    Ec, Ep = [0], [total_potential_energy(bones)]
    l_p_muscle = [[0] for _ in range(len(muscles))]


efforts = np.array([0.36, 0.68, 1, 1, 0])
l_efforts = [efforts]

l_Q = [[-1532.1913424428103, 3749.6096493863097, 24.366758337800864, 0.0, 51.02162584457079, 5206.412607646748]]

Ec, Ep = [0], [total_potential_energy(bones)]
l_p_muscle = [[0] for _ in range(len(muscles))]

l_gravity_center = []

update_gravity_center()
update_gravity_center()
