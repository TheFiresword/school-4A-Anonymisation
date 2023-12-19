import pandas as pd
import json

def genererJson(fichier_csv, fichier_json, incr_semaines:bool=False, idx_type=str, semaine_label='semaine'):
    df = pd.read_csv(fichier_csv)
    df=df.astype({'id_o': int, semaine_label: str, 'id_x': idx_type})
    # Créer un dictionnaire pour stocker les données de sortie
    data = {}
    # Parcourir les lignes du DataFrame
    for index, row in df.iterrows():
        id_1 = row['id_o']
        semaine = ""
        if incr_semaines :
            semaine_dec = row[semaine_label]
            #semaine = semaine_dec.split('-')[0] + '-'  + str((int(semaine_dec.split('-')[1]) + 1))
            semaine = '2015-' + str(int(semaine_dec)+1)
        else :
            semaine = '2015-' + str(row[semaine_label])
        
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


def completeJson(jsonFile):
    with open(jsonFile, 'r') as f:
        previous_attack = json.load(f)
        for i in range(1, 113):
            i = str(i)
            if i not in previous_attack:
                previous_attack[i] = {'2015-' + str(i) : None for i in range(10, 21)}
            else:
                for j in range(10, 21):
                    j = str(j)
                    if '2015-' + j not in previous_attack[i]:
                        #print(f"{i, j}")
                        previous_attack[i]['2015-' + str(j)] = None
                    else:
                        print(f"{i, j}")

        with open('copy.json', 'w') as g:
            json.dump(previous_attack, g, indent=4, separators=(',', ':'))
    return