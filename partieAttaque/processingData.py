from matplotlib.lines import Line2D
import pandas as pd
import numpy as np
import gc
import matplotlib.pyplot as plt

def processDonnees(fichier:str, supp_lignes_DEL=False, numeric_precision=2, nb_bits_id=16, nrows=False, delimiter='\t', only_days=False):
        '''
        Fonction : Clean les données de vérité
        Paramètres :
            - fichier :: nom du fichier csv ou l'url de son emplacement
            - numeric_precision :: Le nombre de chiffres après la virgule pour les champs de nombres réels
        '''
        df = None
        df = pd.read_csv(fichier, delimiter= delimiter, header=None)  if nrows==False else pd.read_csv(fichier, delimiter= delimiter, header=None, nrows=nrows)
        
        df.columns = ["id","date", "long", "lat"]        
        # On a assez de données pour se permettre de supprimer les lignes qui ont même un champ DEL
        if supp_lignes_DEL:
            df = df.loc[(df["id"] != "DEL")  & (df["date"] != "DEL") & (df["long"] != "DEL") & (df["lat"] != "DEL")]
        
        df['semaine'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S").dt.isocalendar().week
        if only_days:
            df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S").dt.date            
            
        id_type = np.int16 if (nb_bits_id == 16) else np.int32 if(nb_bits_id == 32) else str if (nb_bits_id==0) else np.int16
        columns_types = {'id' : id_type, 'date': str, 'long': np.float32, 'lat': np.float32, 'semaine': np.int16}
        df = df.astype(columns_types)
        #print(df['id'], df['date'])
        #df.round({'long':numeric_precision , 'lat':numeric_precision})
        df['long'] = df['long'].apply(lambda x : round(x, numeric_precision))
        df['lat'] = df['lat'].apply(lambda x : round(x, numeric_precision))
        #df['lat'] = df['lat'].round(numeric_precision)
        print(df.head(5))
        return df


def visualiserDonnees(df : pd.DataFrame, id, chemin="Graphiques"):
    '''
    Fonction : Visualiser les données facilement
    , x_axis: str, y_axis: str, z_axis
    '''
    df = df[df['id'] == id]
    map_semaines_couleurs = {
        10 : 'b',
        11: 'g',
        12 : 'r',
        13 : 'c',
        14 : 'm',
        15 : 'y',
        16 : 'k',
        17 : 'purple',
        18 : 'orange',
        19 : 'pink',
        20 : 'brown'
    }
    semaines_coloriees = df['semaine']

    semaines_coloriees = semaines_coloriees.map(map_semaines_couleurs)
    longitudes = df['long']
    latitudes = df['lat']
    
    plt.figure(figsize=(10, 6))
    sc = plt.scatter(longitudes, latitudes, marker='o', c=semaines_coloriees)
    plt.title("Positions de l'id "+ str(id))
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    
    legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=semaine) 
                       for semaine, color in map_semaines_couleurs.items()]
    plt.legend(handles=legend_elements)
    plt.savefig(str(chemin) + '/id'+str(id)+'.png')
    