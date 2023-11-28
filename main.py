from joinAlgo import *
from ano_gps import *
from ano_id import *

fichier_a_anonymiser = 'minidata.csv'

data = bdd_to_df_init(fichier_a_anonymiser)
data = ano_par_grille(data, 1)
data = change_id(data)
df_to_csv(data, 'mini_test.csv')