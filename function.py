import pandas as pd
import json

def chargerDATAvictime(fichier, nomdf):

    victim = pd.read_csv(fichier, delimiter='\t')
    nom_column = ["id_x","date", "lont", "lat"]
    victim.columns = nom_column
    victim[["lont", "lat"]] = victim[["lont", 'lat']].round(3)
    victimclean = victim.loc[victim["id_x"] != "DEL"]
    victimclean.to_csv(nomdf + ".csv", index=False)

def chargerDATAorigin(fichier, nomdf):

    origin = pd.read_csv(fichier, delimiter= '\t')
    origin.columns = ["id_o","date", "lont", "lat"]
    origin[["lont", "lat"]] = origin[["lont", 'lat']].round(3)
    origin['lont'] = origin['lont'].astype('str')
    origin['lat'] = origin['lat'].astype('str')
    origin.to_csv(nomdf + ".csv", index=False)

def createJoin(fichierorigin, fichiervictim, nomjointure):

    origin = pd.read_csv(fichierorigin)
    victim = pd.read_csv(fichiervictim)

    jointure = origin.merge(victim, on=['date', 'lont', 'lat'])
    jointure.to_csv(nomjointure + ".csv", index=False)

def createcouple(fichierjointure, nbfichier):

    df = pd.read_csv(fichierjointure)
    df[['date', 'heure']] = df['date'].str.split(' ', n=1, expand=True)
    df['date'] = pd.to_datetime(df['date'])

    df['date'] = df['date'].dt.to_period('W')
    # Renommer les semaines avec un numéro particulier
    df['date'] = df['date'].dt.week

    # Renommer les semaines en utilisant un dictionnaire de correspondance
    numero_semaines = {10: '2015-10', 11: '2015-11', 12:'2015-12', 13: '2015-13', 14: '2015-14', 15: '2015-15', 16: '2015-16', 17: '2015-17', 18: '2015-18', 19: '2015-19', 20: '2015-20'}
    df['date'] = df['date'].map(numero_semaines)

    
    pair_counts = df.groupby(['id_o', 'date', 'id_x']).size().reset_index(name='count')
    pair_counts = pair_counts.sort_values(by='count', ascending=False)
    pair_counts.to_csv(nbfichier + '.csv', index=False)

def maxresponse(fichierresult, fichierfinal):

    df = pd.read_csv(fichierresult)


    idx = df.groupby(['id_o', 'date'])['count'].idxmax()

# Extraire ces lignes du DataFrame d'origine
    result = df.loc[idx].sort_values(by='count', ascending=False)

    # Réinitialiser les index si nécessaire
    result = result.reset_index(drop=True)


    result.to_csv(fichierfinal+'.csv', index=False)

def generatejson(fichierfinal, nomjson):
    df = pd.read_csv(fichierfinal)

    df = df.drop(columns=['count'])


    # Créer un dictionnaire pour stocker les données de sortie
    data = {}

    # Parcourir les lignes du DataFrame
    for index, row in df.iterrows():
        id_1 = row['id_o']
        semaine = row['date']
        id_2 = row['id_x']

        if id_1 not in data:
            data[id_1] = {}
        
        if semaine not in data[id_1]:
            data[id_1][semaine] = []
        
        data[id_1][semaine].append(id_2)


    # Convertir le dictionnaire en format JSON
    #output_json = json.dumps(data, indent=4, separators=(',', ':'))

    # Écrire le JSON résultant dans un fichier de sortie
    output_file = nomjson+'.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4, separators=(',', ':'))



def idmanquant(nomjson, nomjsonfinal):
    with open(nomjson, 'r') as json_file:
        data = json.load(json_file)

    semaines = {'2015-10':None, '2015-11':None,'2015-12':None,'2015-13':None,  '2015-14':None, '2015-15':None, '2015-16':None, '2015-17':None,'2015-18':None,'2015-19':None, '2015-20':None}


    ids_manquants = [str(i) for i in range(1, 108) if str(i) not in data]

    # Ajouter les clés manquantes avec des valeurs par défaut
    for id_manquant in ids_manquants:
        data[id_manquant] = semaines
        

    

    # Écrire le JSON résultant dans un fichier de sortie
    output_file = nomjsonfinal+'.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4, separators=(',', ':'))


