import numpy as np
import matplotlib.pyplot as plt

dt = 0.1
rho = 1667
mu = 0.9

num_agents = 50
num_shelters = 5

max_time = 1000
num_steps = int(max_time / dt)

theta = np.array([1.0, 1.1, 1.2, 1.3, 1.4])
phi = np.array([100, 125, 150, 175, 200])
agents = np.full(num_agents, -1) # all agents start out uncommitted, represented by -1

agent_history = np.zeros(
    (num_steps + 1, num_agents), #rows, columns to track the state of each agent over time
    dtype=int)

agent_history[0] = agents #documents that the first row of agent history is 'agents' which is -1.
state_counts = np.zeros( # separate array for the totals in each, we will use this to plot
    (num_steps + 1, num_shelters + 1),
    dtype=int)

state_counts[0, 0] = np.sum(agents == -1) # counts how many are uncommited and adds them

for t in range(num_steps):
    shelter_counts = np.array([
        np.sum(agents == k)
        for k in range(num_shelters) #loops over and counts how many agents are in each shelter
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
                shelter = np.random.choice(num_shelters) #1-mu/num shelter. each shelter has equal probability of being chosen.
                p_reject = shelter_counts[shelter] / phi[shelter]
                p_reject = min(p_reject, 1.0) # stops probability from being higher than 1. for exampe if population is higher than capacity. we dont have built in function to make sure it stops autoatically at capacity. mabe implement. 
                p_accept = 1 - p_reject

                entry = np.random.choice(
                    ["accept", "reject"],
                    p=[p_accept, p_reject])
                if entry == "accept":
                    new_agents[i] = shelter
                    
        else:
                
            k = current_state
        
            density = shelter_counts[k] / phi[k]
        
            Q = theta[k] / (
            1 + rho * density)  #if density increasas, q decreases. when conversion to probability, p_stay increases and p_leave decreases. so if density is high, the agent is more likely to stay in the shelter.
                    
        
            p_stay = np.exp(-Q * dt) #P(stay)= e^(-Q*dt) . INVERSE
            p_leave = 1 - p_stay
        
            action = np.random.choice(
                        ["stay", "leave"],
                        p=[p_stay, p_leave]
                    )
                    
            if action == "leave": #agent uncommited again, becomes "-1"
                new_agents[i] = -1
    agents = new_agents #updates everyone
    agent_history[t + 1] = agents
    state_counts[t + 1, 0] = np.sum(agents == -1)
    for k in range(num_shelters):
        state_counts[t + 1, k + 1] = np.sum(agents == k) #K+1 because column 0 is already used for uncommitted agents. This counts how many agents are in each shelter and stores it in the state_counts array, which will be used for plotting later.
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

                    
                    
                    
                    

           