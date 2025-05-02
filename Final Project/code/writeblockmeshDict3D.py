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

b = 1.0


diamond = diamondsection(L,theta,0)
outlet,inlet,top,bott = facevertices(DR,DL,H,L,theta,0)

p = allvertices(diamond,outlet,inlet,top,bott)

intro1 = f"""// Diamond Airfoil Mesh Generation 3D
// Parameters:
// L (chord) = {L:.3}
// b (span) = {b:.3}
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
z = b/2
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
    hex (0 1 2 3 16 17 18 19) (96 32 48) simpleGrading (1 1 1) // diamond block
    hex (11 12 8 9 27 28 24 25) (48 48 72) simpleGrading (1 1 1) // fore domain block
    hex (12 14 6 8 28 30 22 24) (120 48 72) simpleGrading (1 1 1) // mid domain block
    hex (14 15 5 6 30 31 21 22) (72 48 72) simpleGrading (1 1 1) // aft domain block

    // Feel free to play with the number of points Nx, Ny, Nz along axes of blocks for refinement
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
            (11 27 25 9)
        );
    }

    outlet
    {
        type patch;
        faces
        (
            (15 31 21 5)
        );
    }

    bottom
    {
        type symmetryPlane;
        faces
        (
            (11 27 28 12)
            (12 28 30 14)
            (14 30 31 15)
        );
    }

    top
    {
        type symmetryPlane;
        faces
        (
            (9 25 24 8)
            (8 24 22 6)
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