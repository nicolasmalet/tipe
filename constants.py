

g = 9.81  # gravity constant of Earth at the sea level


t = 1 * 10 ** (-3)  # time for euler's method, the lower the time, the better the approximation
simulation_time = 10  # duration of the model
N = int(simulation_time / t)  # number of steps needed


# You can change the following variables depending on what you want to see

running = True
plotting = True
plot_e = True  # plot energies
plot_m = False  # plot movement

simulation = True  # show the system
draw_v_tendon = False  # show the velocity of each tendon
draw_forces = False  # show the forces applied by muscles on bones
