# Folium pour la carte interactive pour chaque station du fichier PrixCarburants_instantane.csv

import folium
import pandas as pd
import numpy as np


# Charger le DataFrame depuis le fichier CSV
df = pd.read_csv('data/PrixCarburants_instantane.csv', sep=';')

# Trier le DataFrame par nom de ville
df = df.sort_values(by='ville')

# Créer une carte centrée sur la France
m = folium.Map(location=[46.52863469527167, 2.43896484375], zoom_start=6)

# Regrouper les stations par ville
grouped = df.groupby('ville')

# Parcourir chaque groupe (ville)
for ville, group in grouped:
    # Créer un popup pour la ville
    html = f"<h3>{ville}</h3><ul>"
    
    # Parcourir chaque station de la ville
    for _, row in group.iterrows():
        adresse = row['adresse']
        carburant = row['nom_carburant']
        prix = row['valeur_carburant']
        
        # Ajouter le prix du carburant pour chaque station
        html += f"<li>{adresse} - {carburant}: {prix} €/L</li>"
    
    html += "</ul>"
    
    # Récupérer les coordonnées de la première station de la ville
    latitude = group['latitude'].values[0]
    longitude = group['longitude'].values[0]
    
    # Ajouter le marqueur à la carte pour la ville
    folium.Marker([latitude, longitude], popup=html).add_to(m)

# Afficher la carte
m.save('carte.html')
