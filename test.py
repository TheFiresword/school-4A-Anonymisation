import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import folium
from folium.plugins import HeatMap
from ano_gps import *

################################################### test heatmap

# Charger votre DataFrame
# Assurez-vous d'avoir déjà lu votre DataFrame avec les colonnes "latitude" et "longitude"

df = bdd_to_df_init("../bdd/0riginal")

# Créer une carte centrée sur la première position
center_lat, center_lon = df.iloc[0]['latitude'], df.iloc[0]['longitude']
ma_carte = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Utiliser une HeatMap pour visualiser les concentrations
heat_data = [[row['latitude'], row['longitude']] for index, row in df.iterrows()]
HeatMap(heat_data).add_to(ma_carte)

# Afficher la carte
ma_carte.save("carte_positions.html")




################################################### test cluster

# df = bdd_to_df_init("../bdd/0riginal")

# # Sélectionner les colonnes nécessaires
# data = df[['latitude', 'longitude']]

# # Normaliser les données
# scaler = StandardScaler()
# scaled_data = scaler.fit_transform(data)

# # Appliquer l'algorithme DBSCAN pour détecter les clusters
# eps = 0.1  # rayon de voisinage
# min_samples = 100000  # nombre minimum de points dans un cluster
# dbscan = DBSCAN(eps=eps, min_samples=min_samples)
# df['cluster'] = dbscan.fit_predict(scaled_data)

# # Calculer les statistiques des clusters
# cluster_stats = df.groupby('cluster').size().reset_index(name='count')
# cluster_stats['percentage'] = (cluster_stats['count'] / len(df)) * 100
# cluster_stats = cluster_stats.sort_values(by='count', ascending=False)

# # Identifier les lieux principaux
# seuil_pourcentage = 1.0  # ajustez selon vos besoins
# lieux_principaux = cluster_stats[cluster_stats['percentage'] > seuil_pourcentage]

# print (lieux_principaux)