import pandas as pd

def chargerDATAvictime(fichier, nomdf):

    victim = pd.read_csv(fichier, delimiter='\t')
    nom_column = ["id_x","date", "lont", "lat"]
    victim.columns = nom_column
    victimclean = victim.loc[victim["id_x"] != "DEL"]
    victimclean.to_csv(nomdf + ".csv", index=False)

def chargerDATAorigin(fichier, nomdf):

    origin = pd.read_csv(fichier, delimiter= '\t')
    origin.columns = ["id_o","date", "lont", "lat"]
    origin[["lont", "lat"]] = origin[["lont", 'lat']].round(2)
    origin['lont'] = origin['lont'].astype('str')
    origin['lat'] = origin['lat'].astype('str')
    origin.to_csv(nomdf + ".csv", index=False)

def createJoin(fichierorigin, fichiervictim, nomjointure):

    origin = pd.read_csv(fichierorigin)
    victim = pd.read_csv(fichiervictim)

    jointure = origin.merge(victim, on=['date', 'lont', 'lat'], suffixes=('_df1', '_df2'))
    jointure.to_csv(nomjointure + ".csv", index=False)

def createcouple(fichierjointure, nbfichier):

    df = pd.read_csv(fichierjointure)
    df[['date', 'heure']] = df['date'].str.split(' ', n=1, expand=True)
    pair_counts = df.groupby(['id_o', 'date', 'id_x']).size().reset_index(name='count')
    pair_counts = pair_counts.sort_values(by='count', ascending=False)
    pair_counts.to_csv(nbfichier + '.csv', index=False)

def sortbymouth(fichierresult, fichierfinal):

    df = pd.read_csv(fichierresult)
    df['date'] = pd.to_datetime(df['date'])

    # Grouper par semaine
    df['date'] = df['date'].dt.to_period('W-TUE')
    # Compter les occurrences de lignes dupliquées pour chaque semaine
    counts = df[df.duplicated()].groupby(['id_o', 'date', 'id_x']).size().reset_index(name='count')


    counts.to_csv(fichierfinal+'.csv', index=False)



