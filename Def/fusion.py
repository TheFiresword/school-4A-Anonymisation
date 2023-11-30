import pandas as pd
import glob

# Specify the path where your CSV files are located
input_path = '../../User/*final.csv'

# Use glob to get a list of all CSV files in the specified path
files = glob.glob(input_path)

# Initialize an empty DataFrame to store the merged data
dfs = []

# Parcourez chaque fichier CSV et ajoutez son DataFrame à la liste
for file in files:
    df = pd.read_csv(file)
    dfs.append(df)

# Concaténez les DataFrames de la liste en un seul DataFrame
merged_data = pd.concat(dfs, ignore_index=True)

# Specify the path where you want to save the merged CSV file
output_path = 'merged_data.csv'

dataframe = merged_data.iloc[1:]

# Save the merged data to a new CSV file
merged_data.to_csv(output_path, header=False, index=False)

print(f'Merged data saved to {output_path}')