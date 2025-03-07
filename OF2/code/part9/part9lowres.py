#--------------------------------#

import numpy as np
import matplotlib.pyplot as plt

#-------------------------------#

# 1 is for L/D Part
# 2 is for ur,utheta

select = 1


match select:
    case 1:
        file = 'OF2\\code\\part9\\25\\L_U.xy'

        print(f"Reading {file}")

        u = [0] # x-direction velocity
        x = [0.5] # x-position
        D = 1

        with open(file, 'r') as f:
            for l in f:
                k = l.split(" ")
                x.append(k[0])
                u.append(k[3])

        x = np.array(x,dtype=float)
        u = np.array(u,dtype=float)

        for i in range(len(u)):
            if u[i]>0:
                point = i
                break

        m = (u[point] - u[point-1])/(x[point]-x[point-1])

        x0 = (u[point-1])/m + x[point-1] # linear interpolation for getting point where u = 0

        L = x0-x[0]

        print(f"L/D = {L}")

    case 2:
        file_pi4 = 'OF2\\code\\part9\\25\\pi4_U.xy'
        file_pi2 = 'OF2\\code\\part9\\25\\pi2_U.xy'
        file_3pi4 = 'OF2\\code\\part9\\25\\threepi4_U.xy'

        xpi4 = [0.35355339059327]
        ypi4 = [0.35355339059327]
        upi4 = [0]
        vpi4 = [0]

        with open(file_pi4, 'r') as f:
            for l in f:
                k = l.split(" ")
                xpi4.append(k[0])
                ypi4.append(k[1])
                upi4.append(k[3])
                vpi4.append(k[4])
        
        xpi4 = np.array(xpi4,dtype=float)
        ypi4 = np.array(ypi4,dtype=float)
        upi4 = np.array(upi4,dtype=float)
        vpi4 = np.array(vpi4,dtype=float)

        xpi2 = [0]
        ypi2 = [0.5]
        upi2 = [0]
        vpi2 = [0]

        with open(file_pi2, 'r') as f:
            for l in f:
                k = l.split(" ")
                xpi2.append(k[0])
                ypi2.append(k[1])
                upi2.append(k[3])
                vpi2.append(k[4])

        xpi2 = np.array(xpi2,dtype=float)
        ypi2 = np.array(ypi2,dtype=float)
        upi2 = np.array(upi2,dtype=float)
        vpi2 = np.array(vpi2,dtype=float)


        x3pi4 = [-0.35355339059327]
        y3pi4 = [0.35355339059327]
        u3pi4 = [0]
        v3pi4 = [0]

        with open(file_3pi4, 'r') as f:
            for l in f:
                k = l.split(" ")
                x3pi4.append(k[0])
                y3pi4.append(k[1])
                u3pi4.append(k[3])
                v3pi4.append(k[4])

        x3pi4 = np.array(x3pi4,dtype=float)
        y3pi4 = np.array(y3pi4,dtype=float)
        u3pi4 = np.array(u3pi4,dtype=float)
        v3pi4 = np.array(v3pi4,dtype=float)

        spi4 = np.zeros(len(xpi4))
        spi2 = np.zeros(len(xpi2))
        s3pi4 = np.zeros(len(x3pi4))

        for i in range(len(xpi4)):
            spi4[i] = np.sqrt(xpi4[i]**2 + ypi4[i]**2)
        for i in range(len(xpi2)):
            spi2[i] = np.sqrt(xpi2[i]**2 + ypi2[i]**2)

        for i in range(len(x3pi4)):
            s3pi4[i] = np.sqrt(x3pi4[i]**2 + y3pi4[i]**2)


        # distances
        spi4 = spi4-spi4[0]
        spi2 = spi2 - spi2[0]
        s3pi4 - s3pi4 - s3pi4[0]

        #radial and tangential velcocities

        urpi4 = np.zeros(len(upi4))
        utpi4 = np.zeros(len(upi4))

        urpi2 = np.zeros(len(upi2))
        utpi2 = np.zeros(len(upi2))

        ur3pi4 = np.zeros(len(u3pi4))
        ut3pi4 = np.zeros(len(u3pi4))

        for i in range(len(upi4)):
            urpi4[i] = upi4[i]*np.cos(np.pi/4) + vpi4[i]*np.sin(np.pi/4)
            utpi4[i] = -upi4[i]*np.sin(np.pi/4) + vpi4[i]*np.cos(np.pi/4)

        for i in range(len(upi2)):
            urpi2[i] = upi2[i]*np.cos(np.pi/2) + vpi2[i]*np.sin(np.pi/2)
            utpi2[i] = -upi2[i]*np.sin(np.pi/2) + vpi2[i]*np.cos(np.pi/2)

        for i in range(len(u3pi4)):
            ur3pi4[i] = u3pi4[i]*np.cos(3*np.pi/4) + v3pi4[i]*np.sin(3*np.pi/4)
            ut3pi4[i] = -u3pi4[i]*np.sin(3*np.pi/4) + v3pi4[i]*np.cos(3*np.pi/4)


        plt.figure(1,figsize=(8,6))
        plt.plot(spi4,urpi4,linewidth=1.5,label="Radial Velocity")
        plt.plot(spi4,utpi4,linewidth=1.5,label="Tangential Velocity")
        plt.title(r"At $\pi/4$")
        plt.ylabel("Velocity")
        plt.xlabel("Distance from Cylinder")
        plt.grid()
        plt.legend()

        plt.figure(2,figsize=(8,6))
        plt.plot(spi2,urpi2,linewidth=1.5,label="Radial Velocity")
        plt.plot(spi2,utpi2,linewidth=1.5,label="Tangential Velocity")
        plt.title(r"At $\pi/2$")
        plt.ylabel("Velocity")
        plt.xlabel("Distance from Cylinder")
        plt.grid()
        plt.legend()

        plt.figure(3,figsize=(8,6))
        plt.plot(s3pi4,ur3pi4,linewidth=1.5,label="Radial Velocity")
        plt.plot(s3pi4,ut3pi4,linewidth=1.5,label="Tangential Velocity")
        plt.title(r"At $3\pi/4$")
        plt.ylabel("Velocity")
        plt.xlabel("Distance from Cylinder")
        plt.grid()
        plt.legend()
    
        plt.show()
    









        