from matplotlib.lines import Line2D
import pandas as pd
import numpy as np
import gc
import matplotlib.pyplot as plt

def processDonnees(fichier:str, supp_lignes_DEL=False, numeric_precision=2, nb_bits_id=16, chunks=False):
    '''
    Fonction : Clean les données de vérité
    Paramètres :
        - fichier :: nom du fichier csv ou l'url de son emplacement
        - numeric_precision :: Le nombre de chiffres après la virgule pour les champs de nombres réels
    '''
    df = None
    if chunks == False :
        df = pd.read_csv(fichier, delimiter= '\t')    
        df.columns = ["id","date", "long", "lat"]
        
        # On a assez de données pour se permettre de supprimer les lignes qui ont même un champ DEL
        if supp_lignes_DEL:
            df = df.loc[(df["id"] != "DEL") & (df["date"] != "DEL") & (df["long"] != "DEL") & (df["lat"] != "DEL")]
        
        id_type = np.int16 if (nb_bits_id == 16) else np.int32 if(nb_bits_id == 32) else str if (nb_bits_id==0) else np.int16
        columns_types = {'id' : id_type, 'date': str, 'long': np.float16, 'lat': np.float16}
        df = df.astype(columns_types)
                
        #df.round({'long':numeric_precision , 'lat':numeric_precision})
        df['long'] = df['long'].apply(lambda x : round(x, numeric_precision))
        df['lat'] = df['lat'].apply(lambda x : round(x, numeric_precision))
        print(df.head(5))
        return df
        
    else :
        df_list = []
        df = pd.read_csv(fichier, delimiter= '\t', chunksize=10000000)    
        for df_part in df:
            print(df_part.shape)
            df_part.columns = ["id","date", "long", "lat"]
        
            # On a assez de données pour se permettre de supprimer les lignes qui ont même un champ DEL
            if supp_lignes_DEL:
                df_part = df_part.loc[(df_part["id"] != "DEL") & (df_part["date"] != "DEL") & (df_part["long"] != "DEL") & (df_part["lat"] != "DEL")]
            
            id_type = np.int16 if (nb_bits_id == 16) else np.int32 if(nb_bits_id == 32) else str if (nb_bits_id==0) else np.int16
            columns_types = {'id' : id_type, 'date': str, 'long': np.float16, 'lat': np.float16}
            df_part = df_part.astype(columns_types)
                    
            #df_part.round({'long':numeric_precision , 'lat':numeric_precision})
            df_part['long'] = df_part['long'].apply(lambda x : round(x, numeric_precision))
            df_part['lat'] = df_part['lat'].apply(lambda x : round(x, numeric_precision))
            print(df_part.head(5))
            df_list.append(df_part)
        del df
        gc.collect()                
        return df_list


def visualiserDonnees(df : pd.DataFrame, id, chemin="Graphiques"):
    '''
    Fonction : Visualiser les données facilement
    , x_axis: str, y_axis: str, z_axis
    '''
    df = df[df['id'] == id]
    map_semaines_couleurs = {
        '2015-10' : 'b',
        '2015-11': 'g',
        '2015-12' : 'r',
        '2015-13' : 'c',
        '2015-14' : 'm',
        '2015-15' : 'y',
        '2015-16' : 'k',
        '2015-17' : 'purple',
        '2015-18' : 'orange',
        '2015-19' : 'pink',
        '2015-20' : 'brown'
    }
    semaines_coloriees = df['date'].dt.strftime('%Y-%U')
    semaines_coloriees = (semaines_coloriees.str.split('-').str[0] + '-' +
                    (semaines_coloriees.str.split('-').str[1].astype(int) + 1).astype(str))

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
    