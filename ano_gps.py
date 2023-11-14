import pandas as pd
import numpy as np


def bruiter_positions_gps (fichier):
    df = pd.read_csv(fichier, delimiter= '\t')
    df.columns = ["id","date", "longitude", "latitude"]

    # bruiter les données gps de façon aléatoire :
    noise = np.random.uniform(-0.001, 0.001, size=len(df))
    df['latitude'] = df['latitude'] + noise
    df['longitude'] = df['longitude'] + noise

    # arrondir au millième les données gps
    df = df.round({'latitude' : 3, 'longitude' : 3})

    # creer le csv
    df.to_csv('donnees_anonymisees.csv', index=False)


bruiter_positions_gps("minimal")