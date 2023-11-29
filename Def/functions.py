import pandas as pd
import numpy as np
import names
import threading


def CreationCarte(CentreLat, CentreLong, echelle, Nbdivison):

    lat_mean = CentreLat
    lont_mean = CentreLong

    carte = {}

    case_count = 1

    divisions_lat = Nbdivison
    divisions_lont = Nbdivison

    # Initialisation des valeurs de latitude et de longitude
    latitude_min = lat_mean - echelle*divisions_lat/2
    latitude_max = lat_mean - echelle*divisions_lont/2 + echelle
    longitude_min = lont_mean - echelle*divisions_lont/2 
    longitude_max = lont_mean - echelle*divisions_lont/2 + echelle

    # Création du dictionnaire pour les 4000 cases
    for lat_div in range(divisions_lat):

        latitude_min = latitude_min + echelle
        latitude_max = latitude_max + echelle
        longitude_min = lont_mean - echelle*divisions_lont/2 
        longitude_max = lont_mean - echelle*divisions_lont/2 + echelle
        for lon_div in range(divisions_lont):
            # Calcul des valeurs de latitude et de longitude pour chaque case

            longitude_min = longitude_min + echelle
            longitude_max = longitude_max + echelle
            # Création de la clé de la case
            case_key = f"Case {case_count}"

            # Création de l'ensemble de données associé à la clé
            data_set = (
                latitude_min,
                latitude_max,
                longitude_min,
                longitude_max,
            )
            
            # Ajout de la case au dictionnaire
            carte[case_key] = data_set
            case_count += 1
    return carte



def AnonymDonnees(fichier):

    LyonGps =(45.75, 4.85)
    BordeauxGps = (44.837789,-0.57918)
    ParisGps = (48.866667,2.333333)
    ToulouseGps = (43.6,1.43)
    Nbdiv = 100
    echelle = 0.001
    diametre = Nbdiv*echelle/2
    Lyon = CreationCarte(LyonGps[0], LyonGps[1], echelle, Nbdiv)
    Bordeaux = CreationCarte(BordeauxGps[0],BordeauxGps[1], echelle, Nbdiv)
    Paris = CreationCarte(ParisGps[0],ParisGps[1], echelle, Nbdiv)
    Toulouse = CreationCarte(ToulouseGps[0], ToulouseGps[1], echelle, Nbdiv)

    df = pd.read_csv(fichier)

    #Gestion de la date 
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].apply(lambda x: x.replace(minute=0, second=0))

    #Gestion des coordonées 
    for index, row in df.iterrows():
        if LyonGps[0]-diametre <= row["lat"] <= LyonGps[0] +diametre and LyonGps[1]-diametre <= row["lont"] <= LyonGps[1]+diametre:
            for case, (min_lat, max_lat, min_lon, max_lon) in Lyon.items():
                if min_lat <= row["lat"] <= max_lat and min_lon <= row["lont"] <= max_lon:
                    milieu_lat = (min_lat + max_lat) / 2
                    milieu_lon = (min_lon + max_lon) / 2
                    df.at[index, 'lat'] = milieu_lat
                    df.at[index, 'lont'] = milieu_lon
        elif BordeauxGps[0]-diametre <= row["lat"] <= BordeauxGps[0] +diametre and BordeauxGps[1] -diametre <= row["lont"] <=  BordeauxGps[1] +diametre:
            for case, (min_lat, max_lat, min_lon, max_lon) in Bordeaux.items():
                if min_lat <= row["lat"] <= max_lat and min_lon <= row["lont"] <= max_lon:
                    milieu_lat = (min_lat + max_lat) / 2
                    milieu_lon = (min_lon + max_lon) / 2
                    df.at[index, 'lat'] = milieu_lat
                    df.at[index, 'lont'] = milieu_lon
        elif ParisGps[0]-diametre <= row["lat"] <= ParisGps[0] +diametre and ParisGps[1] -diametre <= row["lont"] <=  ParisGps[1] + diametre:
            for case, (min_lat, max_lat, min_lon, max_lon) in Paris.items():
                if min_lat <= row["lat"] <= max_lat and min_lon <= row["lont"] <= max_lon:
                    milieu_lat = (min_lat + max_lat) / 2
                    milieu_lon = (min_lon + max_lon) / 2
                    df.at[index, 'lat'] = milieu_lat
                    df.at[index, 'lont'] = milieu_lon
        elif ToulouseGps[0]-diametre <= row["lat"] <= ToulouseGps[0] +diametre and ToulouseGps[1] -diametre <= row["lont"] <=  ToulouseGps[1] + diametre:
            for case, (min_lat, max_lat, min_lon, max_lon) in Toulouse.items():
                if min_lat <= row["lat"] <= max_lat and min_lon <= row["lont"] <= max_lon:
                    milieu_lat = (min_lat + max_lat) / 2
                    milieu_lon = (min_lon + max_lon) / 2
                    df.at[index, 'lat'] = milieu_lat
                    df.at[index, 'lont'] = milieu_lon
        else:
            df.at[index, 'id_x'] = "DEL"
            df['lont'] = df['lont'].round(2)
        
        
        print(f"Ligne {index}, fichier {fichier}")

    noise = np.random.uniform(-0.0001, 0.0001, size=len(df))
    df['lat'] = df['lat'] + noise
    df['lont'] = df['lont'] + noise
    df['week'] = df['date'].dt.to_period('W')

    df['week'] = df['week'].dt.week

    # Renommer les semaines en utilisant un dictionnaire de correspondance
    name = {i : names.get_first_name() for i in range(10,21)}
    df['id_x'] = df['week'].map(name)
    df.drop(columns=['week'], inplace=True)
    df.to_csv(f"{fichier}_final.csv", index=False)


def traitement_par_thread(noms_fichiers):

    for fichier in noms_fichiers:
        AnonymDonnees(fichier)

    

        
