from joinAlgo import *

truth_file_url = "https://drive.usercontent.google.com/download?id=1KE4dJ_ArA7jhIUYmzITIYO7Yh60rQ0-K&export=download&authuser=2&confirm=t&uuid=5b074238-7709-408b-ac93-86cf839cdb07&at=APZUnTXJHY4NiV5TeGbmEtE-F6Ip:1699105244012"

# Charger le fichier de vérité dans un dataframe sans le télécharger
df = processDonnees("../bdd/0riginal")

#=====================================================
# Attaques contre Autofill
#=====================================================

#----------------------Submit476------------------------#
url476 = "https://drive.usercontent.google.com/download?id=1Ax-jMGrXq4Sr3mOm-Lb5O1BdX9FvVYHt&export=download&authuser=2&confirm=t&uuid=7c2d786f-82f2-4cac-ab2b-fcc70752af6d&at=APZUnTXkqE9yATPVDqbZ0db14lyD:1699105490973"
#df_anonyme = processDonnees("Autofill/submit476.csv", suppLignesDEL=True)
#appliquerAlgorithme(df, df_anonyme, 'Autofill/Xsubmit476')
#genererJson('Autofill/Xsubmit476.csv', 'Autofill/Xsubmit476_2')

#----------------------Submit449------------------------#
url449 = "https://drive.usercontent.google.com/download?id=1jsjcmkfZem_MdU9dNotDUyJZWbyPTkNm&export=download&authuser=2&confirm=t&uuid=aaf77d2b-a0ef-453b-861f-9196ba3681dc&at=APZUnTVBQKtbBFQWxXJqg_HvIqQo:1699105534254"
url449="Autofill/submit449.csv"
#df_anonyme = processDonnees(url449, suppLignesDEL=True)
#appliquerAlgorithme(df, df_anonyme, 'Autofill/Xsubmit449')
#genererJson('Autofill/Xsubmit449.csv', 'Autofill/Xsubmit449_1')

#----------------------Submit444------------------------#
url444="https://drive.usercontent.google.com/download?id=1DFlw-8TN2AG-kzu4GJEyZsi_OClL9wWB&export=download&authuser=2&confirm=t&uuid=00612a48-2c8e-4f9f-b274-ef9869221653&at=APZUnTXKPViLvNlu8kz9NQTgUuxu:1699105432050"
#url444="Autofill/submit444.csv"
#df_anonyme = processDonnees(url444, suppLignesDEL=True)
#appliquerAlgorithme(df, df_anonyme, 'Autofill/Xsubmit444')
#genererJson('Autofill/Xsubmit444.csv', 'Autofill/Xsubmit444_1')


#=====================================================
# Attaques contre Autofill
#=====================================================

#----------------------Submit500------------------------#
url500="https://drive.usercontent.google.com/download?id=1EN5pk5goh-U71-WYg3m-a_nbJHk-133_&export=download&authuser=2&confirm=t&uuid=88ecc2fb-8fb3-44cf-b1ba-2b976eae9345&at=APZUnTU55wT12NPqijT_6xpLgmop:1699110725849"
#df_anonyme = processDonnees("Michel Lardon/submit500.csv", supp_lignesDEL=True, nb_bits_id=32)
#appliquerAlgorithme(df, df_anonyme, 'Michel Lardon/Xsubmit500')
#genererJson('Michel Lardon/Xsubmit500.csv', 'Michel Lardon/Xsubmit500_1')

#----------------------Submit499------------------------#




#=====================================================
# Attaques contre anonym212
#=====================================================

#df_anonyme = processDonnees("../bdd/anonym212 - 2", supp_lignesDEL=True)
#appliquerAlgorithme(df, df_anonyme, '../bdd/anonym212-2')
#genererJson('../bdd/anonym212-2.csv', '../bdd/anonym212-2X')
#idmanquant('../bdd/anonym212-2X.json', '../bdd/anonym212-2-final')