import pandas as pd

# Charger le fichier CSV
victim = pd.read_csv("0riginal", delimiter='\t')
nom_column = ["id_x","date", "longitude", "latitude"]
victim.columns = nom_column
victim.to_csv("0riginal.csv", index=False)
donnees_csv = pd.read_csv('0riginal.csv')
# Récupérer les valeurs uniques de la colonne "id"
ids_uniques = donnees_csv['id_x'].unique()

# Diviser le fichier en fonction de chaque ID et enregistrer les sous-ensembles dans des fichiers CSV
for identifiant in ids_uniques:
    subset = donnees_csv[donnees_csv['id_x'] == identifiant]
    nom_fichier = f'sous_ensemble_{identifiant}.csv'
    subset.to_csv(nom_fichier, index=False)
    print(f'Fichier {nom_fichier} créé avec succès.')

