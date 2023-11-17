from joinAlgo import *
from ano_gps import *

# Charger le fichier de vérité dans un dataframe sans le télécharger
#df = processDonnees("../bdd/0riginal")

#=====================================================
# Attaques contre anonym212
#=====================================================

#df_anonyme = processDonnees("../bdd/anonym212_2", supp_lignesDEL=True)    #enleve les DEL
#appliquerAlgorithme(df, df_anonyme, '../bdd/anonym212_2')                 #crée le csv
#genererJson('../bdd/anonym212-2.csv', '../bdd/anonym212_2X')               #crée json avec id dispos
#idmanquant('../bdd/anonym212-2X.json', '../bdd/anonym212_2_final')         #json final avec tous les id

#=====================================================
# Defense
#=====================================================

fichier_a_anonymiser = '../bdd/minimal'

# initialise la bdd en dataframe et nomme les colonnes
data = bdd_to_df_init(fichier_a_anonymiser)
