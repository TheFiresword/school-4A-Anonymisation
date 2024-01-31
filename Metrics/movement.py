import pandas as pd
from geopy.distance import geodesic

def cut_by_id(file):

    df = pd.read_csv(file)
    columns = ["id_x", "date", "longitude", "latitude" ]
    df.columns = columns
    # Récupérer les valeurs uniques de la colonne "id"
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.to_period('W')
    
    df['week'] = df['week'].dt.week
    ids_uniques = df[['id_x',"week"]].drop_duplicates() 
    
    resultat_liste = ids_uniques.values.tolist()
    return resultat_liste


def calcul_distance(file):
    df = pd.read_csv(file)
    columns = ["id_x", "date", "longitude", "latitude" ]
    df.columns = columns
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.to_period('W')
    df['week'] = df['week'].dt.week

    ids_uniques = cut_by_id(file)
    dict_distance_total = {}

    for items in ids_uniques:
        id, week =  items
        subset = df[(df['id_x'] == id) & (df['week'] == week)].copy()

        subset.loc[:, 'coordinates'] = list(zip(subset['latitude'], subset['longitude']))
    
        # Ajouter une colonne pour la date uniquement (ignorer l'heure)
        subset.loc[:,'date'] = pd.to_datetime(subset['date']).dt.date
        # Initialiser un dictionnaire pour stocker la distance totale par jour
        distance_par_jour = {}
        

        # Parcourir chaque jour unique dans le DataFrame
        for date in subset['date'].unique():
            # Sélectionner les coordonnées GPS pour ce jour
            coords_jour = subset[subset['date'] == date]['coordinates'].tolist()

            # Calculer la distance totale parcourue pour ce jour
            distance_totale_jour = sum(geodesic(coords_jour[i], coords_jour[i+1]).kilometers for i in range(len(coords_jour)-1))

            # Stocker la distance totale pour ce jour dans le dictionnaire
            distance_par_jour[date] = distance_totale_jour

        # Calculer la distance totale sur la semaine
        distance_totale_semaine = sum(distance_par_jour.values())
        dict_distance_total[(id, week)] = distance_totale_semaine
        print("ID", id, "SEMAINE", week, "Distance", distance_totale_semaine)

    return dict_distance_total
    
def temoin(dict):

    max = 0
    mon = 0
    distance = dict
    tot = 0
    
    for key in distance.keys():
        if distance[key] > max:
            max = distance[key]

        if distance[key] < min:
            min = distance[min]
        tot += distance[key]

    moy = tot/len(distance)

    print(min)
    print(max)
    print(moy)

    return(min, max, moy)


def utilite(fichierOriginal, fichieranonym):

    Origin = calcul_distance("(fichierOriginal")
    (min0, max0, moy0) = temoin(Origin)
    Anonym = calcul_distance("fichieranonym")
    (minA, maxA, moyA) = temoin(Anonym)

    if minA > min0:
        min = min0/minA
    else:
        min = minA/min0

    if moyA > moy0:
        moy = moy0/moyA
    else:
        moy = moyA/moy

    if maxA > max0:
        maxi = max0/maxA
    else:
        maxi = maxA/max0

    score = (min+maxi+moy)/3
    assert 0<=score<=1
    return score


utilite("/Users/maelp/Documents/Projet Secu/Anonymisation/Metrics/0riginal.csv", "/Users/maelp/Documents/Projet Secu/Anonymisation/Def/finalnoise2")