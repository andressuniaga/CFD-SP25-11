# Script for OF1 : Refining the Solution part


#--------------------------------#

import numpy as np
import matplotlib.pyplot as plt

#-------------------------------#



gridsize = [20,40,80,160]

i = 0

L = 0.1 #m
nu = 0.01 #m^2/s
U = 1 #m/s
Re = L*U/nu

for k in range(len(gridsize)):
    Nx = Ny = gridsize[k]

    file_path  = f'OF1\\code\\U\\verticalmidline_U_{Nx}.xy'

    y = []
    u = []
    v = []

    with open(file_path, 'r') as f:
        for l in f:
            k = l.split(" ")
            y.append(k[1])
            u.append(k[3])
            v.append(k[4])
            
    y = np.array(y,dtype=float)
    u = np.array(u,dtype=float)
    v = np.array(v,dtype=float)

    figk = plt.figure(i,figsize=(8,6))
    figk.canvas.manager.set_window_title(f"Velocity Component Plot for gridsize {Nx}x{Ny}")

    c=100

    plt.plot(u,y/L,'-o',label=r"$u/U$")
    plt.plot(v*c,y/L,'-s',label=rf"$v/U \times {c}$")
    plt.title(r"$\tilde{u}$, $\tilde{v}$ vs. $y/L$ ($x/L = 0.5$)", fontsize=16)
    plt.ylabel(r"$\tilde{y}$",fontsize=12)
    plt.xlabel(r"$\tilde{u}, \tilde{v}$",fontsize=12)
    plt.grid()
    plt.legend(loc='lower right',fontsize = 12)
    
    i+=1

# times in seconds
EndTime = 0.5
ExecutionTimes = [0.13,0.58,5.93,91.66]
dt = [0.005,0.0025,0.00125,0.000625]
iterations = []
C = [] # execution time per step
N = []
for i in range(len(dt)):
    iterations.append(EndTime/dt[i])
    C.append(ExecutionTimes[i]/iterations[i])
    N.append(gridsize[i]**2)


# fit
a, b = np.polyfit(np.log10(N),np.log10(C),deg=1) # linear log fitting
b = 10**b

figNC = plt.figure(i+1,figsize=(8,6))
figNC.canvas.manager.set_window_title("Refinement Measure")

plt.loglog(N,C,'r-s')
plt.plot(N,b*N**a,'k',linewidth = 1.5, label = r"$C = \beta N^{\alpha} $")
plt.title(r"$C$ vs. $N$" '\n' r"$\beta = $"  f"{b:.3e}, " r"$\alpha = $" f" {round(a,3)}", fontsize=16)
plt.ylabel("C (seconds/step)",fontsize=12)
plt.xlabel("N (gridpoints)",fontsize=12)
plt.grid()
plt.legend(loc='lower right',fontsize = 12)
plt.show()











