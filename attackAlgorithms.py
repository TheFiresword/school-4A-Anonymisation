import pandas as pd
import gc
import time
from processingData import *
from scipy.spatial.distance import directed_hausdorff
from pandas.core.groupby.generic import DataFrameGroupBy

def jointureNaive(df_original, df_anonymise, nom_fichier):
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
    df_jointure['date'] = pd.to_datetime(df_jointure['date'], format="%Y-%m-%d %H:%M:%S")
    df_jointure['date'] = df_jointure['date'].dt.strftime('%Y-%U')
    
    df_jointure.rename(columns={'date':'semaine'}, inplace=True)
    
    df_correspondances = df_jointure.groupby(['id_o', 'semaine', 'id_x']).size().reset_index(name='count')
    del df_jointure
    gc.collect()
    
    index_correspondances_probables = df_correspondances.groupby(['id_o', 'semaine'])['count'].idxmax()
    df_correspondances = df_correspondances.loc[index_correspondances_probables].sort_values(by=['id_o', 'semaine'],
                                                                                             ascending=[True, True])
    df_correspondances.to_csv(nom_fichier+'.csv', index=False)


def calcul_distance_hausdorff(trajectoire1, trajectoire2):
    return max(directed_hausdorff(trajectoire1, trajectoire2)[0], directed_hausdorff(trajectoire2, trajectoire1)[0])

def similitudeTrajectoires(df_original, df_anonymise, nom_fichier):
    '''
    Fonction : L'idée de cet algorithme est d'analyser la corrélation entre trajectoires.
    Par exemple, pour l'id réel 1, on va construire l'ensemble de coordonnées par semaine, et puis on va analyser
    la similitude avec les données de chaque id anonyme.
    Faudrait prioriser dans l'ordrer : la trajectoire - la semaine
    ''' 
    t0 =  time.time()
    correspondences = pd.DataFrame(columns=['id_o', 'semaine', 'id_x'])
    
    df_anonymise['semaine']  = pd.to_datetime(df_anonymise['date'], format="%Y-%m-%d %H:%M:%S").dt.isocalendar().week
                
    for vrai_id in df_original['id'].unique():
        df_i = df_original[(df_original['id'] == vrai_id)].copy()
        df_i['semaine']  = pd.to_datetime(df_i['date'], format="%Y-%m-%d %H:%M:%S").dt.isocalendar().week
        
        for semaine in range(10, 21):                        
            df_i_semaine = df_i[df_i['semaine'] == semaine]
            if df_i_semaine.empty :
                continue
            #print(df_i_semaine.head(5))
            min_distance = float(10000)
            correspondant_id = None

            for id_anonyme in df_anonymise['id'].unique():
                df_anonymise_j = df_anonymise[df_anonymise['id'] == id_anonyme]
                #print(df_anonymise_j['date'].value_counts().idxmax())
                if df_anonymise_j['semaine'].value_counts().idxmax() != semaine:
                    continue
                distance = calcul_distance_hausdorff(df_i_semaine[['long', 'lat']], df_anonymise_j[['long', 'lat']])

                if distance < min_distance:
                    min_distance = distance
                    correspondant_id = id_anonyme
            print(f"Id réel {vrai_id} -- semaine 2015-{semaine} -- Id anonyme {correspondant_id}")
            df_anonymise = df_anonymise[df_anonymise['id'] != correspondant_id]
            correspondences = pd.concat(
                [pd.DataFrame({'id_o' : vrai_id, 'semaine': '2015-'+str(semaine), 'id_x': correspondant_id}, 
                                                      columns=correspondences.columns, index=[0]), 
                 correspondences], 
            ignore_index=True)
    print("Temps écoulé : ",time.time()-t0)
    return correspondences.to_csv(nom_fichier+'.csv', index=False)


def correlation(df_original, df_anonymise, nom_fichier):
    '''
    Fonction : L'idée de cet algorithme est d'analyser la corrélation entre trajectoires.
    Par exemple, pour l'id réel 1, on va construire l'ensemble de coordonnées par semaine, et puis on va analyser
    la similitude avec les données de chaque id anonyme.
    Faudrait prioriser dans l'ordrer : la trajectoire - la semaine
    '''    
    # Initialisations
    pd.DataFrame(columns=['id_o', 'semaine', 'id_x', 'dissimilarite']).to_csv(nom_fichier+'.csv', header=True, index=False)
    
    # Transformation dates => semaines
    df_original['date'] = df_original['date'].dt.strftime('%Y-%U')
    df_anonymise['date'] = df_anonymise['date'].dt.strftime('%Y-%U')
    df_original.rename(columns={'date':'semaine'}, inplace=True)
    df_anonymise.rename(columns={'date':'semaine'}, inplace=True)
    
    def calcul_dissimilarite_avec_ids_anonymes(group):
        nonlocal df_anonymise
        df_i_semaine = group        
        semaine = df_i_semaine['semaine'].iloc[0]
        
        dissimilarites = {}

        for id_anonyme, df_anonymise_j in df_anonymise[df_anonymise['semaine'] == semaine].groupby('id'):
            dissimilarite = directed_hausdorff(u=df_i_semaine[['long', 'lat']], v=df_anonymise_j[['long', 'lat']])[0]
            dissimilarites[id_anonyme] = dissimilarite

        id_correspondance_probable = min(dissimilarites, key=dissimilarites.get)
        
        df_anonymise = df_anonymise[df_anonymise['id'] != id_correspondance_probable]

        df_correspondance = pd.DataFrame({
            'id_o': df_i_semaine['id'].iloc[0],
            'semaine': semaine,
            'id_x': id_correspondance_probable,
            'dissimilarite': dissimilarites[id_correspondance_probable]
        }, index=[0])

        df_correspondance.to_csv(nom_fichier+'.csv', mode='a', header=False, index=False)

    df_original.groupby(['id', 'semaine']).apply(calcul_dissimilarite_avec_ids_anonymes)
    

def machineLearning():
    '''
    Fonction : Le but est de prendre pour chaque identifiant anonymisé, donc sur
    1 semaine,
    attaque500:
    filtrer par couleur > range de longitude
    quand la range est trop petite passer
    regarder la forme de la trajectoire et corréler avec les trajectoires réelles
    '''