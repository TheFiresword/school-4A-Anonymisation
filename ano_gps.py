import pandas as pd
import numpy as np

def init_bdd_to_df (fichier):
    df = pd.read_csv(fichier, delimiter= '\t')
    df.columns = ["id","date", "longitude", "latitude"]
    return df

def df_to_csv (df, nom_csv):
    df.to_csv(nom_csv, index=False)

def bruiter_positions_gps (df):
    noise = np.random.uniform(-0.001, 0.001, size=len(df))
    df['latitude'] = df['latitude'] + noise
    df['longitude'] = df['longitude'] + noise
    return df

def arrondir_positions_gps (df):
    df = df.round({'latitude' : 3, 'longitude' : 3}) # arrondit au millième
    return df

def recentrer_positions_gps(df):

    ecart_moyenne = 1 # modifiable ici

    moyenne_latitude = df['latitude'].mean()    # 45,78
    moyenne_longitude = df['longitude'].mean()  # 4,879
    min_lat = moyenne_latitude - ecart_moyenne
    max_lat = moyenne_latitude + ecart_moyenne
    min_lon = moyenne_longitude - ecart_moyenne
    max_lon = moyenne_longitude + ecart_moyenne
    
    lat_moins = len(df[df['latitude'] < min_lat])
    lat_plus = len(df[df['latitude'] > max_lat])
    long_moins = len(df[df['longitude'] < min_lon])
    long_plus = len([df['longitude'] > max_lon])
    nb_lignes_hors_zone = lat_moins + lat_plus + long_moins + long_plus
    
    print (nb_lignes_hors_zone)

    # a finir

    # effacer les lignes en dehors de la zone

def creer_grille (df):
    
    moyenne_latitude = df['latitude'].mean()    # 45,78
    moyenne_latitude = moyenne_latitude.round(2)
    moyenne_longitude = df['longitude'].mean()  # 4,87
    moyenne_longitude = moyenne_longitude.round(2)

    print (moyenne_longitude, moyenne_latitude)

    # tableau des centres des carrés (long, lat)

    rows = 20
    cols = 5
    #dictionnaire_coords = {(i, j): (i * 5, j * 5) for i in range(rows) for j in range(cols)}
    #print(dictionnaire_coords)

    for j in range (10, -11, -1):
        for i in range (-10, 11, 1):
            dictionnaire = {(i,j): (moyenne_longitude + i*0.01, moyenne_latitude + i*0.01)}
            print (dictionnaire)


    

    
    return df







# mettre les id en random