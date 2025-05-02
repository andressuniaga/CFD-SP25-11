from diamondmesh import *
#--------------------------------#
# For 3D Simulation
#--------------------------------#

def blockMeshDict(intro1,intro2,verts,blocks,edges,faces,pairs):
    f = open(r"Final Project\code\3D\blockMeshDict", "w")

    f.write(intro1+intro2+verts+blocks+edges+faces+pairs)

    f.close()

#--------------------------------#
#--------------------------------#
N = 16

L = 1.0
theta = 10.0 # degrees

DL = 1.0
DR = 1.5
H = 1.0
DZ = 1.0 # extension of computational domain for 3D effects


diamond = diamondsection(L,theta,0)
outlet,inlet,top,bott = facevertices(DR,DL,H,L,theta,0)

p = allvertices(diamond,outlet,inlet,top,bott)

intro1 = f"""// Diamond Airfoil Mesh Generation 3D
// Parameters:
// L (chord) = {L:.3}
// Theta (deflection angle)  =  {theta:.3}
// DL (fore)  =  {DL:.3}
// DR  (wake) =  {DR:.3}
// H  (top/bottom) = {H:.3}
// DZ (z-extension) = {DZ:.3}
""" 

intro2 =r"""
/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  7
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

convertToMeters 1;
"""

verts = """
vertices
(   
"""
z = 0.5
for i in range(4):
    vertex = f"     ({p[0,i]:.13e} {p[1,i]:4e} {-z:.13e}) // {i}\n"
    verts +=vertex

for i in range(4,N):
    vertex = f"     ({p[0,i]:.13e} {p[1,i]:4e} {-(z+DZ):.13e}) // {i}\n"
    verts +=vertex

for i in range(4):
    vertex = f"     ({p[0,i]:.13e} {p[1,i]:4e} {z:.13e}) // {i+N}\n"
    verts +=vertex


for i in range(4,N):
    vertex = f"     ({p[0,i]:.13e} {p[1,i]:4e} {z+DZ:.13e}) // {i+N}\n"
    verts +=vertex

verts = verts + ");"

blocks = """\n
blocks
(
    hex (0 4 5 6 16 20 21 22) (48 32 48) simpleGrading (1 1 1) // block 0
    hex (6 7 1 0 22 23 17 16) (96 32 48) simpleGrading (1 1 1) // block 1
    hex (7 8 2 1 23 24 18 17) (96 32 48) simpleGrading (1 1 1) // block 2
    hex (8 9 10 2 24 25 26 18) (24 32 48) simpleGrading (1 1 1) // block 3
    hex (2 10 11 12 18 26 27 28) (24 32 48) simpleGrading (1 1 1) // block 4
    hex (12 13 3 2 28 29 19 18) (96 32 48) simpleGrading (1 1 1) // block 5
    hex (13 14 0 3 29 30 16 19) (96 32 48) simpleGrading (1 1 1) // block 6
    hex (14 15 4 0 30 31 20 16) (48 32 48) simpleGrading (1 1 1) // block 7
); \n
"""

edges = """
edges
(
);
\n
"""

faces = """
boundary
(
    inlet
    {
        type patch;
        faces
        (
            (11 27 26 10)
            (10 26 25 9)
        );
    }
    outlet
    {
        type patch;
        faces
        (
            (5 21 20 4)
            (4 20 31 15)
        );
    }
    bottom
    {
        type symmetryPlane;
        faces
        (
            (11 27 28 12)
            (12 28 29 13)
            (13 29 30 14)
            (14 30 31 15)
        );
    }
    top
    {
        type symmetryPlane;
        faces
        (
            (9 25 24 8)
            (8 24 23 7)
            (7 23 22 6)
            (6 22 21 5)
        );
    }

    obstacle
    {
        type patch;
        faces
        (
            (0 16 17 1)
            (1 17 18 2)
            (2 18 19 3)
            (3 19 16 0)
        );
    }
);\n
"""

patchpairs = """
mergePatchPairs
(
);
"""

blockMeshDict(intro1,intro2,verts,blocks,edges,faces,patchpairs)