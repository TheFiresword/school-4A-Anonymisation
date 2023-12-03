from joinAlgo import *
from ano_gps import *
from ano_id import *
import numpy as np

fichier_a_anonymiser = 'bdd/minidata'

data = bdd_to_df_init(fichier_a_anonymiser)
data = ano_par_grille(data, 1)
data = change_id(data)
data['date'] = data['date'] + pd.to_timedelta(np.random.randint(60, size=len(data)), unit='s') # randomiser les secondes
# data = remplacer_positions_exceptionnelles (data)
df_to_csv(data, 'bdd/testgpd.csv')