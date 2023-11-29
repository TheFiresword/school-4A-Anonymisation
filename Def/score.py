from metrics import pointsOfInterest, hour, meet, date, distance, tuile
import numpy as np


def calculScore(originial_f, anonymise_f):
    metrics = []
    for metric in [pointsOfInterest, hour, meet, date, distance, tuile]:
        metrics.append(metric.main(originial_f, anonymise_f))
    return metrics


import pandas as pd

# Charger la base de données
dataframe = pd.read_csv('../../User/sous_ensemble_1.csv_final.csv', header=None)
dataframe2 = pd.read_csv('../../User/sous_ensemble_1.csv', header=None)

# Supprimer la première ligne (l'en-tête)
dataframe = dataframe.iloc[1:]
dataframe2 = dataframe.iloc[1:]

# Réinitialiser les index
dataframe.reset_index(drop=True, inplace=True)
dataframe2.reset_index(drop=True, inplace=True)

# Enregistrer le DataFrame modifié dans un nouveau fichier CSV
dataframe.to_csv('test.csv', header=False, index=False)
dataframe.to_csv('test2.csv', header=False, index=False)
calculatedMetrics = calculScore("test2.csv", "test.csv")
score = np.mean(calculatedMetrics)
print(calculatedMetrics, "\n", score)