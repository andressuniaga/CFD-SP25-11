# Script for OF2 : blockmeshvertices

# outputs x-y vertices


#--------------------------------#

import numpy as np
import matplotlib.pyplot as plt

#-------------------------------#

def arcvertices(D,R,N=32):
    '''
    Inputs: 
    N = Number of vertices
    D = Diameter of circular cylinder
    R = Distance between circular cylinder and outer circle
    '''
    if N%16!=0 or N<32:
        print("Ensure N is divisible by 16 and at least 32.")
        return None
    else:
        num = N//4
        theta = np.linspace(0,2*np.pi,num+1)
        pinner = np.zeros([2,num])
        pouter = np.zeros([2,num])
        for i in range(num):
            pinner[0,i] = (D/2)*np.cos(theta[i])
            pinner[1,i] = (D/2)*np.sin(theta[i])

            pouter[0,i] = (D/2 + R)*np.cos(theta[i])
            pouter[1,i] = (D/2 + R)*np.sin(theta[i])

        return pinner, pouter

def walls(Lf,Lw,H,outer, N=32):
    '''
    Inputs: 
    N = Number of vertices
    Lf = Length at the fore of the circular cylinder
    Lw = Length at the wake of the circular cylinder
    H = Half height of inlet/outlet
    outer = The outer circle's vertices
    D = Diameter of circular cylinder
    R = Distance between circular cylinder and outer circle
    '''
    if N%16!=0 or N<32:
        print("Ensure N is divisible by 16 and at least 32.")
        return None
    else:
        corners = np.zeros([2,4]) # always four corners to a square
        for i in range(4):
            a = -Lf
            b = H
            if i%2==0:
                a = Lw
            if i > 1:
                b = -H
            corners[0,i] = a
            corners[1,i] = b

        inlet = np.zeros([2,N//8])
        top = np.zeros([2,N//8])
        bottom = np.zeros([2,N//8])
        outlet = np.zeros([2,N//8])

        for i in range(N//8):
            top[1,i] = H
            bottom[1,i] = -H
            inlet[0,i] = -Lf
            outlet[0,i] = Lw

            if -outer[0,0]<outer[0,i]<outer[0,0]:
                top[0,i] = outer[0,i]
                bottom[0,i] = outer[0,i]  

            if outer[1,i] < max(outer[1]):
                inlet[1,i] = outer[1,i]
                outlet[1,i] = outer[1,i]
            
        for i in range(1,N//8//2):
                inlet[1,-i] = -inlet[1,i]
                outlet[1,-i] = -outlet[1,i]

        # putting in corner points
        outlet[0,-N//16] = corners[0,0]
        outlet[1,-N//16] = corners[1,0]

        top[0,-N//16] = corners[0,1]
        top[1,-N//16] = corners[1,1]

        bottom[0,-N//16] = corners[0,2]
        bottom[1,-N//16] = corners[1,2]
        
        inlet[0,-N//16] = corners[0,3]
        inlet[1,-N//16] = corners[1,3]

        topnew = np.zeros([2,N//8])
        bottomnew = np.zeros([2,N//8])
        inletnew = np.zeros([2,N//8])

        a = (N//8)//2 - 1 #index to start and rearrange points
        for i in range(N//8):
            topnew[0,i] = top[0,a-i]
            topnew[1,i] = top[1,a-i]
            bottomnew[0,i] = bottom[0,a-i]
            bottomnew[1,i] = bottom[1,a-i]
            inletnew[0,i] = inlet[0,a-i]
            inletnew[1,i] = inlet[1,a-i]

        top = topnew
        bottom = bottomnew
        inlet = inletnew
                        
        return top,bottom,inlet,outlet

def blockmesh_2D(inner,outer,inlet,top,outlet,bottom,N=32):
    if N%16!=0 or N<32:
        print("Ensure N is divisible by 16 and at least 32.")
        return None
    else:
        # Coding up the 2D Block Mesh vertices in order
        # refer to helpful\OF2\10.OF-tutorial-2-Part-2.2019.03.05.pdf
        points = np.zeros([2,N])

        for i in range(N//2): # circular points
            if i < N//4:
                points[0,i] = inner[0,i]
                points[1,i] = inner[1,i]
            else:
                points[0,i] = outer[0,i-N//4]
                points[1,i] = outer[1,i-N//4]

        together_x = []
        together_y = []

        # ugly section of code but works
        for i in range(N//8):
            if outlet[1,i] >= 0:
                together_x.append(outlet[0,i])
                together_y.append(outlet[1,i])
        for i in range(N//8):
            together_x.append(top[0,i])
            together_y.append(top[1,i])
        for i in range(N//8):
            together_x.append(inlet[0,i])
            together_y.append(inlet[1,i])
        for i in range(N//8):
            together_x.append(bottom[0,i])
            together_y.append(bottom[1,i])
            
        for i in range(len(together_x)):
            points[0,i+N//2] = together_x[i]
            points[1,i+N//2] = together_y[i]
        
        for i in range(1,N//8//2):
            points[0,-i] = outlet[0,-i]
            points[1,-i] = outlet[1,-i]

        return points

       

if __name__ == "__main__":
    # Initial Parameters
    N = 32 # number of points (multiples of 16)

    D = 1 # diameter of cylinder

    Lf = 10
    Lw = 20
    R = 1 
    H = 5

    cylinder,outer = arcvertices(D,R,N)
    top,bottom,inlet,outlet = walls(Lf,Lw,H,outer,N)

    # 2D PLOT
    plt.figure(figsize=(12,4))
    # plt.plot(cylinder[0],cylinder[1],'r.')
    # plt.plot(outer[0],outer[1],'r.')
    # plt.plot(top[0],top[1],'k.')
    # plt.plot(bottom[0],bottom[1],'k.')
    # plt.plot(inlet[0],inlet[1],'k.')
    # plt.plot(outlet[0],outlet[1],'k.')


    # print("top:\n", top,'\n',"bottom:\n",bottom,'\n'
    #       "inlet:\n", inlet,'\n',"outlet:\n",outlet,'\n')
    
    vertices = blockmesh_2D(cylinder,outer,inlet,top,outlet,bottom,N)

    plt.plot(vertices[0],vertices[1],'r.')
    plt.grid()

    # 3D PLOT
    plt.figure()
    ax = plt.axes(projection = '3d')
    x = vertices[0]
    y = vertices[1]
    z1 = -0.5
    z2 = 0.5
    ax.plot(x,y,z1,'r.')
    ax.plot(x,y,z2,'k.')

    # print(vertices)

    plt.show()