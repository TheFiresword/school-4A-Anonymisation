import pandas as pd
import numpy as np
import math
from scipy.spatial import cKDTree

def bdd_to_df_init (fichier):
    df = pd.read_csv(fichier, delimiter= '\t', header=None)
    df.columns = ["id","date", "longitude", "latitude"]
    df['date'] = pd.to_datetime(df['date'])
    return df

def df_to_csv (df, nom_csv):
    df.to_csv(nom_csv, sep="\t", index=False, header=False)

def bruiter_positions_gps(df, arrondi, indices_a_bruiter=None):
    if indices_a_bruiter is None:
        indices_a_bruiter = df.index  # Bruiter toutes les lignes si aucun indice spécifié
    noise = np.random.uniform(-arrondi, arrondi, size=len(indices_a_bruiter))
    df.loc[indices_a_bruiter, 'latitude'] += noise
    df.loc[indices_a_bruiter, 'longitude'] += noise
    return df

def arrondir_positions_gps (df, precision):
    df = df.round({'latitude' : precision, 'longitude' : precision}) # arrondit au millième si 3
    return df

def creer_grille (latitude, longitude, precision): # precision = ecart autour de la moyenne en degrés de longitude/latitude
    # dictionnaire des centres des carrés (long, lat) de 200x200 centrés sur la moyenne des coordonnées
    # cases (i,j) coorespondent aux coordonnées des cases dans la grille (-100<i<100 et -100<j<100)
    grille = {}
    for j in range (precision*100, -precision*100, precision*-1):
        for i in range (-precision*100, precision*100, precision*1):
            coord = (longitude + i*precision/100, latitude + j*precision/100) # dictionnaire de coordonnées
            grille[(i, j)] = coord
    return grille

def distance_euclidienne(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def ano_par_grille (df, precision):

    coordonnees = [
    (45.7499, 4.1563), # Lyon, France (moyenne sur les données)
    (48.8566, 2.3522),  # Paris, France
    (40.7128, -74.0060),  # New York, USA
    (51.5074, -0.1278),  # Londres, Royaume-Uni
    ]

    # bruitage de +/- 0.0001 pour avoir quelques "erreurs"
    df = bruiter_positions_gps(df, 0.0001)
    df_coords = df[['longitude', 'latitude']].values

    indices_non_grilles = set(df.index)


    for coordonnee in coordonnees:
        latitude, longitude = coordonnee

        # convertir les coordonnées en un tableau NumPy
        grille = creer_grille (latitude, longitude, precision)
        grille_coords = np.array(list(grille.values()))

        # construir un arbre KD avec les coordonnées de la grille
        tree = cKDTree(grille_coords)

        # identifier les indices des lignes à modifier en fonction de la condition
        condition_colonne = (df['longitude'] >= longitude-precision) & (df['longitude'] <= longitude+precision) & (df['latitude'] >= latitude-precision) & (df['latitude'] <= latitude+precision)
        indices_a_modifier = df.index[condition_colonne]

        # retirer les indices modifiés de indices_non_grilles
        indices_non_grilles -= set(indices_a_modifier)

        # utiliser l'arbre KD pour trouver les voisins les plus proches uniquement pour les indices identifiés
        indices_plus_proches = tree.query(df_coords[indices_a_modifier])[1]

        # remplacer les valeurs uniquement pour les indices identifiés dans votre DataFrame
        df.loc[indices_a_modifier, ['longitude', 'latitude']] = grille_coords[indices_plus_proches]

    indices_non_grilles_liste = list(indices_non_grilles)

    df = bruiter_positions_gps(df, 0.5, indices_non_grilles_liste)

    df = arrondir_positions_gps (df, 4)
    # df contient maintenant les nouvelles valeurs résultantes uniquement pour les lignes qui satisfont la condition

    return df




