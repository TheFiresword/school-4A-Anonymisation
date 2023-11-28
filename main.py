from joinAlgo import *
from ano_gps import *
from ano_id import *

fichier_a_anonymiser = '../bdd/0riginal'

data = bdd_to_df_init(fichier_a_anonymiser)
data_gps = ano_par_grille(data, 1) # precision = 1 pour avoir 4000 cases
data_gps_id = change_id(data_gps)
df_to_csv(data_gps_id, '../bdd/ano1.csv')