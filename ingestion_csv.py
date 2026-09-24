import pandas as pd
from sqlalchemy import create_engine

moteur = create_engine('postgresql://postgres:admin@localhost:5432/postgres')

df = pd.read_csv('clients.csv')

df.to_sql('clients_bronze', con=moteur, if_exists='replace', index=False)
print("Succès : Version CSV ingérée !")