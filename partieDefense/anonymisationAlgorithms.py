import pandas as pd
from graphique import *
import numpy as np
import datetime
import random
import json
from collections import defaultdict
import csv
from shapely.geometry import Polygon
import names

def permuteDeleteNoisify(df_to_treat:pd.DataFrame):
    '''
    Cet algorithme a principalement 2 objectifs :
     - Résister aux attaques par corrélation des trajectoires, par moyenne et par jointure.
     - Garder une utilité maximale, pour la date, l'heure et les POI
    
    Il consiste à appliquer successivement des couches de bruitage sur les données originales.
     - 1ère couche : arrondi des coordonnées GPS à 2 décimales (précision au quartier)
     - 2eme couche : permuation des données par groupe (id, semaine)
     - 3eme couche : suppression de p% des données par groupe
     - 4eme couche : +-0.2 aux coordonnées GPS
    
    Opérations intermédiaires :
     - Calcul des POI (métrique à satisfaire)
     - Calcul des villes de transit (métrique à satisfaire)
    '''
    # Bucketisation en tuiles représentant des quartiers (arrondi 0.01)
    df_to_treat['long'] = df_to_treat['long'].apply(lambda x : round(x, 2))
    df_to_treat['lat'] = df_to_treat['lat'].apply(lambda x : round(x, 2))
    
    # Déterminer les poi pour les garder intègres au maximum
    WORK_START = datetime.time(9, 0)
    WORK_END = datetime.time(16, 0)
    WEEKEND_START = datetime.time(10, 0)
    WEEKEND_END = datetime.time(18, 0)
    NIGHT_START = datetime.time(22, 0)
    NIGHT_END = datetime.time(6, 0)
    
    def computePOIs(df_: pd.DataFrame, file_name):
        def timedelta_def(): return datetime.timedelta()
        def defaultdicttimedalta(): return defaultdict(timedelta_def)
        def defaultdictseption(): return defaultdict(defaultdicttimedalta)
        def returnnone(): return None
        maxdict = lambda dict: max(dict, key=lambda key: dict[key])
        def diff_time(key, time1, last_date_tab):
            if last_date_tab[key] is None:
                last_date_tab[key] = time1
                return datetime.timedelta()
            else:
                difference = time1 - last_date_tab[key]
                last_date_tab[key] = time1
                return difference
        def getMaxElement(theDict):
            result = defaultdict(timedelta_def)
            for _ in range(3):
                if len(theDict)==0:
                    break
                key = maxdict(theDict)
                result[key] = theDict[key]
                del theDict[key]
            return result
        def track_deplacements(row, deplacements_par_horaire, last_date_original_tab):
            key = row[0]
            gps = (row[2], row[3])
            date_time = datetime.datetime.fromisoformat(row[1][:19])

            if date_time.weekday() < 5:
                if NIGHT_START < date_time.time() or date_time.time() < NIGHT_END:
                    deplacements_par_horaire[key]['night'][gps] += diff_time(key, date_time, last_date_original_tab)
                elif WORK_START < date_time.time() < WORK_END:
                    deplacements_par_horaire[key]['work'][gps] += diff_time(key, date_time, last_date_original_tab)
            else:
                if WEEKEND_START < date_time.time() < WEEKEND_END:
                    deplacements_par_horaire[key]['weekend'][gps] += diff_time(key, date_time, last_date_original_tab) 
        
        #--------------------------------------------------------#
        # Détermination de l'horaire de chaque entrée du df
        #--------------------------------------------------------#
        tmp = pd.to_datetime(df_['date'])
        conditions = [
            (tmp.dt.weekday < 5) & ((tmp.dt.time > NIGHT_START) | (tmp.dt.time < NIGHT_END)),
            (tmp.dt.weekday < 5) & ((WORK_START < tmp.dt.time) & (tmp.dt.time< WORK_END)),
            (tmp.dt.weekday >= 5) & ((WEEKEND_START < tmp.dt.time) & (tmp.dt.time< WEEKEND_END))
        ]
        horaires = ['night', 'work', 'weekend']
        for condition, horaire in zip(conditions, horaires):
            df_.loc[condition, horaire] = True
        
        #--------------------------------------------------------#
        # Calcul des durées passées dans à position gps pour chaque id
        #--------------------------------------------------------#
        deplacements_par_horaire = defaultdict(defaultdictseption)
        last_date_original_tab = defaultdict(returnnone)
        
        fd_original = open(file_name, newline='')
        original_reader = csv.reader(fd_original, delimiter="\t")
        
        for row in original_reader:
            track_deplacements(row, deplacements_par_horaire, last_date_original_tab)
        
        #--------------------------------------------------------#
        # Calcul des positions POI de niveau 1
        #--------------------------------------------------------#
        final_tab = defaultdict(defaultdictseption)
        for id in deplacements_par_horaire:
            for type in deplacements_par_horaire[id]:
                final_tab[id][type] = getMaxElement(deplacements_par_horaire[id][type])

        poi = []
        for id in final_tab:
            vartmp = {'id': id, 'night': None, 'work': None, 'weekend': None, 'duree_night': None, 'duree_work': None, 'duree_weekend': None}
            for champ in final_tab[id]:
                vartmp[champ] = max(final_tab[id][champ], key=lambda x: final_tab[id][champ][x])
                delta_duree = final_tab[id][champ][vartmp[champ]]
                vartmp['duree_'+str(champ)] =  (delta_duree.days * 24 * 3600) + delta_duree.seconds
                isPoiCondition = (df_[champ]) & \
                    (df_['id']==np.int16(id)) & \
                    (df_['long']==float(vartmp[champ][0])) & \
                    (df_['lat']==float(vartmp[champ][1]))
                    
                df_.loc[isPoiCondition, 'isPoi'] = True  
            poi.append(vartmp)
        return poi
    
    def computeTransitCities(df, border_data_file, border_precision=0.01, duration_threeshold=60):
        # Nouvelle fonction pour tenir compte de la métrique mobilité des Lyonnais
        # Comme dans la fonction de la métrique, on calcule la frontière de la métropole de Lyon
        
        def check_time_spent(group):
            group['date'] = pd.to_datetime(group['date'], format="%Y-%m-%d %H:%M:%S")
            group = group.sort_values(by="date")
            time_spent = (group['date'].iloc[group.shape[0]-1] - group['date'].iloc[0]).seconds
            df.loc[group.index, 'isTransitCity'] = False if time_spent >= duration_threeshold else True
            return group
        
        with open(border_data_file, 'r') as fichier_json :
            data = json.load(fichier_json)
            lyon_shape = Polygon(data)
            del data
            # Simplifier le polygone
            lyon_shape = lyon_shape.simplify(border_precision)
            # Grouper par coordonnée et id et vérifier le temps passé à la coordonnée
            df.groupby(by=["id", "long", "lat"], group_keys=True, sort=False).apply(check_time_spent)            
        return

    def permuteData(df: pd.DataFrame, to_poi_entries:bool | None =False, to_transit_entries:bool | None =True):
        groups_indexes, groups_idx = zip(*[(group_indexes, idx) for idx, group_indexes in df.groupby(['id', 'semaine']).groups.items()])
        groups_indexes = list(groups_indexes)
        groups_idx_listified = list(groups_idx)
        groups_idx = set(groups_idx)
        groups_traites_idx = set()

        def pickAnotherGroupInTmp(current_group: Tuple):
            remaining_groups = list(groups_idx - groups_traites_idx)
            remaining_groups.remove(current_group)
            if len(remaining_groups)!=0:
                priority_groups = list(set([a for a in remaining_groups if a[0] != current_group[0]]))
                if len(priority_groups) > 0: other_group = random.choice(priority_groups)
                else: other_group = random.choice(remaining_groups)
                group_position = groups_idx_listified.index(other_group)
                return groups_indexes[group_position]
        
        for idx, group in df.groupby(['id', 'semaine']).groups.items():        
            if to_poi_entries is not None:
                poi_condition = (df.loc[group, 'isPoi'] == to_poi_entries)
                group = group[poi_condition]
            if to_transit_entries is not None:
                transit_condition = (df.loc[group, 'isTransitCity'] == to_transit_entries)
                group = group[transit_condition]
            #print(group)
            df_group = df.loc[group]
            if idx not in groups_traites_idx:
                other_group_indexes = pickAnotherGroupInTmp(idx)
                if other_group_indexes is not None :
                    if to_poi_entries is not None:
                        poi_condition = (df.loc[other_group_indexes, 'isPoi'] == to_poi_entries)
                        other_group_indexes = other_group_indexes[poi_condition]
                    if to_transit_entries is not None:
                        transit_condition = (df.loc[other_group_indexes, 'isTransitCity'] == to_transit_entries)
                        other_group_indexes = other_group_indexes[transit_condition]
                        
                    other_group = df.loc[other_group_indexes]
                    if not other_group.empty :
                        a = df_group[['long', 'lat']].copy()
                        b = other_group[['long', 'lat']].copy()                
                        if a.shape[0] < b.shape[0]:
                            df.loc[group, ['long', 'lat']] = b.iloc[:a.shape[0], :].values
                            df.loc[other_group_indexes, ['long', 'lat']].iloc[:a.shape[0], :] = a.values                    
                        else:
                            df.loc[group, ['long', 'lat']].iloc[ : b.shape[0], :] = b.values
                            df.loc[other_group_indexes, ['long', 'lat']] = a.iloc[:b.shape[0], :].values

                        groups_traites_idx.add(tuple(idx))
                        groups_traites_idx.add(tuple((other_group['id'].iloc[0], other_group['semaine'].iloc[0])))        
        return df
    
    def shiftHour(entry) ->str:
        originalDate = datetime.datetime.fromisoformat(entry)
        shiftValue = -18 if originalDate.time()>=datetime.time(18,00) else 6
        shiftedDate = originalDate + datetime.timedelta(hours=shiftValue)
        entry = shiftedDate.strftime("%Y-%m-%d %H:%M:%S")
        return entry
    
    def deleteData(df: pd.DataFrame, to_poi_entries:bool|None =False, proportion=1/3):
        def suppressionAleatoire(group):
            tmp = group[group['isPoi']==to_poi_entries] if to_poi_entries is not None else group
            tailleSup = int(len(tmp)*proportion)
            indices_to_remove = np.random.choice(tmp.index, size=tailleSup, replace=False)
            group.loc[indices_to_remove, 'id'] = 'DEL'
            return group
        df['id']= df.groupby(['id', 'semaine'], group_keys=True, sort=False).apply(suppressionAleatoire)['id'].values
        return

    def noisifyGps(df_part: pd.DataFrame):
        noise = np.random.choice([-0.02, 0.02], size=(len(df_part), 2))
        df_part[['long', 'lat']] += noise
        return df_part
    
    
    computePOIs(df_to_treat, "truth_ground.csv")
    computeTransitCities(df_to_treat, "partieMetriques/limitesMetropole.json", border_precision=0.01, duration_threeshold=60)
    df_to_treat = permuteData(df_to_treat, to_poi_entries=False, to_transit_entries=True)
    deleteData(df_to_treat, to_poi_entries=False, proportion=0)
    df_to_treat = noisifyGps(df_to_treat)
    
    return df_to_treat


def clusteriser():
    
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
        echelle = 0.01
        diametre = Nbdiv*echelle/2
        Lyon = CreationCarte(LyonGps[0], LyonGps[1], echelle, Nbdiv)
        Bordeaux = CreationCarte(BordeauxGps[0],BordeauxGps[1], echelle, Nbdiv)
        Paris = CreationCarte(ParisGps[0],ParisGps[1], echelle, Nbdiv)
        Toulouse = CreationCarte(ToulouseGps[0], ToulouseGps[1], echelle, Nbdiv)

        df = pd.read_csv(fichier)

        #Gestion de la date 
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].apply(lambda x: x.replace(minute=0, second=0))

        df['week'] = df['date'].dt.to_period('W')

        df['week'] = df['week'].dt.week

        # Renommer les semaines en utilisant un dictionnaire de correspondance
        name = {i : names.get_first_name() for i in range(10,21)}
        df['id_x'] = df['week'].map(name)
        df.drop(columns=['week'], inplace=True)

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

        noise = np.random.uniform(-0.001, 0.001, size=len(df))
        df['lat'] = df['lat'] + noise
        df['lont'] = df['lont'] + noise
        
        df.to_csv(f"{fichier}_final2.csv", index=False)
