from functions import *

LyonGps =(45.75, 4.85)
BordeauxGps = (44.837789,-0.57918)
ParisGps = (48.866667,2.333333)
ToulouseGps = (43.6,1.43)
Nbdiv = 100
echelle = 0.001
diametre = Nbdiv*echelle/2

Lyon = CreationCarte(LyonGps[0], LyonGps[1], echelle, Nbdiv)
Bordeaux = CreationCarte(BordeauxGps[0],BordeauxGps[1], echelle, Nbdiv)
Paris = CreationCarte(ParisGps[0],ParisGps[1], echelle, Nbdiv)
Toulouse = CreationCarte(ToulouseGps[0], ToulouseGps[1], echelle, Nbdiv)

df = pd.read_csv("merged_data.csv")

for index, row in df.iterrows():
        if not(LyonGps[0]-diametre <= row["lat"] <= LyonGps[0] +diametre and LyonGps[1]-diametre <= row["lont"] <= LyonGps[1]+diametre):
            if not(BordeauxGps[0]-diametre <= row["lat"] <= BordeauxGps[0] +diametre and BordeauxGps[1] -diametre <= row["lont"] <=  BordeauxGps[1] +diametre):
                if not(ParisGps[0]-diametre <= row["lat"] <= ParisGps[0] +diametre and ParisGps[1] -diametre <= row["lont"] <=  ParisGps[1] + diametre):
                    if not(ToulouseGps[0]-diametre <= row["lat"] <= ToulouseGps[0] +diametre and ToulouseGps[1] -diametre <= row["lont"] <=  ToulouseGps[1] + diametre):
                        df.at[index, 'id_x'] = "DEL"
                         