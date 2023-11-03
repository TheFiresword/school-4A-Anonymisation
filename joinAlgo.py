import pandas as pd
import json

def nettoyerDonneesAnonymisees(fichier : str):
    '''
    Fonction : Clean les données en forçant les types des colonnes - supprimant les lignes DEL etc
    '''
    df = pd.read_csv(fichier, delimiter='\t')
    df.columns = ["id_x","date", "long", "lat"]
    # On a assez de données pour se permettre de supprimer les lignes qui ont même un champ DEL
    df_propre = df.loc[(df["id_x"] != "DEL") & (df["date"] != "DEL") & (df["long"] != "DEL") & (df["lat"] != "DEL")]
    columns_types = {'id_x' : str, 'date': str, 'long': float, 'lat': float}
    df_propre = df_propre.astype(columns_types)
    #df_propre.to_csv('cleaned.csv', index=False)
    return df_propre


def appliquerAlgorithme(df_original, df_anonymise, nom_fichier):
    '''
    Fonction : L'idée de l'algorithme est de faire des jointures entre le fichier original (truth ground) et le fichier 
    à attaquer, pour retrouver les correspondances identifiant original ⇔ pseudo identifiant. La contrainte est que plusieurs 
    individus de la base de données se retrouvent très souvent, au même endroit au même moment. Pour essayer de les départager 
    et être plus précis, l'algorithme cherche l'individu(pseudonymisé) qui a le plus de correspondances sur la semaine avec 
    l'identifiant original.
    '''
    df_jointure = df_original.merge(df_anonymise, on=['date'], suffixes=['_o','_x'])
    precision_mask = df_jointure.apply(axis = 1, func = lambda row : abs(row['long_o']-row['long_x']) < 0.001 and abs(row['lat_x']-row['lat_o']) < 0.001)
    df_jointure = df_jointure[precision_mask].drop(columns=['long_x', 'lat_x']).rename(
        columns={'long_o': 'long', 'lat_o' : 'lat'})

    df_jointure[['date', 'heure']] = df_jointure['date'].str.split(' ', n=1, expand=True)
    df_jointure['date'] = pd.to_datetime(df_jointure['date'])

    df_jointure['date'] = df_jointure['date'].dt.to_period('W')
    # Renommer les semaines avec un numéro particulier
    df_jointure['date'] = df_jointure['date'].dt.week

    # Renommer les semaines en utilisant un dictionnaire de correspondance
    numero_semaines = {10: '2015-10', 11: '2015-11', 12:'2015-12', 13: '2015-13', 14: '2015-14', 15: '2015-15', 16: '2015-16', 
                       17: '2015-17', 18: '2015-18', 19: '2015-19', 20: '2015-20'}
    df_jointure['date'] = df_jointure['date'].map(numero_semaines)
    df_jointure.rename(columns={'date':'semaine'}, inplace=True)
    
    df_correspondances = df_jointure.groupby(['id_o', 'semaine', 'id_x']).size().reset_index(name='count')
    index_correspondances_probables = df_correspondances.groupby(['id_o', 'semaine'])['count'].idxmax()
    df_correspondances = df_correspondances.loc[index_correspondances_probables].sort_values(by=['count', 'id_o'], 
                                                                                             ascending=[False, True])
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