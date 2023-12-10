from constants import *
from environment import Environment
from stable_baselines3 import PPO
from plot import *
import pygame as pg

env = Environment()
env.set_ep0()


if learning:
    model = PPO.load("deadlift_with_G", env=env)
    model = PPO('MlpPolicy', env, verbose=1)
    model.learn(total_timesteps=1000000)
    model.save("deadlift_with_G")

if testing:
    model = PPO.load("deadlift_with_G", env=env)
    while True:
        state = env.reset()
        done = False
        while not done:
            action, _states = model.predict(state)
            state, rewards, done, info = env.step(action)
            env.render()

elif plotting:  # simulation + graphs
    efforts = len(env.muscles)*[1]
    for i in range(N):
        env.step(efforts)
        env.render()
    pg.quit()
    if plot_e:
        plot_energies(env.Ec, env.Ep, env.l_p_muscle)
    if plot_m:
        plot_movement(env.bones, env.Ec, env.Ep)
    if plot_p:
        plot_phase_portrait(env.bones)

else:  # pygame simulation alone
    efforts = len(env.muscles)*[1]
    while running:
        for event in pg.event.get():
            if event == pg.QUIT:
                pg.quit()
        env.step(efforts)
        env.render()
