import folium
from folium.plugins import HeatMap
import pandas as pd


donnees_csv = pd.read_csv('0riginal.csv')
# Récupérer les valeurs uniques de la colonne "id"
ids_uniques = donnees_csv['id_x'].unique()

for i in ids_uniques:
    # Charger les données depuis le fichier CSV

    
    donnees_gps = pd.read_csv(f'User\sous_ensemble_{i}.csv')

    nom_column = ["id_x","date", "longitude", "latitude"]
    donnees_gps.columns = nom_column

    # Créer une carte centrée sur une position de départ (moyenne des coordonnées GPS)
    ma_carte = folium.Map(location=[45.7, 4.8], zoom_start=12)

    # Ajouter un heatmap basé sur les coordonnées GPS du fichier CSV
    HeatMap(donnees_gps[['latitude', 'longitude']].values).add_to(ma_carte)

    # Enregistrer la carte dans un fichier HTML
    ma_carte.save(f'Carte\heatmap_carte{i}.html')
