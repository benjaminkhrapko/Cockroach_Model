import numpy as np
import matplotlib.pyplot as plt

dt = 0.1
rho = 1667

num_agents = 50
num_shelters = 3

theta = np.array([1.0, 1.5, 2.0])
phi = np.array([100, 125, 150])

max_time = 100
num_steps = int(max_time / dt)

agents = np.random.randint(0, num_shelters, size=num_agents)

shelter_counts = np.zeros(
    (num_steps + 1, num_shelters),
    dtype=int)
shelter_counts[0] = np.bincount(
    agents,
    minlength=num_shelters)

for t in range(num_steps):
    counts=np.bincount(agents, minlength=num_shelters)

    new_agents = np.copy(agents)

    for i in range(num_agents):
        k=agents[i]
        density=counts[k]/phi[k]
        Q=theta[k]/(1+rho*density**2)
        p_stay = np.exp(-Q * dt)
        p_leave = 1 - p_stay

        action = np.random.choice(
            ['stay', 'leave'],
            p=[p_stay, p_leave])

        if action == 'leave':
            possible_shelters=np.delete(
                np.arange(num_shelters),
                k)
            new_agents[i] = np.random.choice(possible_shelters)
    agents = new_agents
    shelter_counts[t + 1] = np.bincount(
        agents,
        minlength=num_shelters)

    time = np.arange(num_steps + 1) * dt

for k in range(num_shelters):

    plt.plot(
        time,
        shelter_counts[:, k],
        label=f"Shelter {k}"
    )

plt.xlabel("Time")
plt.ylabel("Number of agents")
plt.title("Model 1: Cockroach Shelter Aggregation")
plt.legend()

plt.show()



        
