import pandas as pd
from faker import Faker
import random

def change_id(df : pd.DataFrame):
    fake = Faker()
    df['semaine'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S").dt.isocalendar().week
    df['id_x'] = df['id']
    df['id_x'] = df.groupby(['id', 'semaine'])['id_x'].transform(lambda serie : fake.name())
    #print(df.groupby(['id', 'semaine'])[['id_x']].first())
    return df[['id_x', 'date', 'longitude', 'latitude']]
