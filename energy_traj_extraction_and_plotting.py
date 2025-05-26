"""
Constant-Energy Trajectory Extractor and Plotter

This script:
1. Loads (R, a0, E) data from a CSV file representing a 2D energy landscape.
2. Builds a contour plot of E(R, a0).
3. Finds the nearest computed data point to a specified starting point.
4. Locates and plots the constant-energy contour (trajectory) passing through that energy.
5. Extracts the (R, a0) coordinates along that contour for further use.

Input:
- A CSV file named "fourier_refined.csv" with columns: R, a0, E

User Parameters:
- `start_point`: tuple (R, a0), the point through which the trajectory should pass

Output:
- A matplotlib plot of the contour map and trajectory
- A list of (R, a0) points along the constant-energy contour
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

# Load dataset
df = pd.read_csv("fourier_coefficients.csv")
df = df[df['E'] > 0].copy()
df = df[(df['a0'] >= 0.35) & (df['R'] <= 2.0) & (df['a0'] <= 1.4)]


# Build pivot table for plotting
pivot = df.pivot_table(index='a0', columns='R', values='E')
R_vals = pivot.columns.values
a0_vals = pivot.index.values
R_grid, a0_grid = np.meshgrid(R_vals, a0_vals)
E_grid = pivot.values

# Starting point (user-specified)
start_point = (1.2, 0.41)

# Use KDTree to find the closest data point
points = df[['R', 'a0']].values
tree = cKDTree(points)
_, idx = tree.query(start_point)
nearest_point = points[idx]
nearest_energy = df.iloc[idx]['E']

# Create filled contour plot
plt.figure(figsize=(8, 6))
contourf = plt.contourf(R_grid, a0_grid, E_grid, levels=50)
cbar = plt.colorbar(contourf)
cbar.set_label("Energy E")

# Extract constant-energy contour line
contours = plt.contour(R_grid, a0_grid, E_grid, levels=[nearest_energy], colors='magenta', linewidths=2)

# Find the contour path closest to the start point
closest_path = None
min_dist = float('inf')
for path in contours.get_paths():
    verts = path.vertices
    dist = np.min(np.linalg.norm(verts - start_point, axis=1))
    if dist < min_dist:
        min_dist = dist
        closest_path = verts

# Plot trajectory
if closest_path is not None:
    plt.plot(closest_path[:, 0], closest_path[:, 1], 'm-', label='Trajectory')
    plt.plot(*start_point, 'ko', label=f'Start (R={start_point[0]}, a₀={start_point[1]})')
else:
    print("Warning: No contour path found.")

plt.xlabel("Major Radius R")
plt.ylabel("Fourier Coefficient a₀")
plt.title("Constant Energy Trajectory from (R, a₀)")
plt.legend()
plt.tight_layout()
# plt.show()

# Output the contour trajectory for further use
trajectory_points = closest_path if closest_path is not None else np.empty((0, 2))
print("Extracted trajectory shape:", trajectory_points.shape)
# trajectory_points is a NumPy array of shape (N, 2) with columns [R, a₀]
np.save('traj_points',trajectory_points)
