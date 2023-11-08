from function import *



# FICHIER 385
chargerDATAorigin("0riginal", "dforigin")
chargerDATAvictime("Ano_385", "dfvictim385")
createJoin("dforigin.csv", "dfvictim385.csv", "jointure385")
createcouple("jointure385.csv", "resultat385")
maxresponse("resultat385.csv", "final385")
generatejson("final385.csv", "attack385")
idmanquant("attack385.json", "attfin385")

# FICHIER 407
chargerDATAvictime("Ano_407", "dfvictim407")
createJoin("dforigin.csv", "dfvictim407.csv", "jointure407")
createcouple("jointure407.csv", "resultat407")
maxresponse("resultat407.csv", "final407")
generatejson("final407.csv", "attack407")
idmanquant("attack407.json", "attfin407")

# FICHIER 468
chargerDATAvictime("Ano_468", "dfvictim468")
createJoin("dforigin.csv", "dfvictim468.csv", "jointure468")
createcouple("jointure468.csv", "resultat468")
maxresponse("resultat468.csv", "final468")
generatejson("final468.csv", "attack468")
idmanquant("attack468.json", "attfin468")