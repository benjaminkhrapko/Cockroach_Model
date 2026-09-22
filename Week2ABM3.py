import numpy as np
import matplotlib.pyplot as plt

dt = 0.1
rho = 1667
mu = 0.9

num_agents = 50
num_shelters = 3

max_time = 100
num_steps = int(max_time / dt)

theta = np.array([1.0, 1.5, 2.0])
phi = np.array([100, 125, 150])
agents = np.full(num_agents, -1)

agent_history = np.zeros(
    (num_steps + 1, num_agents),
    dtype=int)

agent_history[0] = agents
state_counts = np.zeros(
    (num_steps + 1, num_shelters + 1),
    dtype=int)

state_counts[0, 0] = np.sum(agents == -1)

for t in range(num_steps):
    shelter_counts = np.array([
        np.sum(agents == k)
        for k in range(num_shelters)
    ])

    new_agents = agents.copy()

    for i in range(num_agents):

        current_state = agents[i]

        if current_state == -1:

            action = np.random.choice(
                ["uncommitted", "find_shelter"],
                p=[mu, 1 - mu]
            )

            if action == "find_shelter":
                shelter = np.random.choice(num_shelters)
                p_reject = shelter_counts[shelter] / phi[shelter]
                p_reject = min(p_reject, 1.0)
                p_accept = 1 - p_reject

                entry = np.random.choice(
                    ["accept", "reject"],
                    p=[p_accept, p_reject])
                if entry == "accept":
                    new_agents[i] = shelter
                    state_counts[t + 1, shelter + 1] += 1
                else:
                     k = current_state
                    
                     density = shelter_counts[k] / phi[k]
                    
                     Q = theta[k] / (
                     1 + rho * density ** 2)
                                
                    
                     p_stay = np.exp(-Q * dt)
                     p_leave = 1 - p_stay
                    
                     action = np.random.choice(
                                    ["stay", "leave"],
                                    p=[p_stay, p_leave]
                                )
                    
                     if action == "leave":
                        new_agents[i] = -1
    agents = new_agents
    agent_history[t + 1] = agents
    state_counts[t + 1, 0] = np.sum(agents == -1)
    for k in range(num_shelters):
        state_counts[t + 1, k + 1] = np.sum(agents == k)
time = np.arange(num_steps + 1) * dt

plt.plot(
    time,
    state_counts[:, 0],
    label="Uncommitted"
)
for k in range(num_shelters):

    plt.plot(
        time,
        state_counts[:, k + 1],
        label=f"Shelter {k}"
    )

plt.xlabel("Time")
plt.ylabel("Number of agents")
plt.title("Model 3: Cockroach Shelter Aggregation")
plt.legend()
plt.show()

                    
                    
                    
                    

           