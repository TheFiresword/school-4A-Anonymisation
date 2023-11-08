from joinAlgo import *

truth_file_url = "https://drive.usercontent.google.com/download?id=1KE4dJ_ArA7jhIUYmzITIYO7Yh60rQ0-K&export=download&authuser=2&confirm=t&uuid=5b074238-7709-408b-ac93-86cf839cdb07&at=APZUnTXJHY4NiV5TeGbmEtE-F6Ip:1699105244012"

# Charger le fichier de vérité dans un dataframe sans le télécharger
df = processDonnees("../bdd/0riginal")

#=====================================================
# Attaques contre anonym212
#=====================================================

#df_anonyme = processDonnees("../bdd/anonym212_2", supp_lignesDEL=True)    #enleve les DEL
#appliquerAlgorithme(df, df_anonyme, '../bdd/anonym212_2')                 #crée le csv
genererJson('../bdd/anonym212-2.csv', '../bdd/anonym212_2X')               #crée json avec id dispos
idmanquant('../bdd/anonym212-2X.json', '../bdd/anonym212_2_final')         #json final avec tous les id