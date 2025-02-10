import numpy as np
import matplotlib.pyplot as plt

U = r"OF1\data\cavity.original\0.5\U"

with open(U, 'r') as file:
    lines = file.readlines()

velocity_data = []
reading = False

for line in lines:
    line_stripped = line.strip()
    if reading:
        if line_stripped.startswith(")"):
            break
        if line_stripped.startswith("(") and line_stripped.endswith(")"):
            line_no_paren = line_stripped[1:-1]

            parts = line_no_paren.split()
            if len(parts) >= 2:
                u_val = float(parts[0])
                v_val = float(parts[1])
                velocity_data.append((u_val, v_val))
    if line_stripped.isdigit():
        reading = True

velocity_array = np.array(velocity_data)
print("Number of velocity points:", velocity_array.shape[0])

u_values = velocity_array[:, 0]
v_values = velocity_array[:, 1]

grid_size = (20, 20)
if velocity_array.shape[0] != grid_size[0] * grid_size[1]:
    raise ValueError("The number of data points does not match a 20x20 grid.")

u_grid = u_values.reshape(grid_size)
v_grid = v_values.reshape(grid_size)

x = np.linspace(0, 1, grid_size[0])
y = np.linspace(0, 1, grid_size[1])
X, Y = np.meshgrid(x, y)

plt.figure(figsize=(6, 5))
contour_u = plt.contour(X, Y, u_grid, levels=20, cmap="coolwarm")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Contour Line Plot of u-velocity (∼u)")
plt.colorbar(contour_u, label="u velocity")
plt.show()

# Contour line plot for v-velocity (vertical component)
plt.figure(figsize=(6, 5))
contour_v = plt.contour(X, Y, v_grid, levels=20, cmap="coolwarm")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Contour Line Plot of v-velocity (∼v)")
plt.colorbar(contour_v, label="v velocity")
plt.show()

center_index = grid_size[0] // 2
u_profile = u_grid[:, center_index]  # u at x = 0.5 for all y
v_profile = v_grid[:, center_index]  # v at x = 0.5 for all y
plt.figure(figsize=(6, 5))
plt.plot(u_profile, y, label="u/U", color="blue")
plt.plot(v_profile*100, y, label="v/U * 100", color="red")
plt.xlabel("Velocity")
plt.ylabel("y")
plt.title("Velocity Profiles at x = 0.5")
plt.legend()
plt.grid()
plt.show()