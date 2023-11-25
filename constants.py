

g = 9.81  # gravity constant of Earth at the sea level


t = 1 * 10 ** (-3)  # time for euler's method, the lower the time, the better the approximation
simulation_time = 5  # duration of the model
N = int(simulation_time / t)  # number of steps needed


# You can change the following variables depending on what you want to see

running = True
plotting = True

plot_m = True  # plot movement
plot_e = False  # plot energies
plot_p = False  # plot phase portrait

simulation = True  # show the system
draw_ground = True  # draw the ground
draw_v_tendon = False  # show the velocity of each tendon
draw_forces = False  # show the forces applied by muscles on bones


background_color = (20, 20, 20)
ground_color = (50, 50, 50)
bone_color = (255, 255, 255)
muscle_color = (255, 0, 0)
