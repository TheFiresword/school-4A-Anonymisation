import pandas as pd
import json

def genererJson(fichier_csv, fichier_json, incr_semaines:bool=False):
    df = pd.read_csv(fichier_csv)
    # Créer un dictionnaire pour stocker les données de sortie
    data = {}
    # Parcourir les lignes du DataFrame
    for index, row in df.iterrows():
        id_1 = row['id_o']
        semaine = ""
        if incr_semaines :
            semaine_dec = row['semaine']
            semaine = semaine_dec.split('-')[0] + '-'  + str((int(semaine_dec.split('-')[1]) + 1))
        else :
            semaine = row['semaine']
        
        id_2 = row['id_x']

        if id_1 not in data:
            data[id_1] = {}

        if semaine not in data[id_1]:
            data[id_1][semaine] = []
        
        data[id_1][semaine].append(id_2)
    
    # Compléter les ids manquants
    for i in range(1, 113):
        if i not in data :
            data[i] = {'2015-' + str(i) : None for i in range(10, 21)}
        
    # Convertir le dictionnaire en format JSON et Écrire le JSON résultant dans un fichier de sortie
    output_file = fichier_json +'.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4, separators=(',', ':'))


