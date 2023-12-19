from numpy import Inf
import pandas as pd
import gc
import time
from processingData import *
from scipy.spatial.distance import directed_hausdorff
from pandas.core.groupby.generic import DataFrameGroupBy
import concurrent.futures

def jointureNaive(df_original: pd.DataFrame, df_anonymise:pd.DataFrame, nom_fichier, sur_semaine=False, is_frangipane=False):
    '''
    Fonction : L'idée de l'algorithme est de faire des jointures entre le fichier original (truth ground) et le fichier 
    à attaquer, pour retrouver les correspondances identifiant original ⇔ pseudo identifiant. La contrainte est que plusieurs 
    individus de la base de données se retrouvent très souvent, au même endroit au même moment. Pour essayer de les départager 
    et être plus précis, l'algorithme cherche l'individu(pseudonymisé) qui a le plus de correspondances sur la semaine avec 
    l'identifiant original.
    '''
    if is_frangipane:
        if sur_semaine:
            df_jointure = pd.merge(df_original, df_anonymise, on=['semaine', 'long'], how='inner', suffixes=['_o', '_x'])
        else:
            df_jointure = pd.merge(df_original, df_anonymise, on=['date', 'long'], how='inner', suffixes=['_o', '_x'])
        print(df_jointure.head(2))

    else:
        df_jointure = pd.merge(df_original, df_anonymise, on=['date', 'long', 'lat'], how='inner', suffixes=['_o', '_x'])
        df_jointure.drop(columns=['semaine_x'], inplace=True)
        df_jointure.rename(columns={'semaine_o': 'semaine'}, inplace=True)
    
    # optimisation mémoire
    del df_original
    del df_anonymise
    gc.collect()
    
    if is_frangipane:
        df_correspondances = df_jointure.groupby(['id_o', 'semaine_o', 'id_x']).size().reset_index(name='count')
        index_correspondances_probables = df_correspondances.groupby(['id_o', 'semaine_o'])['count'].idxmax()
        df_correspondances = df_correspondances.loc[index_correspondances_probables].sort_values(by=['id_o', 'semaine_o'],
                                                                                             ascending=[True, True])
    else:
        df_correspondances = df_jointure.groupby(['id_o', 'semaine', 'id_x']).size().reset_index(name='count')
        index_correspondances_probables = df_correspondances.groupby(['id_o', 'semaine'])['count'].idxmax()
        df_correspondances = df_correspondances.loc[index_correspondances_probables].sort_values(by=['id_o', 'semaine'],
                                                                                             ascending=[True, True])
    
    del df_jointure
    gc.collect()
    #df_correspondances.to_csv(nom_fichier+'all.csv', index=False)
    
    df_correspondances.to_csv(nom_fichier+'.csv', index=False)




def calcul_distance_hausdorff(trajectoire1, trajectoire2):
    return max(directed_hausdorff(trajectoire1, trajectoire2)[0], directed_hausdorff(trajectoire2, trajectoire1)[0])




def similitudeTrajectoires(df_original, df_anonymise, nom_fichier):
    def process_semaine(vrai_id, semaine):
        df_i_semaine = df_original[(df_original['id'] == vrai_id) & (df_original['semaine'] == semaine)]
        if df_i_semaine.empty:
            return None

        min_distance = float('inf')
        correspondant_id = None

        for id_anonyme in df_anonymise['id'].unique():
            df_anonymise_j = df_anonymise[(df_anonymise['id'] == id_anonyme) & (df_anonymise['semaine'] == semaine)]
            if not df_anonymise_j.empty:
                distance = calcul_distance_hausdorff(df_i_semaine[['long', 'lat']], df_anonymise_j[['long', 'lat']])
                if distance < min_distance:
                    min_distance = distance
                    correspondant_id = id_anonyme

        return vrai_id, semaine, correspondant_id
        
    t0 = time.time()
    correspondences = pd.DataFrame(columns=['id_o', 'semaine', 'id_x'])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for vrai_id in df_original['id'].unique():
            for semaine in range(10, 21):
                futures.append(executor.submit(process_semaine, vrai_id, semaine))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                vrai_id, semaine, correspondant_id = result
                print(f"Id réel {vrai_id} -- semaine 2015-{semaine} -- Id anonyme {correspondant_id}")
                df_anonymise = df_anonymise[df_anonymise['id'] != correspondant_id]
                correspondences = pd.concat([pd.DataFrame({'id_o': vrai_id, 'semaine': '2015-' + str(semaine),
                                                           'id_x': correspondant_id},
                                                          columns=correspondences.columns, index=[0]),
                                             correspondences],
                                            ignore_index=True)

    print("Temps écoulé : ", time.time() - t0)
    correspondences.to_csv(nom_fichier + '.csv', index=False)



def correlation(df_original, df_anonymise, nom_fichier, remove_found=True, is_frangipane=False, threeshold=0.5):
    '''
    Fonction : L'idée de cet algorithme est d'analyser la corrélation entre trajectoires.
    Par exemple, pour l'id réel 1, on va construire l'ensemble de coordonnées par semaine, et puis on va analyser
    la similitude avec les données de chaque id anonyme.
    Faudrait prioriser dans l'ordre : la trajectoire - la semaine
    '''
    # Initialisations
    pd.DataFrame(columns=['id_o', 'semaine', 'id_x', 'dissimilarite']).to_csv(nom_fichier+'.csv', header=True, index=False)
        
    def calcul_dissimilarite_avec_ids_anonymes(df_i_semaine):
        t0 = time.time()
        nonlocal df_anonymise
        def calcul_distance_hausdorff(id_anon, trajectoire1, trajectoire_anon, dissimilarites):
            if not is_frangipane:
                dissimilarite = max(directed_hausdorff(trajectoire1, trajectoire_anon)[0], directed_hausdorff(trajectoire_anon, trajectoire1)[0])
            else :
                dissimilarite = max(directed_hausdorff(trajectoire1[['long']], trajectoire_anon[['long']])[0], directed_hausdorff(trajectoire_anon[['long']], trajectoire1[['long']])[0])
            
            dissimilarites[id_anon] = dissimilarite
                        
        semaine = df_i_semaine['semaine'].iloc[0]
        id_original = df_i_semaine['id'].iloc[0]
        
        dissimilarites = {}
    
        df_anonymise[df_anonymise['semaine'] == semaine].groupby('id', group_keys=True).apply(
            lambda group: calcul_distance_hausdorff(id_anon=group['id'].iloc[0], trajectoire1=df_i_semaine[['long', 'lat']], 
                                                    trajectoire_anon=group[['long', 'lat']], dissimilarites=dissimilarites))
        
        if dissimilarites != {}:
            id_correspondance_probable = min(dissimilarites, key=dissimilarites.get)
        else:
            print(f"Id: {id_original} -- Semaine: {semaine} ####")
            return
        
        # Pas sûr
        if remove_found:
            df_anonymise = df_anonymise[df_anonymise['id'] != id_correspondance_probable]
        
        print(f"Id: {id_original} -- Semaine: {semaine} -- Idx: {id_correspondance_probable} -- Dissimilarite: {dissimilarites[id_correspondance_probable]}")
        df_correspondance = pd.DataFrame({
            'id_o': id_original,
            'semaine': semaine,
            'id_x': id_correspondance_probable,
            'dissimilarite': dissimilarites[id_correspondance_probable]
        }, index=[0])

        df_correspondance.to_csv(nom_fichier+'.csv', mode='a', header=False, index=False)
        print("Temps écoulé :", time.time() - t0)

    df_original.groupby(['id', 'semaine']).apply(calcul_dissimilarite_avec_ids_anonymes)
    


def similitudeMoyennes():
    return

def correspondanceNombreDeGps(df_original:pd.DataFrame, df_anonymise:pd.DataFrame, nom_fichier):
    data = {}
    correspondances = []

    def remplirData(group, data):
        data[group['id'].iloc[0]]=len(group)    
    df_anonymise.groupby(['id']).apply(remplirData, data=data)
    
    def trouveCorrespondant(df_i_semaine):
        nonlocal correspondances
        nonlocal data
        
        id_o = df_i_semaine['id'].iloc[0]
        semaine = df_i_semaine['semaine'].iloc[0]
        nb_lignes_id = len(df_i_semaine)
        
        for key in data:
            if data[key] == nb_lignes_id:
                correspondances.append({
                    'id_o': id_o,
                    'semaine': semaine,
                    'id_x': key,
                    'nbLignes': nb_lignes_id
                })
                data.pop(key)     
        return
    df_original.groupby(['id', 'semaine']).apply(trouveCorrespondant)
    print(data)
    pd.DataFrame(data=correspondances, columns=['id_o', 'semaine', 'id_x', 'nbLignes']).to_csv(nom_fichier+'.csv', header=True, index=False)
    return