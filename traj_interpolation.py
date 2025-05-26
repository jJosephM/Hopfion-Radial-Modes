"""
Fourier Coefficient Interpolator Along Constant-Energy Trajectory

This script:
1. Loads the full dataset with (R, a0, a2, a4, b3, b5, E) columns.
2. Assumes you have a NumPy array `trajectory_points` from a constant-energy contour (shape Nx2).
3. Interpolates the values of all other Fourier coefficients at each point on the trajectory.
Outputs the Pandas DataFrame containing interpolated values of: R, a0, a2, a4, b3, b5, E
"""

import pandas as pd
import numpy as np

df = pd.read_csv("fourier_refined.csv")
df = df[df['E'] > 0].copy()

#REQUIRED coefficient columns
coeff_columns = ['a2', 'a4', 'b3', 'b5', 'E']
base_points = df[['R', 'a0']].values

# Replace this with the actual trajectory_points if importing from another script
# For example, trajectory_points = np.load("trajectory.npy")
# Here we assume trajectory_points is already defined
# Example placeholder (remove and replace with real trajectory if needed):
# trajectory_points = np.array([[1.2, 0.85], [1.22, 0.86], ...])
trajectory_points = np.load("traj_points.npy")

#interpolate each coefficient at trajectory points
interpolated_data = {
    'R': trajectory_points[:, 0],
    'a0': trajectory_points[:, 1],
}

from scipy.interpolate import griddata
for coeff in coeff_columns:
    interpolated_values = griddata(base_points, df[coeff].values, trajectory_points, method='linear')
    interpolated_data[coeff] = interpolated_values

trajectory_df = pd.DataFrame(interpolated_data)

print(trajectory_df.head())

# trajectory_df.to_csv("interpolated_trajectory.csv", index=False)
