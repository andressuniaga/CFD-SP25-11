# Script for OF2 : blockmeshdict for Mesh A

mesh = "A"

# creates and writes blockMeshDict for Mesh A


#--------------------------------#

import numpy as np
from blockmeshvertices import *

#-------------------------------#

def blockMeshDict(intro1,intro2,verts,blocks,edges,faces):
    f = open("OF2\code\\blockMesh\\A\\blockMeshDict", "w")

    f.write(intro1+intro2+verts+blocks+edges+faces)

    f.close()


if __name__ == "__main__":
    # Parameters for Mesh A
    D = 1 # diameter of cylinder
    Lf = 4
    Lw = 6
    R = 1.0 
    H = 4
    
    N = 32 # NOTE: Treat this as a CONST variable
    # DO NOT CHANGE; this blockMeshDict creation does not adapt to higher number of vertices
    # Due to time constraints with this assignment we stick with N=32 vertices for our simulations
    # However, resolution can be played with in 'blocks' section!

    inner,outer = arcvertices(D,R)
    top,bottom,inlet,outlet = walls(Lf,Lw,H,outer)
    vertices = blockmesh_2D(inner,outer,inlet,top,outlet,bottom)

    intro1 = f""" 
// Mesh {mesh} Generation
// Parameters:
// D (diameter) = {D:.3e}
// Lf (fore)  =  {Lf:.3e}
// Lw (wake)  =  {Lw:.3e}
// R  (outer) =  {R:.3e}
// H  (top/bottom) = {H:.3e}
    """

    intro2 = """
FoamFile
{
    version  2.0;
    format   ascii;
    class    dictionary;
    object   blockMeshDict;
}

convertToMeters 1.0;
    """

    verts = """
vertices
(   
"""
    z = -5e-02
    for i in range(N):
        vertex = f"     ({vertices[0,i]:.13e} {vertices[1,i]:4e} {z:.13e}) // {i}\n"
        verts +=vertex

    for i in range(N):
        vertex = f"     ({vertices[0,i]:.13e} {vertices[1,i]:4e} {-z:.13e}) // {i+N}\n"
        verts +=vertex

    verts = verts + ");"

    blocks = """\n
blocks
(
"""

    resX = 10
    resY = 20
    resZ = 1
    gradeX = 2
    gradeY = 1
    gradeZ = 1

    for i in range(N - (N//4+N//8)):
        if i < N//4-1:
            block = f"\
            // block {i}\n\
            hex ({i} {i+N//4} {i+N//4+1} {i+1} {i+N} {i+N//4+N} {i+N//4+N+1} {N+i+1}) ({resX} {resY} {resZ}) simpleGrading ({gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if i == N//4 - 1:
            block = f"\
            // block {i}\n\
            hex ({i} {i+N//4} {N//4} {i-(N//4-1)} {i+N} {i+N//4+N} {i+N+1} {N}) ({resX} {resY} {resZ}) simpleGrading ({gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if i == N//4:
            block = f"\
            // block {i}\n\
            hex ({i} {i+N//4} {i+N//4+1} {i+1} {i+N} {i+N//4+N} {i+N+N//4+1} {N+1+i}) ({resX+20} {resY} {resZ}) simpleGrading ({gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if i == N//4+1:
            block = f"\
            // block {i}\n\
            hex ({i} {i+N//4} {i+N//4+1} {i+N//4+2} {i+N} {i+N//4+N} {i+N//4+N+1} {i+N//4+N+2}) ({resX+20} {resY+10} {resZ}) simpleGrading ({gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if N//4+1<i<N//4+N//8:
            block = f"\
            // block {i}\n\
            hex ({i} {i-1} {i+N//4+1} {i+N//4+2} {i+N} {i+N-1} {i+N+N//4+1} {i+N//4+N+2}) ({resX+10} {resY+10} {resZ}) simpleGrading ({gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if i == N//4+N//8:
            block = f"\
            // block {i}\n\
            hex ({i+N//4+3} {i-1} {i+N//4+1} {i+N//4+2} {i+N//4+3+N} {i+N-1} {i+N//4+3+N-2} {i+N//4+3+N-1}) ({resX+5} {resY+10} {resZ}) simpleGrading ({gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if N//4+N//8 < i <= N//4+N//8+2:
            block = f"\
            // block {i}\n\
            hex ({i+N//4+3} {i-1} {i-2} {i+N//4+2} {i+N//4+3+N} {i+N-1} {i+N-2} {i+N//4+3+N-1}) ({resX+5} {resY} {resZ}) simpleGrading ({gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if i == N//4+N//8 + 3:
            block = f"\
            // block {i}\n\
            hex ({i+N//4+3} {i+N//4+N//8} {i-2} {i+N//4+2} {i+N//4+3+N} {i+N//4+N//8+N} {i+N-2} {i+N//4+2+N}) ({resX+5} {resY+10} {resZ}) simpleGrading ({gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if N//2 <= i <= N//2 + 1:
            block = f"\
            // block {i}\n\
            hex ({i+N//4+3} {i+N//4+N//8} {i-2} {i-3} {i+N//4+3+N} {i+N//4+N//8+N} {i+N-2} {i+N-3}) ({resX+10} {resY+10} {resZ}) simpleGrading ({gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if i == N//2 + 2:
            block = f"\
            // block {i}\n\
            hex ({i+N//4+N//8-1} {i+N//4+N//8} {i+N//4+N//8+1} {i-3} {i+N//4+N//8+N-1} {i+N//4+N//8+N} {i+N//4+N//8+N+1} {i+N-3}) ({resX+20} {resY+10} {resZ}) simpleGrading ({gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if i == N - (N//4+N//8) - 1:
            block = f"\
            // block {i}\n\
            hex ({i-N//8} {i+N//4+N//8} {i-N//8+1} {i-N//8-N//4+1} {i+N-N//8} {i+N + N//8 + N//4} {i+N-N//8+1} {i+N-N//8-N//4+1}) ({resX+10} {resY} {resZ}) simpleGrading ({gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block

    blocks = blocks + ");\n"

    # NOTE: Arcs and Faces from example given shall remain the same given D,R = 1 and N=32

    midpoints1 = arcmidpoints(z,vertices,D,R)
    midpoints2 = arcmidpoints(-z,vertices,D,R)
    [a,b]=np.shape(midpoints1)

    arcindex1 = np.zeros([2,b])
    arcindex2 = np.zeros([2,b])
    for i in range(b):
        arcindex1[0,i] = i
        arcindex2[0,i] = i+N
        if i != b-1:
            arcindex1[1,i] = i+1
            arcindex2[1,i] = i+1+N
        else:
            arcindex1[1,i] = b/2
            arcindex2[1,i] = b/2+N

    arcindex1[1,N//4-1] = arcindex1[0,0]
    arcindex2[1,N//4-1] = arcindex2[0,0]
    
    arcs = """
edges
(
"""
    for i in range(b):
        arcs += f"arc {int(arcindex1[0,i])} {int(arcindex1[1,i])} ( {midpoints1[0,i]:.5e} {midpoints1[1,i]:.5e} {midpoints1[2,i]:.5e})\n"

    for i in range(b):
        arcs += f"arc {int(arcindex2[0,i])} {int(arcindex2[1,i])} ( {midpoints2[0,i]:.5e} {midpoints2[1,i]:.5e} {midpoints2[2,i]:.5e})\n"

    arcs = arcs +");\n"

    faces = """
boundary
(

  inlet
  {
      type patch;
      faces
      (
         (22 54 55 23)
         (23 55 56 24)
         (24 56 57 25)
         (25 57 58 26)
      );
  }

  outlet
  {
      type patch;
      faces
      (
         (18 50 49 17)
         (17 49 48 16)
         (16 48 63 31)
         (31 63 62 30)
      );
  }

  cylinder
  {
      type wall;
      faces
      (
         (0 32 33 1)
         (1 33 34 2)
         (2 34 35 3)
         (3 35 36 4)
         (4 36 37 5)
         (5 37 38 6)
         (6 38 39 7)
         (7 39 32 0)
      );
  }

  top
  {
      type symmetryPlane;
      faces
      (
         (22 54 53 21)
         (21 53 52 20)
         (20 52 51 19)
         (19 51 50 18)
      );
  }

  bottom
  {
      type symmetryPlane;
      faces
      (
         (26 58 59 27)
         (27 59 60 28)
         (28 60 61 29)
         (29 61 62 30)
      );
  }

);
    """


    blockMeshDict(intro1,intro2,verts,blocks,arcs,faces)