import math 

# ======== Generates the vertices ======== 
def circle_points(radius, z):
    """
    Returns a list of 8 coordinates around a circle of radius R (defines 8-15)
    """
    angles = [0, 45, 90, 135, 180, 225, 270, 315]
    coordinates = []
    for i in angles:
        theta = math.radians(i)   # measured in radians so convert
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        coordinates.append((x, y, z))
    return coordinates

def domain_boundary_points(Lf, Lw, H, R, z):
    """
    Returns 16 coordinates for the outer rectangle 
    """
    r_diag = R / math.sqrt(2)
    return [
        (Lw,     0.0,   z),   # 16
        ( Lw,    r_diag,z),   # 17 
        ( Lw,    H,     z),   # 18
        ( r_diag,H,     z),   # 19
        ( 0.0,   H,     z),   # 20
        (-r_diag,H,     z),   # 21
        (-Lf,    H,     z),   # 22
        (-Lf,    r_diag,z),   # 23
        (-Lf,    0.0,   z),   # 24
        (-Lf,   -r_diag,z),   # 25
        (-Lf,   -H,     z),   # 26
        (-r_diag,-H,    z),   # 27
        ( 0.0,   -H,    z),   # 28
        ( r_diag,-H,    z),   # 29
        ( Lw,    -H,    z),   # 30
        ( Lw,   -r_diag,z),   # 31
    ]

def create_vertices(Lf, Lw, H, R_inner, R, z):
    """
    Build all 64 vertex coordinates in correct order
    """
    # defining 0-31 points
    inner_circle = circle_points(R_inner, -z)   # could also put this in +z
    outer_circle = circle_points(R, -z)
    rectangle = domain_boundary_points(Lf, Lw, H, R, -z)

    # replicate but now at +z
    inner_circle_pos = circle_points(R_inner, z)
    outer_circle_pos = circle_points(R, z)
    rectangle_pos = domain_boundary_points(Lf, Lw, H, R, z)

    vertices = (inner_circle + outer_circle + rectangle + inner_circle_pos + outer_circle_pos + rectangle_pos)

    return vertices 

def write_vertices_block(vertices):
    lines = []
    lines.append("vertices\n(")
    for i, (x, y, z) in enumerate(vertices):
        lines.append(f"    ( {x:.8e} {y:.8e} {z:.8e} ) // {i}")
    lines.append(");")
    return "\n".join(lines)


# ======== Blocks ========
def define_blocks():
    # should stay the same, we will still have the same amount of blocks 
    blocks = []

    blocks.append({
        "verts": (0, 8, 9, 1, 32, 40, 41, 33),
        "cells": (10, 20, 1),
        "grading": (2.0, 1.0, 1.0)
    })
    blocks.append({
        "verts": (1, 9, 10, 2, 33, 41, 42, 34),
        "cells": (10, 20, 1),
        "grading": (2.0, 1.0, 1.0)
    })
    blocks.append({
        "verts": (2, 10, 11, 3, 34, 42, 43, 35),
        "cells": (10, 20, 1),
        "grading": (2.0, 1.0, 1.0)
    })
    blocks.append({
        "verts": (3, 11, 12, 4, 35, 43, 44, 36),
        "cells": (10, 20, 1),
        "grading": (2.0, 1.0, 1.0)
    })
    blocks.append({
        "verts": (4, 12, 13, 5, 36, 44, 45, 37),
        "cells": (10, 20, 1),
        "grading": (2.0, 1.0, 1.0)
    })
    blocks.append({
        "verts": (5, 13, 14, 6, 37, 45, 46, 38),
        "cells": (10, 20, 1),
        "grading": (2.0, 1.0, 1.0)
    })
    blocks.append({
        "verts": (6, 14, 15, 7, 38, 46, 47, 39),
        "cells": (10, 20, 1),
        "grading": (2.0, 1.0, 1.0)
    })
    blocks.append({
        "verts": (7, 15, 8, 0, 39, 47, 40, 32),
        "cells": (10, 20, 1),
        "grading": (2.0, 1.0, 1.0)
    })
    blocks.append({
        "verts": (8, 16, 17, 9, 40, 48, 49, 41),
        "cells": (30, 20, 1),
        "grading": (4.0, 1.0, 1.0)
    })
    blocks.append({
        "verts": (9, 17, 18, 19, 41, 49, 50, 51),
        "cells": (30, 30, 1),
        "grading": (4.0, 4.0, 1.0)
    })
    blocks.append({
        "verts": (10, 9, 19, 20, 42, 41, 51, 52),
        "cells": (20, 30, 1),
        "grading": (1.0, 4.0, 1.0)
    })
    blocks.append({
        "verts": (11, 10, 20, 21, 43, 42, 52, 53),
        "cells": (20, 30, 1),
        "grading": (1.0, 4.0, 1.0)
    })
    blocks.append({
        "verts": (23, 11, 21, 22, 55, 43, 53, 54),
        "cells": (15, 30, 1),
        "grading": (0.25, 4.0, 1.0)
    })
    blocks.append({
        "verts": (24, 12, 11, 23, 56, 44, 43, 55),
        "cells": (15, 20, 1),
        "grading": (0.25, 1.0, 1.0)
    })
    blocks.append({
        "verts": (25, 13, 12, 24, 57, 45, 44, 56),
        "cells": (15, 20, 1),
        "grading": (0.25, 1.0, 1.0)
    })
    blocks.append({
        "verts": (26, 27, 13, 25, 58, 59, 45, 57),
        "cells": (15, 30, 1),
        "grading": (0.25, 0.25, 1.0)
    })
    blocks.append({
        "verts": (27, 28, 14, 13, 59, 60, 46, 45),
        "cells": (20, 30, 1),
        "grading": (1.0, 0.25, 1.0)
    })
    blocks.append({
        "verts": (28, 29, 15, 14, 60, 61, 47, 46),
        "cells": (20, 30, 1),
        "grading": (1.0, 0.25, 1.0)
    })
    blocks.append({
        "verts": (29, 30, 31, 15, 61, 62, 63, 47),
        "cells": (30, 30, 1),
        "grading": (4.0, 0.25, 1.0)
    })
    blocks.append({
        "verts": (15, 31, 16, 8, 47, 63, 48, 40),
        "cells": (30, 20, 1),
        "grading": (4.0, 1.0, 1.0)
    })

    return blocks

def write_blocks_section(block_list):
    lines = []
    lines.append("blocks")
    lines.append("(")
    for i, block in enumerate(block_list):
        v = block["verts"]
        c = block["cells"]
        g = block["grading"]
        lines.append(f"    hex ({v[0]} {v[1]} {v[2]} {v[3]} {v[4]} {v[5]} {v[6]} {v[7]}) " +
                     f"({c[0]} {c[1]} {c[2]}) " +
                     f"simpleGrading ({g[0]} {g[1]} {g[2]}) // block {i}")
    lines.append(");")
    return "\n".join(lines)


# ======== Generates edges ========
def compute_arc_point(v1, v2):
    x1, y1, z1 = v1
    x2, y2, z2 = v2

    # compute angles of each vertex
    theta1 = math.atan2(y1, x1)
    theta2 = math.atan2(y2, x2)

    avg_cos = math.cos(theta1) + math.cos(theta2)
    avg_sin = math.sin(theta1) + math.sin(theta2)
    avg_theta = math.atan2(avg_sin, avg_cos)

    r1 = math.hypot(x1, y1)
    r2 = math.hypot(x2, y2)
    r = 0.5 * (r1 + r2)
    return (r * math.cos(avg_theta), r * math.sin(avg_theta), z1)

def write_edges_section(vertices):
    lines = []
    lines.append("edges")
    lines.append("(")

    # negative z inner circle (vertices 0-7)
    for i in range(8):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % 8]  
        arc_pt = compute_arc_point(v1, v2)
        lines.append(f"    arc {i} {(i+1)%8} ( {arc_pt[0]:.5e} {arc_pt[1]:.5e} {arc_pt[2]:.5e} )")

    # negative z outer circle
    for i in range(8, 16):
        v1 = vertices[i]
        v2 = vertices[8 + ((i - 8 + 1) % 8)]
        arc_pt = compute_arc_point(v1, v2)
        lines.append(f"    arc {i} {8 + ((i-8+1)%8)} ( {arc_pt[0]:.5e} {arc_pt[1]:.5e} {arc_pt[2]:.5e} )")
    
    # positive z inner circle
    for i in range(32, 40):
        v1 = vertices[i]
        v2 = vertices[32 + ((i - 32 + 1) % 8)]
        arc_pt = compute_arc_point(v1, v2)
        lines.append(f"    arc {i} {32 + ((i-32+1)%8)} ( {arc_pt[0]:.5e} {arc_pt[1]:.5e} {arc_pt[2]:.5e} )")

    # positive z outer circle
    for i in range(40, 48):
        v1 = vertices[i]
        v2 = vertices[40 + ((i - 40 + 1) % 8)]
        arc_pt = compute_arc_point(v1, v2)
        lines.append(f"    arc {i} {40 + ((i-40+1)%8)} ( {arc_pt[0]:.5e} {arc_pt[1]:.5e} {arc_pt[2]:.5e} )")
    
    lines.append(");")
    return "\n".join(lines)


# ======== Boundaries ========
def write_boundary_section():
    boundary = """boundary
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
    return boundary

def main():
    # define parameters
    Lf = 4.0
    Lw = 20.0
    H = 4.0
    R_inner = 0.5
    R = 1.0
    z = 0.05
    convertToMeters = 1.0

    vertices = create_vertices(Lf, Lw, H, R_inner, R, z)
    vertices_text = write_vertices_block(vertices)
    block_data_list = define_blocks()
    blocks_text = write_blocks_section(block_data_list)
    edges_text = write_edges_section(vertices)
    boundary_text = write_boundary_section()

    bmd = []
    bmd.append("FoamFile")
    bmd.append("{")
    bmd.append("    version  2.0;")
    bmd.append("    format   ascii;")
    bmd.append("    class    dictionary;")
    bmd.append("    object   blockMeshDict;")
    bmd.append("}")
    bmd.append("")
    bmd.append("convertToMeters {};".format(convertToMeters))
    bmd.append("")
    bmd.append(vertices_text)
    bmd.append("\n")
    bmd.append(blocks_text)
    bmd.append("\n")
    bmd.append(edges_text)
    bmd.append(boundary_text)

    complete_text = "\n".join(bmd)
    
    # write to a file here 
    with open("blockMeshDict_new", "w") as f:
        f.write(complete_text)
    print("blockMeshDict file has been generated")

if __name__ == "__main__":
    main()