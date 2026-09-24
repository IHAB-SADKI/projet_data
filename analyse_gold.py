import pandas as pd
from sqlalchemy import create_engine

# 1. CONNEXION
moteur = create_engine('postgresql://postgres:admin@localhost:5432/postgres')

# 2. LECTURE (On utilise les données propres de la couche Silver)
df = pd.read_sql('clients_silver', con=moteur)

# 3. ANALYSE MÉTIER (Couche Gold)
# La fonction groupby() regroupe les données par ville.
# La fonction agg() (pour agrégation) permet de faire des calculs sur ces groupes :
# - On compte ('count') les 'id' pour savoir combien on a de clients par ville.
# - On fait la moyenne ('mean') des 'age' pour avoir l'âge moyen par ville.
df_gold = df.groupby('ville').agg(
    nombre_clients=('id', 'count'),
    age_moyen=('age', 'mean')
).reset_index()

# On arrondit l'âge moyen à un chiffre après la virgule pour faire plus propre
df_gold['age_moyen'] = df_gold['age_moyen'].round(1)

# 4. CHARGEMENT
# On sauvegarde ce tableau de statistiques dans une table finale
df_gold.to_sql('clients_gold', con=moteur, if_exists='replace', index=False)

print("Succès : Analyse terminée et sauvegardée dans la table Gold !")