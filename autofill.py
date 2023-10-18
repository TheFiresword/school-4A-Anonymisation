import pandas as pd
victim1 = pd.read_csv("S_user_34_be49cdd8d6cffccceecf45eb1f9d2fec3260d3bfa736ae390a61614b2a9f7914", delimiter= '\t')

nom_column = ["id_x","date", "lont", "lat"]

victim1.columns = nom_column
victim1clean = victim1.loc[victim1["id_x"] != "DEL"]

origin = pd.read_csv("0riginal", delimiter= '\t')
origin.columns = ["id_o","date", "lont", "lat"]
origin[["lont", "lat"]] = origin[["lont", 'lat']].round(2)
#origin.to_csv("new_origin.csv", index=False)
origin['lont'] = origin['lont'].astype('str')
origin['lat'] = origin['lat'].astype('str')

# test = pd.merge(origin, victim1clean, on='date')
test = origin.merge(victim1clean, on=['date', 'lont', 'lat'], suffixes=('_df1', '_df2'))
test.to_csv("test.csv", index=False)
