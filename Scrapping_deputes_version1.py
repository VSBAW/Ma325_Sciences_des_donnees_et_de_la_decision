# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 11:34:52 2023

@author: Valentin
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np

url = "https://www.europarl.europa.eu/meps/fr/full-list/xml/a"
response = requests.get(url)
soup = BeautifulSoup(response.text, "xml")
deputes_ids = []
deputes_names = []
deputes_bd=[]
deputes_age=[]
annee_actuelle = datetime.now().year

#On scrappe tous les id des deputes afin de pouvoir acceder a leur page respective via l url
for depute_id in soup.find_all("id"):
    deputes_ids.append(depute_id.get_text())

#On scrappe tous les noms complets des deputes pour le fun  
for depute_fullName in soup.find_all("fullName"):
    deputes_names.append(depute_fullName.get_text())

#On va scrapper une par une toutes les pages deputes grace a leurs id et on rcupere leur date de naissance
for i in deputes_ids:
    #print(i)
    url = "https://www.europarl.europa.eu/meps/fr/"+str(i)
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    depute_bd = soup.find("time", {"class": "sln-birth-date"})
    if depute_bd:
        bd=depute_bd.get_text().strip()
        annee_naissance=bd[-4:]
        print(annee_naissance)
        age=annee_actuelle-int(annee_naissance)
        print(bd)
    else:
        #si la date de naissance est pas affichee il y aura un None dans la liste
        bd, annee_naissance, age="None", "None", "None"
        print(bd)
    deputes_bd.append(bd)
    deputes_age.append(age)
        
    
    

#print(deputes_ids)
#print(deputes_names)
#print(len(deputes_ids))
#print(deputes_bd)
#print(len(deputes_bd))
#print(deputes_age)
#print(len(deputes_age))

recapitulatif=[deputes_ids,deputes_names,deputes_bd,deputes_age]
tableau_recapitulatif=np.transpose(recapitulatif)
print("\nVoici le tableau récapitulatif des donnees scrappees\n","\n(Nota :Si None est affiché, cela signifie que la donnee n'est pas accessible sur le site officiel des deputes, il faut aller la chercher autre part)",2*"\n",tableau_recapitulatif)


