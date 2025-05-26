"""
CSV Merger and Zero-Row Cleaner

This script:
1. Loads all CSV files in a directory matching a pattern.
2. Concatenates them into a single DataFrame.
3. Removes rows where all numeric values are zero (or just the 'E' column).
4. Saves the cleaned result to a new file.
"""

import pandas as pd
import glob

# Load all CSV files in the current directory matching pattern
csv_files = glob.glob("*.csv")  # Adjust pattern if needed

# Read and concatenate
df_all = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

# Option A: remove rows where *all* numeric entries are zero
df_cleaned = df_all.loc[~(df_all.select_dtypes(include='number') == 0).all(axis=1)]

# Option B: if you only want to filter out rows where 'E' == 0
# df_cleaned = df_all[df_all['E'] != 0]

# Save result
df_cleaned.to_csv("fourier_coefficients.csv", index=False)
print("Merged and cleaned CSV saved as 'fourier_coefficients.csv'")
