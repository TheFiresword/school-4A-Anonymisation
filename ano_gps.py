import pandas as pd
import numpy as np
import math
from scipy.spatial import cKDTree

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
    df = df.round({'latitude' : precision, 'longitude' : precision}) # arrondit au millième si 3
    return df

def creer_grille (df, precision): # precision = ecart autour de la moyenne en degrés de longitude/latitude
    moyenne_latitude = df['latitude'].mean().round(3)
    moyenne_longitude = df['longitude'].mean().round(3)
    # dictionnaire des centres des carrés (long, lat) de 200x200 centrés sur la moyenne des coordonnées
    # cases (i,j) coorespondent aux coordonnées des cases dans la grille (-100<i<100 et -100<j<100)
    grille = {}
    for j in range (precision*100, -precision*100, precision*-1):
        for i in range (-precision*100, precision*100, precision*1):
            coord = (moyenne_longitude + i*precision/100, moyenne_latitude + j*precision/100) # dictionnaire de coordonnées
            grille[(i, j)] = coord
    return grille

def distance_euclidienne(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# def trouver_plus_proche(coordonnees, point_reference): # deux couples de coordonnées a comparer
#     plus_proche = None
#     distance_min = float('inf')  # initialisation à une valeur infinie
#     for coord in coordonnees:
#         distance = distance_euclidienne(point_reference, coord)
#         if distance < distance_min:
#             distance_min = distance
#             plus_proche = coord
#     return plus_proche

def ano_par_grille (df, precision):

    grille = creer_grille(df, precision)

    # convertir les coordonnées en un tableau NumPy
    df_coords = df[['longitude', 'latitude']].values
    grille_coords = np.array(list(grille.values()))

    # construir un arbre KD avec les coordonnées de la grille
    tree = cKDTree(grille_coords)

    # tTrouver les indices des points les plus proches pour chaque point dans le DataFrame
    indices_plus_proches = tree.query(df_coords)[1]

    # remplacez les valeurs dans le DataFrame avec les valeurs de la grille
    df[['longitude', 'latitude']] = grille_coords[indices_plus_proches]

    # df contient maintenant les nouvelles valeurs résultantes
    return df


def test (df, precision):
    grille = creer_grille(df, precision) # prend environ 1min

    for long in df['longitude']:
        for lat in df['latitude']:

            if (long-precision < df['longitude'].mean() < long+precision) and (lat-precision < df['latitude'].mean() < lat+precision):
                resultat = trouver_plus_proche(grille.values(), (long, lat))
                index_a_modifier = df[(df['longitude'] == long) & (df['latitude'] == lat)].index
                df.loc[index_a_modifier, 'longitude'] = resultat[0]
                df.loc[index_a_modifier, 'latitude'] = resultat[1]
    

    return df