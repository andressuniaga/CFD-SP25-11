# Script for OF1 : Refining the Solution part


#--------------------------------#

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid

#-------------------------------#

Re = [10,50,100,250,500]
endtime = [0.5, 1.5, 2.5, 3, 4]
F = []

for r in range(len(Re)):
    Ufile = rf"OF1\data\DeltaRe\cavityRe{Re[r]}\{endtime[r]}\U"
    print(f"Reading {Ufile}")

    Nx = Ny = 80 # gridsize

    L = 0.1 # 0.1m
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

    Ux = np.zeros([Nx,Ny])

    # Mean x-component velocity in each row starting from row y=1 to y=0
    for i in range(Nx):
        for j in range(Ny):
            Ux[i,j] = u[(Nx*Ny-80*(i+1))+j]

    x = np.linspace(0,L,Ny)/L
    dx=dy=1/Nx

    tau = np.zeros(Nx)
    n = 4  # rows to fit 

    #polynomial fitting
    for i in range(Nx):
        a,b,c = np.polyfit(x[0:n],Ux[0:n,i],2)
        tau[i] = 2*a*(1) + b

    #Finite Difference Approximation 
    tau2 = np.zeros(Nx)   

    for i in range(Nx):
        tau2[i] = (Ux[0,i] - Ux[1,i])/dy

    figRe = plt.figure(0,figsize=(8,6))
    figRe.canvas.manager.set_window_title("Nondimensional Stress vs. x")

    plt.plot(x,tau,linewidth=2,label=f"Re = {Re[r]}")
    # plt.plot(x,tau2,linewidth=2,label=f"Re = {Re[r]} tau2")
    plt.title("$\\tilde{\\tau}$ vs. $\\tilde{x}$, Meshsize = " f"{Nx}x{Ny}", fontsize = 16)
    plt.ylabel(r"$\tilde{\tau}$         ",fontsize=14,rotation=0)
    plt.xlabel(r"$\tilde{x}$",fontsize=14)
    plt.grid()
    plt.legend(loc="lower left")

    F.append(trapezoid(tau,x,dx=dx))


figRe = plt.figure(1,figsize=(8,6))
figRe.canvas.manager.set_window_title("Nondimensional Force vs. Re")
plt.plot(Re,F,'rs',markersize=7)
plt.title("$\\tilde{F}$ vs. Re, Meshsize = " f"{Nx}x{Ny}", fontsize = 16)
plt.ylabel(r"$\tilde{F}$         ",fontsize=14,rotation=0)
plt.xlabel(r"Re",fontsize=14)
plt.grid()

plt.show()


