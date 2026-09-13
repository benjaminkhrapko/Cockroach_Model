import numpy as np
import matplotlib.pyplot as plt
import random

def normal(vector):
           length=np.sqrt(vector[0]**2+vector[1]**2)
           return vector/length

ap=np.array([0,0])

max_time = 10000

all_positions=np.zeros((max_time+1,2))
all_positions[0]=ap

for t in range(1,max_time+1):
        direction=np.random.normal(size=2)
while np.all(direction==0):
        direction=np.random.normal(size=2)
new_direction=direction=normal(direction)
new_position=ap+new_direction
all_positions[t]=new_position

ap=new_position