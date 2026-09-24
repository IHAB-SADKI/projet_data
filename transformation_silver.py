# Importation des outils nécessaires
import pandas as pd # Pandas sert à manipuler les données sous forme de tableau
from sqlalchemy import create_engine # Permet de créer le pont entre Python et PostgreSQL

# 1. CONNEXION
# On crée le "moteur" pour se connecter à ta base de données locale
moteur = create_engine('postgresql://postgres:admin@localhost:5432/postgres')

# 2. EXTRACTION (Lecture)
# On ne lit plus le fichier CSV ! On va chercher les données brutes directement 
# dans la table "clients_bronze" de PostgreSQL
df = pd.read_sql('clients_bronze', con=moteur)

# 3. TRANSFORMATION (Le nettoyage - Couche Silver)

# a. Standardisation du texte
# On force une majuscule au début de chaque nom et de chaque ville.
# Cela transforme le "dupont" (ligne 4) en "Dupont", pour qu'il soit identique à la ligne 1.
df['nom'] = df['nom'].str.capitalize()
df['ville'] = df['ville'].str.capitalize()

# b. Suppression des doublons
# Maintenant que les "Dupont" sont écrits pareils, on supprime les lignes en double.
# On ignore la colonne 'id' car l'identifiant est différent (1 et 4).
df = df.drop_duplicates(subset=['nom', 'age', 'ville'])

# c. Gestion des valeurs manquantes (les trous)
# Durand n'a pas d'âge renseigné. On remplace ce vide (NaN) par le chiffre 0.
df['age'] = df['age'].fillna(0)


# 4. CHARGEMENT (Écriture)
# On envoie ce nouveau tableau tout propre dans une NOUVELLE table nommée "clients_silver".
# "if_exists='replace'" signifie que si on relance ce script, il écrasera l'ancienne table pour la mettre à jour.
df.to_sql('clients_silver', con=moteur, if_exists='replace', index=False)

print("Succès : Données nettoyées et sauvegardées dans la table Silver !")