"""
Energy Contour Plot Generator

This script loads the CSV file containing the precomputed values of:
- Major radius R
- First Fourier coefficient a0
- Energy E

It creates a 2D contour plot of the energy E as a function of R and a0.
The script:
1. Loads and filters the data within a specified R–a0 range (optional).
2. Constructs a pivot table for interpolation.
3. Uses matplotlib to generate and display a contour plot.

Input:
- A CSV file with columns: R, a0, E (and optionally other Fourier coefficients)

Output:
- A contour plot of E(R, a0) rendered in a matplotlib window.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("fourier_coefficients.csv")  # Replace with your filename if different

# Optional: filter to a specific region
# df = df[(df['R'] >= 1.0) & (df['R'] <= 1.5) & (df['a0'] >= 0.6) & (df['a0'] <= 1.0)]
df = df[(df['a0'] >= 0.4) & (df['R'] <= 2.0) & (df['a0'] <= 1.4)]

# Pivot table for contour plotting
pivot = df.pivot_table(index='a0', columns='R', values='E')

# Create meshgrid
R_vals = pivot.columns.values
a0_vals = pivot.index.values
R_grid, a0_grid = np.meshgrid(R_vals, a0_vals)
E_grid = pivot.values

plt.figure(figsize=(8, 6))
contour = plt.contourf(R_grid, a0_grid, E_grid, levels=50)
cbar = plt.colorbar(contour)
cbar.set_label('Energy E')

plt.xlabel('Major Radius R')
plt.ylabel('Fourier Coefficient $a_0$')
# plt.title('Energy Contour Plot')
plt.tight_layout()
plt.show()
