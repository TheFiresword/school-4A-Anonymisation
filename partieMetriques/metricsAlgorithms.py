import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import json
from random import randint
from shapely.geometry import Point, Polygon
from time import sleep
import os

def metric1(file_noanon, file_anon, file_tmp):
    '''
        But: Déterminer les villes françaises, autres que Lyon, les plus fréquentées par les Lyonnais. 
        Les villes hors de France ne sont pas considérées.
        
        Pseudo-code métrique  :
            - Modélisation de la frontière de la métropole de Lyon par un polygone de points GPS.
            - Exclusion des villes de transit, où la durée passée dans la ville est inférieure à 60 minutes.
            - Exclusion des points appartenant à la métropole de Lyon.
            - Pour chaque enregistrement restant, on calcule la ville (code postal) et le pays correspondant à la position GPS, 
                et on retient seulement les enregistrements où le pays est la France.
            - Pour chaque ville, on compte le nombre d'individus uniques qui y sont allés.

    '''
    def compute_based_town_boundaries(data_file, tolerance=0.01):
        with open(data_file, 'r') as fichier_json :
            data = json.load(fichier_json)
            lyon_shape = Polygon(data)
            del data
            print("Complexité originale de la frontière : " ,len(lyon_shape.exterior.coords))
            x, y = lyon_shape.exterior.xy
            plt.plot(x, y, label='Polygone Non Simplifié', color='red')
            
            # Simplifier le polygone
            lyon_shape = lyon_shape.simplify(tolerance)
            print("Complexité simplifiée de la frontière : ", len(lyon_shape.exterior.coords))
            
            x, y = lyon_shape.exterior.xy
            plt.plot(x, y, label='Polygone Non Simplifié', color='blue')
            return lyon_shape
    
    
    def find_dest_towns(based_town_shape, file_name, tmp_file_name, precision=2, duration_threeshold=60):
    
        def check_time_spent(group, reduced_data):
            group = group.sort_values(by="date")
            time_spent = (group['date'].iloc[group.shape[0]-1] - group['date'].iloc[0]).seconds
            if time_spent >= duration_threeshold:
                # C'est un endroit où l'individu a passé au moins duration_threeshold secondes
                # donc potentiellement une destination
                # on check si c'est différent de Lyon
                gps = (group['long'].iloc[0], group['lat'].iloc[0])
                if not based_town_shape.contains(Point(gps)):
                    reduced_data['id'].append(group['id'].iloc[0])
                    reduced_data['date'].append(group['date'].iloc[0].strftime("%Y-%m-%d %H:%M:%S"))
                    reduced_data['long'].append(gps[0])
                    reduced_data['lat'].append(gps[1])

            return reduced_data
        
        df = pd.read_csv(file_name, delimiter= '\t', header=None)
        df.columns = ["id","date", "long", "lat"]
        df = df[df['id'] != "DEL"]

        columns_types = {'id' : str, 'date': str, 'long': np.float32, 'lat': np.float32}
        df = df.astype(columns_types)
        df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S")
        df['long'] = df['long'].apply(lambda x : round(x, precision))
        df['lat'] = df['lat'].apply(lambda x : round(x, precision))
        df = df.sort_values(by="id")
        
        reduced_data = {'id': [], 'date': [], 'long': [], 'lat': []}
        # Grouper par coordonnée et id et vérifier le temps passé à la coordonnée
        df.groupby(by=["id", "long", "lat"], group_keys=True, sort=False).apply(check_time_spent, reduced_data)
        
        try:
            os.remove(tmp_file_name)
        except OSError as e:
            None
        pd.DataFrame(reduced_data).to_csv(tmp_file_name, sep="\t", index=False, header=False)
        return
    
    def reverse_geocode(geolocator, gps, sleep_sec):
        try:
            return geolocator.reverse(gps)
        except GeocoderTimedOut:
            print("Sleeping")
            sleep(randint(1*100,sleep_sec*100)/100)
            return reverse_geocode(geolocator, gps, sleep_sec)
        except GeocoderServiceError as e:
            return None
        except Exception as e:
            return None
    
    def compute_metrique1(file_name, precision=2):
        BASED_COUNTRY = "France".lower()
        # Pré-requis : file_name est le chemin du fichier généré par la fonction find_dest_towns() précédente
        # Il contient uniquement les enregistrements où la ville est différente de Lyon et l'individu a passé 
        # un certain temps
        towns_visited = dict()
        travellers_counter = 0
        fd_original = open(file_name, newline='')
        original_reader = csv.reader(fd_original, delimiter="\t")
        user_agent = 'user_me_{}'.format(randint(10000,99999))
        geolocator = Nominatim(user_agent=user_agent)
        banned_gps = set()
        
        for row in original_reader:        
            key = row[0]
            if "DEL" != key[0 :3].upper():
                gps = (round(float(row[2]), precision), round(float(row[3]), precision))
                town_gps = (round(gps[0], precision-1), round(gps[1], precision-1))
                #town_gps = gps
                if town_gps in towns_visited :
                    towns_visited[town_gps]['keys'].add(key)
                    continue
                if town_gps in banned_gps:
                    continue
                                    
                print("Requete" , travellers_counter+1, " id :", key, " gps : ", town_gps)
                location = reverse_geocode(geolocator, reversed(gps), 5)
                if location:
                    str_location = f"{location}".split(', ')
                    if len(str_location) >= 2 :
                        current_country, current_town = (str_location[-1].lower(), str_location[-2])
                        if current_country == BASED_COUNTRY:
                            #print("Nouvelle ville ", current_town, "\n")
                            travellers_counter += 1
                            if town_gps not in towns_visited:
                                towns_visited[town_gps] = {'zip_code': current_town, 'keys': set()}
                                towns_visited[town_gps]['keys'].add(key)
                        else:
                            print("Autre pays : ", current_country)
                            banned_gps.add(town_gps)
                else :
                    print("Error during retrieving localisations data")
                    banned_gps.add(town_gps)
                    
        towns_counter = {}
        for town in towns_visited:
            if not towns_visited[town]['zip_code'] in towns_counter:
                towns_counter[towns_visited[town]['zip_code']] = set(towns_visited[town]['keys'])
                
            else:
                towns_counter[towns_visited[town]['zip_code']] |= set(towns_visited[town]['keys'])

        print(towns_counter)
        towns_counter = {key: val for key, val in sorted({k: len(v) for k, v in towns_counter.items()}.items(), key = lambda ele: ele[1], reverse=True)} 
        print(towns_counter, "\n", travellers_counter)
        return towns_counter
    
    def compute_score(utility_noanon, utility_anon):
        score = 0
        for postal_code in utility_noanon :
            if postal_code in utility_anon :
                count_noanon = utility_noanon[postal_code]
                count_anon = utility_anon[postal_code]
                score += (count_anon / count_noanon) if count_anon < count_noanon else (count_noanon / count_anon)
        score /= len(utility_noanon)
        assert 0 <= score <= 1
        return score

    LYON_SHAPE = compute_based_town_boundaries(data_file='partieMetriques/limitesMetropole.json', tolerance=0.01)
    
    def measure(file_noanon, file_anon, tmp_file, gps_precision=2):
        find_dest_towns(LYON_SHAPE, file_noanon, tmp_file, gps_precision, duration_threeshold=60)
        result_noanon = compute_metrique1(tmp_file, gps_precision)
        
        find_dest_towns(LYON_SHAPE, file_anon, tmp_file, gps_precision, duration_threeshold=60)
        result_anon = compute_metrique1(tmp_file, gps_precision)
        return result_noanon, result_anon, compute_score(result_noanon, result_anon)
    
    a, b, c = measure(file_noanon, file_anon, file_tmp)
    return c


def metric2(file_noanon, file_anon):
    '''
        But : Calculer la distance parcourue par un individu chaque semaine en kilomètres selon ses coordonnées. 
        
        Après une étape de séparation et de tri, on va pour chaque identifiant, calculer son déplacement par jour 
        sur une semaine. Pour se faire, on utilise également la bibliothèque “geopy” qui permet de calculer une 
        distance entre deux coordonnées GPS pour facilement. On itère donc sur chaque coordonnées et calcule la distance 
        entre chaque ping pour un jour précis. Ensuite on ajoute les distances pour tous les jours présents dans la base 
        de données pour cet individu et on obtient une distance hebdomadaire. Nous avons forcément des erreurs qui 
        proviennent du manque de ping à certaines heures. Mais cela ne pose pas un réel problème car nous allons quand même 
        calculer la distance entre les 2 pings même si ceux là sont séparés par des heures. On obtient alors la distance 
        “à vol d'oiseau” parcouru par cet individu à la place de la distance exacte qu'il a effectuée si ce dernier à changer de lieu.
    '''
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

        Origin = calcul_distance(fichierOriginal)
        (min0, max0, moy0) = temoin(Origin)
        Anonym = calcul_distance(fichieranonym)
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
    
    return utilite(file_noanon, file_anon)