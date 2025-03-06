# Script for OF2 : blockmeshdict for Mesh B

mesh = "B"

# creates and writes blockMeshDict for Mesh B


#--------------------------------#

import numpy as np
from blockmeshvertices import *

#-------------------------------#

def blockMeshDict(intro1,intro2,verts,blocks,edges,faces):
    f = open("OF2\code\\blockMesh\\B\\blockMeshDict", "w")

    f.write(intro1+intro2+verts+blocks+edges+faces)

    f.close()


if __name__ == "__main__":
    # Parameters for Mesh B
    D = 1 # diameter of cylinder
    Lf = 10
    Lw = 30
    R = 1 
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
    z = -5e-01
    for i in range(N):
        vertex = f"     ({vertices[0,i]:.13e} {vertices[1,i]:4e} {z:.13e}) // {i}\n"
        verts +=vertex

    z = 5e-01
    for i in range(N):
        vertex = f"     ({vertices[0,i]:.13e} {vertices[1,i]:4e} {z:.13e}) // {i+N}\n"
        verts +=vertex

    verts = verts + ");"

    blocks = """\n
blocks
(
"""

    resX = 25
    resY = 50
    resZ = 1
    gradeX = 2.5
    gradeY = 1.5
    gradeZ = 1

    for i in range(N - (N//4+N//8)):
        if i < N//4-1:
            block = f"\
            // block {i}\n\
            hex ({i} {i+N//4} {i+N//4+1} {i+1} {i+N} {i+N//4+N} {i+N//4+N+1} {N+1}) ({resX} {resY} {resZ}) simpleGrading ({gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if i == N//4 - 1:
            block = f"\
            // block {i}\n\
            hex ({i} {i+N//4} {N//4} {i-(N//4-1)} {i+N} {i+N//4+N} {i+N//4+1} {N}) ({resX} {resY} {resZ}) simpleGrading ({gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if i == N//4:
            block = f"\
            // block {i}\n\
            hex ({i} {i+N//4} {i+N//4+1} {i+1} {i+N} {i+N//4+N} {i+N//4+1} {N+1+i}) ({resX+20} {resY} {resZ}) simpleGrading ({2*gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if i == N//4+1:
            block = f"\
            // block {i}\n\
            hex ({i} {i+N//4} {i+N//4+1} {i+N//4+2} {i+N} {i+N//4+N} {i+N//4+N+1} {i+N//4+N+2}) ({resX+20} {resY+10} {resZ}) simpleGrading ({2*gradeX:.4e} {4*gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if N//4+1<i<N//4+N//8:
            block = f"\
            // block {i}\n\
            hex ({i} {i-1} {i+N//4+1} {i+N//4+2} {i+N} {i+N-1} {i+N+N//4+1} {i+N//4+N+2}) ({resX+10} {resY+10} {resZ}) simpleGrading ({0.5*gradeX:.4e} {4*gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if i == N//4+N//8:
            block = f"\
            // block {i}\n\
            hex ({i+N//4+3} {i-1} {i+N//4+1} {i+N//4+2} {i+N//4+3+N} {i+N-1} {i+N//4+3+N-2} {i+N//4+3+N-1}) ({resX+5} {resY+10} {resZ}) simpleGrading ({1.5*gradeX:.4e} {4*gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if N//4+N//8 < i <= N//4+N//8+2:
            block = f"\
            // block {i}\n\
            hex ({i+N//4+3} {i-1} {i-2} {i+N//4+2} {i+N//4+3+N} {i+N-1} {i+N-2} {i+N//4+3+N-1}) ({resX+5} {resY} {resZ}) simpleGrading ({1.5*gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if i == N//4+N//8 + 3:
            block = f"\
            // block {i}\n\
            hex ({i+N//4+3} {i+N//4+N//8} {i-2} {i+N//4+2} {i+N//4+3+N} {i+N//4+N//8+N} {i+N-2} {i+N//4+2+N}) ({resX+5} {resY+10} {resZ}) simpleGrading ({1.5*gradeX:.4e} {2.5*gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if N//2 <= i <= N//2 + 1:
            block = f"\
            // block {i}\n\
            hex ({i+N//4+3} {i+N//4+N//8} {i-2} {i-3} {i+N//4+3+N} {i+N//4+N//8+N} {i+N-2} {i+N-3}) ({resX+10} {resY+10} {resZ}) simpleGrading ({gradeX:.4e} {2.5*gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if i == N//2 + 2:
            block = f"\
            // block {i}\n\
            hex ({i+N//4+N//8-1} {i+N//4+N//8} {i+N//4+N//8+1} {i-3} {i+N//4+N//8+N-1} {i+N//4+N//8+N} {i+N//4+N//8+N+1} {i+N-3}) ({resX+10} {resY+10} {resZ}) simpleGrading ({2*gradeX:.4e} {2.5*gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block
        if i == N - (N//4+N//8) - 1:
            block = f"\
            // block {i}\n\
            hex ({i-N//8} {i+N//4+N//8} {i-N//8+1} {i-N//8-N//4+1} {i+N-N//8} {i+N + N//8 + N//4} {i+N-N//8+1} {i+N-N//8-N//4+1}) ({resX+10} {resY} {resZ}) simpleGrading ({2*gradeX:.4e} {gradeY:.4e} {gradeZ:.1e})\n\n"
            blocks+=block

    blocks = blocks + ");\n"

    # NOTE: Arcs and Faces from example given shall remain the same given D,R = 1 and N=32

    arcs = """
edges
(

arc 0 1 ( 4.61940e-01  1.91342e-01 -5.00000e-02)
arc 8 9 ( 9.23880e-01  3.82683e-01 -5.00000e-02)
arc 32 33 ( 4.61940e-01  1.91342e-01  5.00000e-02)
arc 40 41 ( 9.23880e-01  3.82683e-01  5.00000e-02)
arc 1 2 ( 1.91342e-01  4.61940e-01 -5.00000e-02)
arc 9 10 ( 3.82683e-01  9.23880e-01 -5.00000e-02)
arc 33 34 ( 1.91342e-01  4.61940e-01  5.00000e-02)
arc 41 42 ( 3.82683e-01  9.23880e-01  5.00000e-02)
arc 2 3 (-1.91342e-01  4.61940e-01 -5.00000e-02)
arc 10 11 (-3.82683e-01  9.23880e-01 -5.00000e-02)
arc 34 35 (-1.91342e-01  4.61940e-01  5.00000e-02)
arc 42 43 (-3.82683e-01  9.23880e-01  5.00000e-02)
arc 3 4 (-4.61940e-01  1.91342e-01 -5.00000e-02)
arc 11 12 (-9.23880e-01  3.82683e-01 -5.00000e-02)
arc 35 36 (-4.61940e-01  1.91342e-01  5.00000e-02)
arc 43 44 (-9.23880e-01  3.82683e-01  5.00000e-02)
arc 4 5 (-4.61940e-01 -1.91342e-01 -5.00000e-02)
arc 12 13 (-9.23880e-01 -3.82683e-01 -5.00000e-02)
arc 36 37 (-4.61940e-01 -1.91342e-01  5.00000e-02)
arc 44 45 (-9.23880e-01 -3.82683e-01  5.00000e-02)
arc 5 6 (-1.91342e-01 -4.61940e-01 -5.00000e-02)
arc 13 14 (-3.82683e-01 -9.23880e-01 -5.00000e-02)
arc 37 38 (-1.91342e-01 -4.61940e-01  5.00000e-02)
arc 45 46 (-3.82683e-01 -9.23880e-01  5.00000e-02)
arc 6 7 ( 1.91342e-01 -4.61940e-01 -5.00000e-02)
arc 14 15 ( 3.82683e-01 -9.23880e-01 -5.00000e-02)
arc 38 39 ( 1.91342e-01 -4.61940e-01  5.00000e-02)
arc 46 47 ( 3.82683e-01 -9.23880e-01  5.00000e-02)
arc 7 0 ( 4.61940e-01 -1.91342e-01 -5.00000e-02)
arc 15 8 ( 9.23880e-01 -3.82683e-01 -5.00000e-02)
arc 39 32 ( 4.61940e-01 -1.91342e-01  5.00000e-02)
arc 47 40 ( 9.23880e-01 -3.82683e-01  5.00000e-02)

);\n"""

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