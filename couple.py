import pandas as pd

dfbe = pd.read_csv("test.csv")
df = pd.read_csv("test72.csv")

df[['date', 'heure']] = df['date'].str.split(' ', n=1, expand=True)

pair_counts = df.groupby(['id_o', 'date', 'id_x']).size().reset_index(name='count')

pair_counts = pair_counts.sort_values(by='count', ascending=False)

pair_counts.to_csv('resultat72.csv', index=False)