from attackAlgorithms import *
from utils import *
import concurrent.futures

truth_file_url = "https://drive.usercontent.google.com/download?id=1KE4dJ_ArA7jhIUYmzITIYO7Yh60rQ0-K&export=download&authuser=2&confirm=t&uuid=5b074238-7709-408b-ac93-86cf839cdb07&at=APZUnTXJHY4NiV5TeGbmEtE-F6Ip:1699105244012"

# Charger le fichier de vérité dans un dataframe sans le télécharger
#df = processDonnees("truth_ground.csv")
#df_a = df.loc[:10000000]
#for i in range(107, 113):
#    visualiserDonnees(df=df, id=i)

#=====================================================
# Attaques contre Autofill
#=====================================================

#----------------------Submit476------------------------#
url476 = "https://drive.usercontent.google.com/download?id=1Ax-jMGrXq4Sr3mOm-Lb5O1BdX9FvVYHt&export=download&authuser=2&confirm=t&uuid=7c2d786f-82f2-4cac-ab2b-fcc70752af6d&at=APZUnTXkqE9yATPVDqbZ0db14lyD:1699105490973"
#df_anonyme = processDonnees("Autofill/submit476.csv", supp_lignes_DEL=True)
#jointureNaive(df, df_anonyme, 'Autofill/Xsubmit476')
#genererJson('Autofill/Xsubmit476.csv', 'Autofill/Xsubmit476_2')

#----------------------Submit449------------------------#
url449 = "https://drive.usercontent.google.com/download?id=1jsjcmkfZem_MdU9dNotDUyJZWbyPTkNm&export=download&authuser=2&confirm=t&uuid=aaf77d2b-a0ef-453b-861f-9196ba3681dc&at=APZUnTVBQKtbBFQWxXJqg_HvIqQo:1699105534254"
#url449="Autofill/submit449.csv"
#df_anonyme = processDonnees(url449, supp_lignes_DEL=True)
#jointureNaive(df, df_anonyme, 'Autofill/Xsubmit449')
#genererJson('Autofill/Xsubmit449.csv', 'Autofill/Xsubmit449_2')

#----------------------Submit444------------------------#
url444="https://drive.usercontent.google.com/download?id=1DFlw-8TN2AG-kzu4GJEyZsi_OClL9wWB&export=download&authuser=2&confirm=t&uuid=00612a48-2c8e-4f9f-b274-ef9869221653&at=APZUnTXKPViLvNlu8kz9NQTgUuxu:1699105432050"
#url444="Autofill/submit444.csv"
#df_anonyme = processDonnees(url444, supp_lignes_DEL=True)
#jointureNaive(df, df_anonyme, 'Autofill/Xsubmit444')
#genererJson('Autofill/Xsubmit444.csv', 'Autofill/Xsubmit444_1')


#=====================================================
# Attaques contre Autofill
#=====================================================


#----------------------Submit michel lardon------------------------#
#df_anonyme = processDonnees("Michel Lardon/submit498.csv", supp_lignes_DEL=True)
#jointureNaive(df, df_anonyme, 'Michel Lardon/Xsubmit498')
#genererJson('Michel Lardon/Xsubmit498.csv', 'Michel Lardon/Xsubmit498_1')


#----------------------Submit pocochocambo------------------------#
#df_anonyme = processDonnees("pocochocambo/submit434.csv", supp_lignes_DEL=True)
#print(df_anonyme['id'].unique().size)
#for id_x in df_anonyme['id'].unique() :
#    visualiserDonnees(df=df_anonyme, id=id_x, chemin="pocochocambo/images")
#jointureNaive(df, df_anonyme, 'pocochocambo/Xsubmit352')
#correlation(df, df_anonyme, "pocochocambo/Xsubmit352_1")

#similitudeTrajectoires(df, df_anonyme, f"pocochocambo/Xsubmit434_part")
#genererJson('pocochocambo/Xsubmit434_1.csv', 'pocochocambo/Xsubmit434_2')


#----------------------Submit dazc------------------------#
#df_anonyme = processDonnees("dazc/submit467.csv", supp_lignes_DEL=True, numeric_precision=2, nb_bits_id=0)
#similitudeTrajectoires(df, df_anonyme, f"dazc/Xsubmit467_2")

#----------------------Submit anonym------------------------#
#df_anonyme = processDonnees("anonym/submit468.csv", supp_lignes_DEL=True, numeric_precision=2)
#print(df_anonyme['id'].unique().size)
#for id_x in df_anonyme['id'].unique() :
#    visualiserDonnees(df=df_anonyme, id=id_x, chemin="pocochocambo/images")
#jointureNaive(df, df_anonyme, 'anonym/Xsubmit468')
#correlation(df, df_anonyme, "pocochocambo/Xsubmit352_1")
#genererJson('anonym/Xsubmit468.csv', 'anonym/Xsubmit468_1', incr_semaines=True)

#----------------------Submit the------------------------#
#df_anonyme = processDonnees("the/submit309.csv", supp_lignes_DEL=True, numeric_precision=2)
#print(df_anonyme['id'].unique().size)
#for id_x in df_anonyme['id'].unique() :
#    visualiserDonnees(df=df_anonyme, id=id_x, chemin="pocochocambo/images")
#jointureNaive(df, df_anonyme, 'the/Xsubmit309')
#correlation(df, df_anonyme, "pocochocambo/Xsubmit352_1")
#genererJson('the/Xsubmit309.csv', 'the/Xsubmit309_1', incr_semaines=True)

#----------------------Submit alanozy------------------------#
#df_anonyme = processDonnees("alanozy/submit546.csv", supp_lignes_DEL=True, numeric_precision=2, nb_bits_id=0)
#print(df_anonyme['id'].unique().size)
#for id_x in df_anonyme['id'].unique() :
#    visualiserDonnees(df=df_anonyme, id=id_x, chemin="pocochocambo/images")
#jointureNaive(df, df_anonyme, 'alanozy/Xsubmit546')
#correlation(df, df_anonyme, "pocochocambo/Xsubmit352_1")
#genererJson('alanozy/Xsubmit546.csv', 'alanozy/Xsubmit546_1', incr_semaines=True)

#----------------------Submit thathack------------------------#
#df_anonyme = processDonnees("thathack/submit356.csv", supp_lignes_DEL=True, numeric_precision=2)
#print(df_anonyme['id'].unique().size)
#for id_x in df_anonyme['id'].unique() :
#    visualiserDonnees(df=df_anonyme, id=id_x, chemin="pocochocambo/images")
#jointureNaive(df, df_anonyme, 'thathack/Xsubmit356')
#correlation(df, df_anonyme, "thathack/Xsubmit356_1")
#genererJson('thathack/Xsubmit356.csv', 'thathack/Xsubmit356_1', incr_semaines=True)


#----------------------Auto attaques------------------------#
#df = processDonnees("partieDefense/file1.csv")
#df = processDonnees("truth_ground.csv")
#df_anonyme = processDonnees("partieDefense/anonym3.csv", supp_lignes_DEL=True, numeric_precision=2, nb_bits_id=0)
#jointureNaive(df, df_anonyme, f"partieAttaque/autoAttaques/sub1")
#genererJson('partieAttaque/autoAttaques/sub1.csv', 'partieAttaque/autoAttaques/sub1', incr_semaines=True)


#----------------------Submit Frangipane------------------------#

df_anonyme = processDonnees("partieAttaque/Cyberwardens/submit672.csv", supp_lignes_DEL=True, numeric_precision=3, nb_bits_id=0)
df = processDonnees("truth_ground.csv", numeric_precision=3)
jointureNaive(df, df_anonyme, f"partieAttaque/Cyberwardens/Xsubmit672")
#correlation(df, df_anonyme, "partieAttaque/Cyberwardens/submit672_X")
genererJson('partieAttaque/Cyberwardens/Xsubmit672.csv', 'partieAttaque/Cyberwardens/submit672_3')

