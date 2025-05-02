import numpy as np
import matplotlib.pyplot as plt

#--------------------------------#

# Diamond Airfoil Mesh

#--------------------------------#

# 32 Vertices 
# 8 Blocks
# 4 Faces

def diamondsection(L,theta,z):
    '''
    Inputs: L (Length), theta (deflection angle in degrees), z (z-location)
    Output: v (vertices) 
    '''
    r = 3 # rows : x-y-z
    c = 4 # cols : 4-points needed for diamond

    v = np.zeros([r,c])

    a = L/2
    b = (L/2)*np.tan(theta*np.pi/180)

    for i in range(c):
        v[0,i] = a*np.cos(i*np.pi/2)
        v[1,i] = b*np.sin(i*np.pi/2)
        v[2,i] = z
    return v

def facevertices(DR,DL,H,L,theta,z):
    '''
    Inputs: 
    - DR (Distance Right from Diamond)
    - DL (Distance Left from Diamond)
    - H (Height from Diamond)
    - L (Length of Diamond)
    - theta (Diamond deflection angle in degrees)
    - z (z-location)

    Outputs:
    -outlet, inlet, top, bottom (Points of each respective face)
    '''
    r = 3
    c = 12 

    a = L/2
    b = (L/2)*np.tan(theta*np.pi/180)

    outlet = np.zeros([r,c//4])
    inlet = np.zeros([r,c//4])
    top = np.zeros([r,c//4])
    bottom = np.zeros([r,c//4])

    for i in range(c//4):
        outlet[0,i] = DR+a
        outlet[1,i] = (H+b)*np.sin((i-1)*np.pi/2)
        outlet[2,i] = z

        inlet[0,i] = -(DL+a)
        inlet[1,i] = (H+b)*np.sin((i+1)*np.pi/2)
        inlet[2,i] = z

        top[0,i] = (a)*np.cos(i*np.pi/2)
        top[1,i] = H+b
        top[2,i] = z

        bottom[0,i] = -(a)*np.cos(i*np.pi/2)
        bottom[1,i] = -(H+b)
        bottom[2,i] = z

    return outlet, inlet, top, bottom
    
def allvertices(v,o,i,t,b):
    '''
    Inputs:
    - v (Diamond vertices)
    - o (Outlet vertices)
    - i (Inlet vertices)
    - t (Top vertices)
    - b (Bottom vertices)
    \n
    Ouput:
    - p (All vertices)
    '''
    r = 3   
    c = 16

    p = np.zeros([r,c])

    n = c//4

    p[:,0:n] = v
    p[:,n:n+2] = o[:,1:]
    p[:,n+2:n+5] = t[:,:]
    p[:,n+5:n+8] = i[:,:]
    p[:,n+8:n+11] = b[:,:]
    p[:,-1] = o[:,0]

    return p

if __name__ == "__main__":
    L = 1
    theta = 10 # degrees

    DL = 1
    DR = 1.5
    H = 1

    diamond = diamondsection(L,theta,0)
    outlet,inlet,top,bott = facevertices(DR,DL,H,L,theta,0)

    p = allvertices(diamond,outlet,inlet,top,bott)

    mesh = plt.figure(figsize=(10,5))
    mesh.canvas.manager.set_window_title("2D Diamond Airfoil Mesh")

    # Edges

    #DIAMOND
    diamondedges = np.zeros([3,5])
    diamondedges[:,0:4] = diamond
    diamondedges[:,4] = diamond[:,0]
    for i in range(4):
        plt.plot(diamondedges[0,i:i+2],diamondedges[1,i:i+2],'b-')
    
    # OUTER
    pedges = np.zeros([3,13])
    pedges[:,0:12] = p[:,4:]
    pedges[:,12] = p[:,4]
    for i in range(12):
        plt.plot(pedges[0,i:i+2],pedges[1,i:i+2],'k-')

    # INNER
    inner1 = np.zeros([3,8])
    inner2 = np.zeros([3,8])

    c = 4
    for i in range(4):

        inner1[0,2*i] = p[0,i]
        inner1[0,2*i+1] = p[0,i+c]

        inner1[1,2*i] = p[1,i]
        inner1[1,2*i+1] = p[1,i+c]

        inner1[2,2*i] = p[2,i]
        inner1[2,2*i+1] = p[2,i+c]

        c = c + 2
    
    for i in range(4):
        plt.plot(inner1[0,2*i:2*i+2],inner1[1,2*i:2*i+2],'k-')

    c = 6
    for i in range(4):
        if i%2==0:
            k = 0
        else:
            k = 2
        
        if i == 2:
            c = 14
        elif i==3:
            c = 10
    
        inner2[0,2*i] = p[0,k]
        inner2[0,2*i+1] = p[0,k+c]

        inner2[1,2*i] = p[1,k]
        inner2[1,2*i+1] = p[1,k+c]

    for i in range(4):
        plt.plot(inner2[0,2*i:2*i+2],inner2[1,2*i:2*i+2],'k-')

    # Vertices
    plt.plot(diamond[0],diamond[1],'b.',label="Diamond")
    plt.plot(outlet[0],outlet[1],'s',label="Outlet")
    plt.plot(inlet[0],inlet[1],'s',label="Inlet")
    plt.plot(top[0],top[1],'s',label="Top")
    plt.plot(bott[0],bott[1],'s',label="Bottom")
    plt.title(fr"$\theta$ = {theta}$\degree$ Diamond Airfoil, 2D Mesh")
    plt.legend()
    plt.grid()


    visualizationmesh = plt.figure()
    visualizationmesh.canvas.manager.set_window_title("Visualization Diamond Airfoil Mesh")

    ax = plt.axes(projection = '3d')

    DZ = 1 # extension of computational domain for 3D effects

    x = p[0,4:]
    y = p[1,4:]

    z1 = -0.5
    z2 = 0.5

    z = [z1 - DZ, z2 + DZ]

    diamond_1 = diamondsection(L,theta,z1)
    diamond_2 = diamondsection(L,theta,z2)


    ax.plot(diamond_1[0],diamond_1[1],diamond_1[2],'b.',markersize=3,label="Diamond")
    ax.plot(diamond_2[0],diamond_2[1],diamond_2[2],'b.',markersize=3)

    ax.plot(x,y,z[0],'ks',markersize=2.5,label="Domain")
    ax.plot(x,y,z[1],'ks',markersize=2.5)
    ax.plot(diamond[0],diamond[1],z[0],'ks',markersize=2.5)
    ax.plot(diamond[0],diamond[1],z[1],'ks',markersize=2.5)


    for i in range(4):
        ax.plot(diamondedges[0,i:i+2],diamondedges[1,i:i+2],z1,'b-')
        ax.plot(diamondedges[0,i:i+2],diamondedges[1,i:i+2],z2,'b-')

        ax.plot(diamondedges[0,i:i+2],diamondedges[1,i:i+2],z[0],'k-')
        ax.plot(diamondedges[0,i:i+2],diamondedges[1,i:i+2],z[1],'k-')

    for i in range(12):
        plt.plot(pedges[0,i:i+2],pedges[1,i:i+2],z[0],'k-')
        plt.plot(pedges[0,i:i+2],pedges[1,i:i+2],z[1],'k-')

    for i in range(4):
        plt.plot(inner1[0,2*i:2*i+2],inner1[1,2*i:2*i+2],z[0],'k-')
        plt.plot(inner1[0,2*i:2*i+2],inner1[1,2*i:2*i+2],z[1],'k-')

    for i in range(4):
        plt.plot(inner2[0,2*i:2*i+2],inner2[1,2*i:2*i+2],z[0],'k-')
        plt.plot(inner2[0,2*i:2*i+2],inner2[1,2*i:2*i+2],z[1],'k-')
    
        # 3D Edges
        N = 16

        vertices3d = np.zeros([3,2*N])
        for i in range(N):
            vertices3d[0,i] = p[0,i]
            vertices3d[1,i] = p[1,i]
            vertices3d[0,i+N] = p[0,i]
            vertices3d[1,i+N] = p[1,i]
            if i < 4:
                vertices3d[2,i] = z1
                vertices3d[2,i+N] = z2
            else:
                vertices3d[2,i] = z1 - DZ
                vertices3d[2,i+N] = z2 + DZ

    # rarrange for edges
        edges3d = np.zeros([3,2*N])
        j = 1
        for i in range(2*N):
            if i%2==0:
                edges3d[:,i] = vertices3d[:,i//2]
            else:
                edges3d[:,i] = vertices3d[:,i+N-j]
                j+=1

    for i in range(2*N):
        if i < 4:
            plt.plot(edges3d[0,2*i:2+2*i],edges3d[1,2*i:2+2*i],edges3d[2,2*i:2+2*i],'b')
        else:
            plt.plot(edges3d[0,2*i:2+2*i],edges3d[1,2*i:2+2*i],edges3d[2,2*i:2+2*i],'k')

    ax.set_title("Visualization of Diamond Airfoil Mesh")
    ax.grid()
    ax.legend()

    plt.show()