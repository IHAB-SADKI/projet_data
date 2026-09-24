import pandas as pd
from sqlalchemy import create_engine

moteur = create_engine('postgresql://postgres:admin@localhost:5432/postgres')

data = {
    'id': [1, 2, 3],
    'nom': ['Dupont', 'Martin', 'Durand'],
    'age': [34, 45, 28],
    'ville': ['Paris', 'Lyon', 'Marseille']
}
df = pd.DataFrame(data)

df.to_sql('clients_bronze', con=moteur, if_exists='replace', index=False)
print("Succès : Version manuelle ingérée !")