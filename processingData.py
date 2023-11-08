import pandas as pd
import numpy as np
import json

def processDonnees(fichier:str, supp_lignesDEL=False, numeric_precision=2, nb_bits_id=16):
    '''
    Fonction : Clean les données de vérité
    Paramètres :
        - fichier :: nom du fichier csv ou l'url de son emplacement
        - numeric_precision :: Le nombre de chiffres après la virgule pour les champs de nombres réels
    '''
    df = pd.read_csv(fichier, delimiter= '\t')
    print(df.head(5))
    df.columns = ["id","date", "long", "lat"]
    # On a assez de données pour se permettre de supprimer les lignes qui ont même un champ DEL
    if supp_lignesDEL:
        df = df.loc[(df["id"] != "DEL") & (df["date"] != "DEL") & (df["long"] != "DEL") & (df["lat"] != "DEL")]
    
    id_type = np.int16 if (nb_bits_id == 16) else np.int32 if(nb_bits_id == 32) else np.int16
    columns_types = {'id' : id_type, 'date': str, 'long': np.float16, 'lat': np.float16}
    df = df.astype(columns_types)
    
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S")
    df[["long", "lat"]] = df[["long", 'lat']].round(numeric_precision)
    return df

