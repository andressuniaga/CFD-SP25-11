# Script for OF1 : Refining the Solution part


#--------------------------------#

import numpy as np
import matplotlib.pyplot as plt

#-------------------------------#

Ufile = r"OF1\data\DeltaRe\cavityRe10\0.5\U"

Nx = Ny = 80 # gridsize

U = 1 #m/s

u = []

with open(Ufile, 'r') as f:
    lines = f.readlines()              

for i in lines:
    if i.startswith("("):
        k = i.split()[0][1:]
        u.append(k)

# all x-component velocities from y=0 to y=1
u = u[1:]
u = np.array(u,dtype=float)

# adding u(x/L,y/L=1) = 1 condition
for i in range(80):
    u = np.append(u,U)

