from matrix import a_ij, b_i               
from plot import update_energy, update_muscle_power
from bone import update_gravity_center, n
from numpy.linalg import solve


def update_bones(bones, X):
    
    for bone in bones:
        bone.theta = X[bone.index]
        bone.l_theta.append(bone.theta)
        bone.update()


def update_model(bones, efforts):
    
    # set the motion and reaction forces system
    A = [[a_ij(i, j, n) for j in range(3 * n)] for i in range(3 * n)]
    B = [b_i(i, n, efforts) for i in range(3 * n)]

    # solve the system
    X = solve(A, B)
    
    update_bones(bones, X)
    
    update_gravity_center(bones)
    update_energy(bones)  # record the kinetic and potential energy of the system
    update_muscle_power(efforts)  # record the power given to the bone by the muscle
        