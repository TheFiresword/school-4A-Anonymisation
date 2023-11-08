import pandas as pd
import json
import gc
from processingData import *

def appliquerAlgorithme(df_original, df_anonymise, nom_fichier):
    '''
    Fonction : L'idée de l'algorithme est de faire des jointures entre le fichier original (truth ground) et le fichier 
    à attaquer, pour retrouver les correspondances identifiant original ⇔ pseudo identifiant. La contrainte est que plusieurs 
    individus de la base de données se retrouvent très souvent, au même endroit au même moment. Pour essayer de les départager 
    et être plus précis, l'algorithme cherche l'individu(pseudonymisé) qui a le plus de correspondances sur la semaine avec 
    l'identifiant original.
    '''
    df_jointure = pd.merge(df_original, df_anonymise, on=['date', 'long', 'lat'], how='inner', suffixes=['_o', '_x'])
    # optimisation mémoire
    del df_original
    del df_anonymise
    gc.collect()
    
    # Il faut rajouter +1 aux semaines parce que la méthode strftime() commence à partir de 0
    df_jointure['date'] = df_jointure['date'].dt.strftime('%Y-%U')
    df_jointure['date'] = (df_jointure['date'].str.split('-').str[0] + '-' +
                    (df_jointure['date'].str.split('-').str[1].astype(int) + 1).astype(str))

    df_jointure.rename(columns={'date':'semaine'}, inplace=True)
    
    df_correspondances = df_jointure.groupby(['id_o', 'semaine', 'id_x']).size().reset_index(name='count')
    del df_jointure
    gc.collect()
    
    index_correspondances_probables = df_correspondances.groupby(['id_o', 'semaine'])['count'].idxmax()
    df_correspondances = df_correspondances.loc[index_correspondances_probables].sort_values(by=['id_o', 'semaine'],
                                                                                             ascending=[True, True])
    df_correspondances.to_csv(nom_fichier+'.csv', index=False)


def genererJson(fichier_csv, fichier_json):
    df = pd.read_csv(fichier_csv)
    # Créer un dictionnaire pour stocker les données de sortie
    data = {}
    # Parcourir les lignes du DataFrame
    for index, row in df.iterrows():
        id_1 = row['id_o']
        semaine = row['semaine']
        id_2 = row['id_x']

        if id_1 not in data:
            data[id_1] = {}

        if semaine not in data[id_1]:
            data[id_1][semaine] = []
        
        data[id_1][semaine].append(id_2)
        
    # Convertir le dictionnaire en format JSON et Écrire le JSON résultant dans un fichier de sortie
    output_file = fichier_json +'.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4, separators=(',', ':'))