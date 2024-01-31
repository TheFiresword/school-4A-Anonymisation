import pandas as pd
import csv

# Specify the path where your CSV files are located
input_path = '../../User/resultat/'

# Ordre spécifique des fichiers
desired_order = [1, 2, 107, 98, 21, 5, 9, 6, 7, 8, 11, 17, 15, 44, 42, 16, 23, 32, 24, 37, 14, 25, 13, 26, 31, 28, 89, 29, 27, 30, 34, 38, 36, 39, 35, 54, 48, 41, 55, 49, 50, 43, 60, 51, 52, 62, 59, 63, 53, 65, 75, 18, 67, 68, 66, 70, 77, 84, 69, 72, 71, 73, 81, 78, 83, 87, 58, 4, 110]

# Générez la liste complète des fichiers CSV dans le répertoire spécifié
files = [f'../../User/resultat/sous_ensemble_{x}.csv_final.csv' for x in desired_order]

# Triez les fichiers en utilisant une expression régulière pour extraire l'ID

# # Initialisez une liste pour stocker les DataFrames individuels
dfs = []

# Parcourez chaque fichier CSV et ajoutez son DataFrame à la liste
for file in files:
    #print(file)
    df = pd.read_csv(file)
    dfs.append(df)

# Concaténez les DataFrames de la liste en un seul DataFrame
merged_data = pd.concat(dfs, ignore_index=True)
print(len(merged_data.columns))

output_path = 'finaltest'
# Save the merged data to a new CSV file
merged_data.to_csv(output_path, header=False, index=False)

print(f'Merged data saved to {output_path}')

with open("finaltest", 'r', newline='', encoding='utf-8') as csv_entree:
    lecteur_csv = csv.reader(csv_entree, delimiter=',')

    # Lire les lignes du fichier d'entrée et les écrire dans le fichier de sortie avec une tabulation comme délimiteur
    with open("finaltest2", 'w', newline='', encoding='utf-8') as tsv_sortie:
        ecrivain_tsv = csv.writer(tsv_sortie, delimiter='\t')
        for ligne in lecteur_csv:
            ecrivain_tsv.writerow(ligne)



# print("Conversion terminée avec succès.")