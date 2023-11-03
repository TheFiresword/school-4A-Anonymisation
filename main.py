from joinAlgo import *
df = pd.read_csv('truth_ground.csv', delimiter= '\t')
df.columns = ["id_o","date", "long", "lat"]

#=====================================================
# Attaque contre Autofill
#=====================================================
df_anonyme = nettoyerDonneesAnonymisees('Autofill/submit1')
appliquerAlgorithme(df, df_anonyme, 'Autofill/Xsubmit1')
genererJson('Autofill/Xsubmit1.csv', 'Autofill/Xsubmit1_1')



# FICHIER 92
#chargerDATAorigin("0riginal", "dforigin")
#chargerDATAvictime("S_user_59_92898742d7129cbbf413724f301c258730b979188310cebca9d06ab58c7f5ae0", "dfvictim92")
#createJoin("dforigin.csv", "dfvictim92.csv", "jointure92")
#createcouple("jointure92.csv", "resultat92")
#maxresponse("resultat92.csv", "final92")
#generatejson("final92.csv", "attack92")

# FICHIER a5
# chargerDATAvictime("S_user_59_a5f2ff1b47e658792f3919d1fd0c04571f4ebff75bfcc74121b7a1429613d49d", "dfvictima5")
# createJoin("..\dforigin.csv", "dfvictima5.csv", "jointurea5")
# createcouple("jointurea5.csv", "resultata5")
# maxresponse("resultata5.csv", "finala5")
# generatejson("finala5.csv", "attacka5")

# Fichier a3
# chargerDATAvictime("S_user_59_a365473ee4db27f1b72c6e2c72e0875c508afba82c1511e3501a5f82e58f564a", "dfvictima3")
# createJoin("..\dforigin.csv", "dfvictima3.csv", "jointurea3")
# createcouple("jointurea3.csv", "resultata3")
# maxresponse("resultata3.csv", "finala3")
# generatejson("finala3.csv", "attacka3")

