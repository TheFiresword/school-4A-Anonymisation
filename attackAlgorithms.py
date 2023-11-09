import pandas as pd
import gc
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


def correlation(df_original, df_anonymise, nom_fichier):
    '''
    Fonction : L'idée de cet algorithme est d'analyser la corrélation entre trajectoires.
    Par exemple, pour l'id réel 1, on va construire l'ensemble de coordonnées par semaine, et puis on va analyser
    la similitude avec les données de chaque id anonyme.
    '''    
    # Initialisations
    pd.DataFrame(columns=['id', 'semaine', 'id_anonyme', 'dissimilarite']).to_csv(nom_fichier+'.csv', header=True, index=False)
    dic_dissimilarites = {'id': [], 'semaine': [], 'id_anonyme': [], 'dissimilarite' : []}
    
    # Transformation dates => semaines
    df_original['date'] = df_original['date'].dt.strftime('%Y-%U')
    df_anonymise['date'] = df_anonymise['date'].dt.strftime('%Y-%U')
    df_original.rename(columns={'date':'semaine'}, inplace=True)
    df_anonymise.rename(columns={'date':'semaine'}, inplace=True)
        
    def calcul_dissimilarite_avec_ids_anonymes(group):
        df_i_semaine = group
        semaine = group['semaine'].iloc[0]
        print("Semaine", semaine)
        
        for id_anonyme, df_anonymise_j in df_anonymise[df_anonymise['semaine'] == semaine].groupby('id'):              
            dissimilarite = directed_hausdorff(u=df_i_semaine[['long', 'lat']], v=df_anonymise_j[['long', 'lat']])[0]            
            dic_dissimilarites['id'].append(df_i_semaine['id'].iloc[0])
            dic_dissimilarites['semaine'].append(semaine)
            dic_dissimilarites['id_anonyme'].append(id_anonyme)
            dic_dissimilarites['dissimilarite'].append(dissimilarite)
            
        df_dissimilarites = pd.DataFrame(data=dic_dissimilarites)
        index_correspondance_probable = df_dissimilarites['dissimilarite'].idxmin()
        df_correspondance = df_dissimilarites.loc[index_correspondance_probable]
        df_correspondance.to_csv(nom_fichier+'.csv', mode='a', header=False, index=False)
        
        dic_dissimilarites['id'].clear()
        dic_dissimilarites['semaine'].clear()
        dic_dissimilarites['id_anonyme'].clear()
        dic_dissimilarites['dissimilarite'].clear()
        #dic_dissimilarites = {'id': [], 'semaine': [], 'id_anonyme': [], 'dissimilarite' : []}
    
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