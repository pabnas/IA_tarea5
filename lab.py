import gym
import gym_gridworlds
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
from collections import Counter

from Gui import *

gui = GUI()

env = gym.make('WindyGridworld-v0') # Example 6.5 Sutton’s book
obs = env.reset() # Get initial state (3, 0)
#print(env.observation_space)

q_table = np.zeros([7,10,env.action_space.n])
#print(q_table[obs])
#action = 3  # 1 right     0 up    2 down    3 left

#
#   Training the agent
#

import random
#Hyperparameters
alpha = 0.3
gamma = 0.6
epsilon = 0.1

# For plotting metrics
all_epochs = []
episodes = 1001
reward_by_episode = np.zeros([episodes-1])
histogram_of_states = []

for i in range(1, episodes):
    state = env.reset()
    epochs, reward, = 0, 0

    done = False
    while not done:
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()  # Explore action space
        else:
            action = np.argmax(q_table[state])  # Exploit learned values

        next_state, reward, done, info = env.step(action)

        sum_reward = reward_by_episode[i-1]
        sum_reward = sum_reward+reward
        reward_by_episode[i-1] = sum_reward

        histogram_of_states.append((state))

        old_value = q_table[state][action]
        next_max = np.max(q_table[next_state])

        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state][action] = new_value

        state = next_state
        epochs += 1



    if i % 10 == 0:
        print("Training: " + str(i/10) + "%")

print("Training finished.\n")


#   
# Evaluate agent's performance after Q-learning
#
total_epochs = 0
episodes = 1

for _ in range(episodes):
    state = env.reset()
    epochs,reward = 0,0

    done = False
    while not done:
        action = np.argmax(q_table[state])
        state, reward, done, info = env.step(action)
        gui.show_state(state, q_table,True)
        sleep(.1)
        epochs += 1

    total_epochs += epochs

print("Results after " + str(episodes) + " episodes")
print("Average timesteps per episode: " + str(total_epochs / episodes))

plt.figure(1)
plt.plot(reward_by_episode)
plt.ylabel('Reward')
plt.xlabel('Episode')
#plt.savefig("reward_by_episode,alpha = 0.2,gamma = 0.6,epsilon = 0.9.png")
plt.show()

plt.figure(2)
c=Counter(histogram_of_states)
x=range(len(c))
y=[c[key] for key in sorted(c)]
xlabels=[str(t) for t in sorted(c)]
plt.bar(x,y)
plt.xticks([x+0.5 for x in x],xlabels)
plt.ylabel('Times in a state')
plt.xlabel('State')
#plt.savefig("Times in a state,alpha = 0.2,gamma = 0.6,epsilon = 0.9.png")
plt.show()

gui.wait()