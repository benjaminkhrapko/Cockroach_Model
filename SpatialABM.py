import numpy as np
import matplotlib.pyplot as plt

num_shelters = 7
arena_min = -15
arena_max = 15

shelter_radius = 1.5
inner_ring_radius = 5
outer_ring_radius = 10
step_size = 0.5
max_walk_steps = 10000
num_walks_per_shelter = 1000

target_center = np.array([0.0, 0.0])
num_per_ring = 3
angles = np.linspace(
    0,
    2 * np.pi,
    num_per_ring,
    endpoint=False
)
inner_centers = np.column_stack(( #combines the two arrays. (x and y)
    inner_ring_radius * np.cos(angles),
    inner_ring_radius * np.sin(angles)
))
outer_angles = angles + np.pi / 3 #rotates it 60 degrees so that the outer shelters are not directly in line with the inner shelters.

outer_centers = np.column_stack((
    outer_ring_radius * np.cos(outer_angles),
    outer_ring_radius * np.sin(outer_angles)
))

shelter_centers = np.vstack(( # vertically stack them
    target_center,
    inner_centers,
    outer_centers
))

def find_shelter(x, y): #going to locate is point is within shelter radius of any of the shelters. if it is, return the index of that shelter. if not, return -1.

    for k in range(num_shelters):

        center_x = shelter_centers[k, 0]
        center_y = shelter_centers[k, 1]

        distance_squared = (
            (x - center_x) ** 2
            + (y - center_y) ** 2
        )

        if distance_squared <= shelter_radius ** 2:
            return k

    return -1 # if not in any shelter, return -1 (uncommited)

def random_walk_step(x, y):
    angle = np.random.uniform(0, 2 * np.pi) #selects a number from a continous random distribution
    dx = step_size * np.cos(angle)
    dy = step_size * np.sin(angle)

    new_x = x + dx
    new_y = y + dy

    if new_x < arena_min: # boundary for -15
        new_x = 2 * arena_min - new_x #refelcts the change to the inside of the arena. for example if it goes to -16, it will reflect to -14. if it goes to -17, it will reflect to -13.

    elif new_x > arena_max: #boundary for 15
        new_x = 2 * arena_max - new_x

    if new_y < arena_min:
        new_y = 2 * arena_min - new_y

    elif new_y > arena_max:
        new_y = 2 * arena_max - new_y

    return new_x, new_y

transition_counts = np.zeros(
    (num_shelters, num_shelters), #7 x 7 matrix
    dtype=int)

for start_shelter in range(num_shelters):

    for walk in range(num_walks_per_shelter):
        start_angle = np.random.uniform(0, 2 * np.pi) # starts at a random angle from 0 to 2pi (360)
        start_distance = np.random.uniform(shelter_radius+step_size) #places the starting point just outside the shelter radius, so that it is not already in a shelter.

        x = (shelter_centers[start_shelter, 0] + start_distance * np.cos(start_angle)) 
        y = (shelter_centers[start_shelter, 1] + start_distance * np.sin(start_angle))
            
            
        for step in range(max_walk_steps):

            x, y = random_walk_step(x, y)

            encountered_shelter = find_shelter(x, y)

            if (
                encountered_shelter != -1
                and encountered_shelter != start_shelter
            ):

                transition_counts[
                    start_shelter,
                    encountered_shelter
                ] += 1

                break
T = np.zeros(
    (num_shelters, num_shelters),
    dtype=float
)

for start_shelter in range(num_shelters):

    total_transitions = np.sum(
        transition_counts[start_shelter]
    )

    if total_transitions > 0:

        T[start_shelter] = (
            transition_counts[start_shelter]
            / total_transitions)



print("Shelter centers:")
print(shelter_centers)

print("\nTransition counts:")
print(transition_counts)

print("\nTransition probability matrix T:")
print(np.round(T, 3))

print("\nRow sums:")
print(np.sum(T, axis=1))

fig, ax = plt.subplots()

ax.set_xlim(arena_min, arena_max)
ax.set_ylim(arena_min, arena_max)
ax.set_aspect("equal")

for k in range(num_shelters):

    circle = plt.Circle(
        shelter_centers[k],
        shelter_radius,
        fill=False
    )

    ax.add_patch(circle)

    ax.scatter(
        shelter_centers[k, 0],
        shelter_centers[k, 1]
    )

    ax.text(
        shelter_centers[k, 0],
        shelter_centers[k, 1],
        str(k)
    )

plt.xlabel("X position")
plt.ylabel("Y position")
plt.title("Spatial ABM Shelter Layout")

plt.show()
        

            
        
    