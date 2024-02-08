import pandas as pd
import numpy as np
import json
import string, random
from morse3 import Morse as m
from anonymisationAlgorithms import *
from metrics import pointsOfInterest, hour, meet, date, distance, tuile, nationalMobility

# Charger le fichier de vérité dans un dataframe sans le télécharger
df = pd.read_csv("truth_ground.csv", delimiter= '\t', header=None)    
df.columns = ["id","date", "long", "lat"]
print(df.head(2))
# Ajout de colonnes pour aider au traitement
df['isPoi'] = [False]*df.shape[0]
df['isTransitCity'] = [False]*df.shape[0]
df['night'] = [False]*df.shape[0]
df['work'] = [False]*df.shape[0]
df['weekend'] = [False]*df.shape[0]
df['semaine'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S").dt.isocalendar().week

columns_types = {'id' : np.int16, 'date': str, 'long': np.float32, 'lat': np.float32, 
                 'isPoi' : bool, 'night': bool, 'work': bool, 'weekend': bool, 'semaine': np.int16}
df = df.astype(columns_types)

df = permuteDeleteNoisify(df)

CHARACTERS_POOL = string.ascii_letters + string.digits
CORRESPONDANCES_FILE =  'correspondances3.json'

def generatePseudoIds(df_ : pd.DataFrame):
    def generator(group, nb_characters : int):
        pseudo_id_str = ''.join(random.choice(CHARACTERS_POOL) for _ in range(nb_characters))
        pseudo_id_final = m(pseudo_id_str).stringToMorse().replace(" ", "")
        group.loc[group!='DEL'] = pseudo_id_final
        #print(group)
        return group

    def saveCorrespondances(group:pd.DataFrame, corresp_struc):
        tmp = group.loc[group['id'] != 'DEL' ,['id', 'id_x']]
        id_original = int(tmp['id'].iloc[0]) if not tmp.empty else 'DEL'
        if id_original == 'DEL':
            return group
        pseudo_id_final = tmp['id_x'].iloc[0]

        if id_original not in corresp_struc:
            corresp_struc[id_original] = {}
        semaine = f"2015-{group['semaine'].iloc[0]}"
        if  semaine not in corresp_struc[id_original]:
            corresp_struc[id_original][semaine] = []
        corresp_struc[id_original][semaine].append(pseudo_id_final)
        return group

    data = {}
    df_['id_x'] = df_['id']   
    df_['id_x'] = df_.groupby(['id', 'semaine'])['id_x'].transform(lambda group: generator(group, nb_characters=5))
    df_.groupby(['id', 'semaine'], group_keys=True).apply(lambda group : saveCorrespondances(group, corresp_struc=data))
    
    with open(CORRESPONDANCES_FILE, 'w') as f:
        json.dump(data, f, indent=4, separators=(',', ':'))
    return df_

b = generatePseudoIds(df.copy())
b[['id_x', 'date', 'long', 'lat']].to_csv("partieDefense/soumissions/anonym3.csv", sep="\t", index=False, header=False)

def calculScore(originial_f, anonymise_f):
    metrics = []
    for metric in [pointsOfInterest, hour, meet, date, distance, tuile, nationalMobility]:
        metrics.append(metric.main(originial_f, anonymise_f))
    return metrics
calculatedMetrics = calculScore("truth_ground.csv", "partieDefense/soumissions/anonym3.csv")
print("Tableau de métriques = ", calculatedMetrics)
score = np.mean(calculatedMetrics)
print("Score = ", score)


def calculateReidentificationScore(json_correct, json_soumis):
    score = 0
    nb_pseudo = 0
    with open(json_correct, 'r') as f:
        data_correct = json.load(f)

    with open(json_soumis, 'r') as f:
        data_soumis = json.load(f)

    for id, semaines_correctes in data_correct.items():
            # Comparer les pseudo-identifiants pour chaque semaine
            for semaine, pseudo_id_correct in semaines_correctes.items():
                nb_pseudo += 1
                if id in data_soumis:
                    pseudo_id_soumis = data_soumis[id].get(semaine, None)
                    # Vérifier les correspondances
                    if pseudo_id_soumis and pseudo_id_correct[0] == pseudo_id_soumis[0]:
                        score += 1
    print(f"Score={score}/{nb_pseudo}")
    return score/nb_pseudo
calculateReidentificationScore('correspondances3.json', 'partieAttaque/autoAttaques/sub2.json')