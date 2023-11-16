import pandas as pd
import numpy as np
import math

def bdd_to_df_init (fichier):
    df = pd.read_csv(fichier, delimiter= '\t')
    df.columns = ["id","date", "longitude", "latitude"]
    return df

def df_to_csv (df, nom_csv):
    df.to_csv(nom_csv, index=False)

def bruiter_positions_gps (df):
    noise = np.random.uniform(-0.001, 0.001, size=len(df))
    df['latitude'] = df['latitude'] + noise
    df['longitude'] = df['longitude'] + noise
    return df

def arrondir_positions_gps (df, precision):
    df = df.round({'latitude' : precision, 'longitude' : precision}) # arrondit au millième
    return df

# def recentrer_positions_gps(df, ecart_moyenne): 

#     moyenne_latitude = df['latitude'].mean()    # 45,78
#     moyenne_longitude = df['longitude'].mean()  # 4,879
#     min_lat = moyenne_latitude - ecart_moyenne
#     max_lat = moyenne_latitude + ecart_moyenne
#     min_lon = moyenne_longitude - ecart_moyenne
#     max_lon = moyenne_longitude + ecart_moyenne
    
#     lat_moins = len(df[df['latitude'] < min_lat])
#     lat_plus = len(df[df['latitude'] > max_lat])
#     long_moins = len(df[df['longitude'] < min_lon])
#     long_plus = len([df['longitude'] > max_lon])
#     nb_lignes_hors_zone = lat_moins + lat_plus + long_moins + long_plus
    
#     print ("nb de lignes hors zone : ", nb_lignes_hors_zone)

#     # a finir
#     # effacer les lignes en dehors de la zone


def creer_grille (df, precision): # precision = ecart autour de la moyenne en degrés de longitude/latitude
    moyenne_latitude = df['latitude'].mean().round(2)    # 45,78
    moyenne_longitude = df['longitude'].mean().round(2)  # 4,87
    # dictionnaire des centres des carrés (long, lat) de 200x200 centrés sur la moyenne des coordonnées
    # cases (i,j) coorespondent aux coordonnées des cases dans la grille (-100<i<100 et -100<j<100)
    grille = {}
    for j in range (precision*10, -precision*11, precision*-1):
        for i in range (-precision*10, precision*11, precision*1):
            coord = (moyenne_longitude + i*precision/100, moyenne_latitude + j*precision/100) #dictionnaire de coordonnées
            grille[(i, j)] = coord
    
    return grille

def distance_euclidienne(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def trouver_plus_proche(coordonnees, point_reference): #deux couples de coordonnées a comparer
    plus_proche = None
    distance_min = float('inf')  # Initialisation à une valeur infinie

    for coord in coordonnees:
        distance = distance_euclidienne(point_reference, coord)
        if distance < distance_min:
            distance_min = distance
            plus_proche = coord

    return plus_proche

def ano_par_grille (df, precision):

    grille = creer_grille(df, precision)

    for long in df['longitude']:
        for lat in df['latitude']:

            if (long-precision < df['longitude'].mean() < long+precision) and (lat-precision < df['latitude'].mean() < lat+precision):
                resultat = trouver_plus_proche(grille.values(), (long, lat))
                index_a_modifier = df[(df['longitude'] == long) & (df['latitude'] == lat)].index
                df.loc[index_a_modifier, 'longitude'] = resultat[0]
                df.loc[index_a_modifier, 'latitude'] = resultat[1]
    
    return df







# mettre les id en random