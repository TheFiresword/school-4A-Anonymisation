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

# mettre les id en random