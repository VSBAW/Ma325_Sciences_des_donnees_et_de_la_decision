# -*- coding: utf-8 -*-
"""
Created on Tue May  9 08:57:48 2023
@author: Valentin
"""
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

# Charger les données
dfx_country = pd.read_csv("indice_country.csv", delimiter=';')
dfx_party = pd.read_csv("indice_party.csv", delimiter=';')
dfx_epg = pd.read_csv("indice_epg.csv", delimiter=';')
dfy = pd.read_csv("votes_20.csv", delimiter=';')

# Fusionner les données des différents tableaux
dfx = pd.concat([dfx_country, dfx_party, dfx_epg], axis=1)

# Extraire les colonnes en tant que tableau
x = dfx.values
y = dfy.values.ravel()

# Fractionner les données en ensembles d'entraînement et de test
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Standardiser les données
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# Créer et entraîner le modèle de régression logistique
model = LogisticRegression(solver='liblinear', random_state=0)
model.fit(x_train, y_train)

# Prédire les votes à partir des données de test
y_pred = model.predict(x_test)

# Évaluation du modèle
print("Score de précision :", model.score(x_test, y_test))

# Matrice de confusion
confusion = confusion_matrix(y_test, y_pred)
print("Matrice de confusion :")
print(confusion)

# Rapport de classification
classification = classification_report(y_test, y_pred)
print("Rapport de classification :")
print(classification)

# Récupérer les coefficients de régression spécifiques à chaque variable
coeff_country = model.coef_[0][:dfx_country.shape[1]]
coeff_party = model.coef_[0][dfx_country.shape[1]:dfx_country.shape[1] + dfx_party.shape[1]]
coeff_epg = model.coef_[0][dfx_country.shape[1] + dfx_party.shape[1]:]

# Tracer le graphique des coefficients de régression pour les pays
countries = ['Poland', 'Bulgaria', 'Italy', 'Malta', 'Spain', 'United Kingdom', 'Sweden', 'France', 'Portugal', 'Latvia', 'Germany', 'Greece', 'Belgium', 'Estonia', 'Hungary', 'Romania', 'Denmark', 'Lithuania', 'Netherlands', 'Slovakia', 'Austria', 'Czech Republic', 'Slovenia', 'Croatia', 'Ireland', 'Cyprus', 'Luxembourg', 'Finland']
plt.figure(figsize=(10, 6))
plt.bar(countries, coeff_country)
plt.xlabel('Pays')
plt.ylabel('Coefficient de régression')
plt.title("Influence des pays sur la prédiction du vote")
plt.xticks(rotation=90)
plt.show()
