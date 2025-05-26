"""
Parametric Plot of Membrane Cross-Sections

This script:
1. Takes a DataFrame `trajectory_df` containing a sequence of Fourier coefficients.
2. Constructs r(θ) profiles and maps them to parametric (x, y) space.
3. Rotates the coordinate system so that the x-axis points up (now labeled z),
   and the y-axis becomes the horizontal axis (now labeled ρ).
4. Animates the evolution of the membrane profile with a light blue background.

Input:
- A DataFrame `trajectory_df` with columns: R, a0, a2, a4, b3, b5

Output:
- An MP4 animation titled "r_theta_parametric_rotated.mp4"
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter



###################################################################################################
from scipy.interpolate import griddata

# Load the full dataset
df = pd.read_csv("fourier_refined.csv")
df = df[df['E'] > 0].copy()

# Required coefficient columns
coeff_columns = ['a2', 'a4', 'b3', 'b5', 'E']
base_points = df[['R', 'a0']].values

trajectory_points = np.load("traj_points.npy")

# Interpolate each coefficient at trajectory points
interpolated_data = {
    'R': trajectory_points[:, 0],
    'a0': trajectory_points[:, 1],
}

for coeff in coeff_columns:
    interpolated_values = griddata(base_points, df[coeff].values, trajectory_points, method='linear')
    interpolated_data[coeff] = interpolated_values

# Create DataFrame
trajectory_df = pd.DataFrame(interpolated_data)
###################################################################################################



# Define θ
theta = np.linspace(0, 2 * np.pi, 500)

# Generate r(θ) profiles from Fourier coefficients
r_profiles = []
for _, row in trajectory_df.iterrows():
    a0, a2, a4 = row['a0'], row['a2'], row['a4']
    b3, b5 = row['b3'], row['b5']
    r_theta = a0 \
            + a2 * np.cos(2 * theta) \
            + a4 * np.cos(4 * theta) \
            + b3 * np.sin(3 * theta) \
            + b5 * np.sin(5 * theta)
    r_profiles.append(r_theta)
r_profiles = np.array(r_profiles)

# Convert to (ρ, z) = (y, x)
x_profiles = [r * np.cos(theta) for r in r_profiles]  # vertical axis (z)
y_profiles = [r * np.sin(theta) for r in r_profiles]  # horizontal axis (ρ)
z_profiles = x_profiles
rho_profiles = y_profiles
print(rho_profiles)

# Set up plot
# fig, ax = plt.subplots(figsize=(5, 5))
# fig.patch.set_facecolor('#e6f2ff')  # light blue background
# ax.set_facecolor('#e6f2ff')

# line, = ax.plot(rho_profiles[0], z_profiles[0])
# # ax.set_xlim(np.min(rho_profiles) * 1.1, np.max(rho_profiles) * 1.1)
# # ax.set_ylim(np.min(z_profiles) * 1.1, np.max(z_profiles) * 1.1)
# ax.set_xlim(-1.5,1.5)
# ax.set_ylim(-1.5,1.5)
# ax.set_xlabel(r'$\rho$', fontsize=14)
# ax.set_ylabel(r'$z$', fontsize=14)
# ax.set_title('Membrane Cross-Section (Rotated)', fontsize=14)

# # Update function
# def update(frame):
#     line.set_data(rho_profiles[frame], z_profiles[frame])
#     # ax.set_title(f'Step {frame + 1}', fontsize=12)
#     return line,

# # Animate
# ani = FuncAnimation(fig, update, frames=len(rho_profiles), blit=True)
# plt.close()

# # Save animation
# output_file = "r_theta_parametric_rotated.mp4"
# ani.save(output_file, writer=FFMpegWriter(fps=25, bitrate=3600))
# print(f"Animation saved to {output_file}")
