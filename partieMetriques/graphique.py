from typing import List, Tuple, Dict
import folium
from folium.plugins import HeatMap
import pandas as pd
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def draw_map(id:int, df : pd.DataFrame, name : str, interestPoints : Dict[str, Tuple[float, float]] = {}):
    donnees_id = df[df['id']==id]
    # Créer une carte centrée sur une position de départ (moyenne des coordonnées GPS)
    ma_carte = folium.Map(location=[45.7, 4.8], zoom_start=12)
    # Ajouter un heatmap basé sur les coordonnées GPS du fichier CSV
    HeatMap(donnees_id[['lat', 'long']].values).add_to(ma_carte)
    for label in interestPoints :
        marqueur = folium.Marker(interestPoints[label], popup=label)
        marqueur.add_to(ma_carte)
    
    # Enregistrer la carte dans un fichier HTML
    ma_carte.save(name+'.html')
    

def draw_shape(df : pd.DataFrame):
    '''
    Fonction : Visualiser les données facilement
    , x_axis: str, y_axis: str, z_axis
    '''

    longitudes = df['long']
    latitudes = df['lat']
    
    plt.figure(figsize=(10, 6))
    sc = plt.scatter(longitudes, latitudes, marker='o')
    plt.title("Frontière de Lyon ")
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)