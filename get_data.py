import os
from urllib import request
from zipfile import ZipFile
import xmltodict
import pandas as pd
import ssl

def isRealPrice(price):
    return price>0.05 and price<9 # on considère que les prix en dessous de 5 centimes et au dessus de 9 euros sont des erreurs
 
def convert_xml_to_csv(xml_file_path, csv_file_path):
    """
    Convertir un fichier XML en un fichier CSV.
    :param xml_file_path: Chemin vers le fichier XML à convertir.
    :param csv_file_path: Chemin vers le fichier CSV à créer.
    :return: None
    """
    print("Conversion du fichier XML en CSV en cours...")
    
    # Charger le fichier XML
    with open(xml_file_path, 'rb') as xml_file:
        xml_data = xml_file.read()
    
    # Convertir le XML en un dictionnaire Python
    data_dict = xmltodict.parse(xml_data, xml_attribs=True)
    
    # Nombre de points de vente 
    #total_rows = len(data_dict['pdv_liste']['pdv'])
    #processed_rows = 0
    
    # Extraire les données pertinentes du dictionnaire
    data_list = []
    for point_de_vente in data_dict['pdv_liste']['pdv']:
        adresse = point_de_vente['adresse'].replace('`', "'")
        ville = point_de_vente['ville'].replace('`', "'")
        
        id = point_de_vente['@id']
        
        if "@latitude" in point_de_vente and "@longitude" in point_de_vente and point_de_vente['@latitude'] and point_de_vente['@longitude']:
            latitude = float(point_de_vente['@latitude']) / 100000
            longitude = float(point_de_vente['@longitude']) / 100000

            if "prix" in point_de_vente and point_de_vente['prix'] is not None:
                for prix in point_de_vente['prix']:
                    if "@nom" not in prix or "@id" not in prix or "@maj" not in prix or "@valeur" not in prix or not isRealPrice(float(prix['@valeur'])):
                        continue
                    nom_carburant = prix['@nom']
                    maj_carburant = prix['@maj']
                    valeur_carburant = prix['@valeur']

                    data_list.append({
                        'id': id,
                        'ville': ville,
                        'adresse': adresse,
                        'latitude': latitude,
                        'longitude': longitude,
                        'nom_carburant': nom_carburant,
                        'date': maj_carburant,
                        'valeur_carburant': valeur_carburant
                    })
        # Mettre à jour le compteur de lignes traitées
        #processed_rows += 1
        
        # Calculer le pourcentage d'exécution
        #completion_percentage = (processed_rows / total_rows) * 100
        #print(f"Progression : {completion_percentage:.2f}%")

    # Créer un DataFrame pandas à partir de la liste de données
    df = pd.DataFrame(data_list)
    
    
    # Si le chemin vers les dossiers parents du chemin vers le fichier CSV n'existe pas, on le crée
    if not os.path.exists(os.path.dirname(csv_file_path)):
        os.makedirs(os.path.dirname(csv_file_path))
        

    # Enregistrer le DataFrame au format CSV
    df.to_csv(csv_file_path, index=False, sep=';')
    os.remove(xml_file_path) # Supprimer le fichier XML pour économiser de l'espace disque
    print("Conversion terminée ! (fichier CSV enregistré dans le dossier data/)")
    
    
 
 
def download_and_extract_zip_file(url, zip_file_path):
    """Download and extract a zip file from an URL."""
    # Download the zip file from the URL
    request.urlretrieve(url, zip_file_path)
    
    # si le lien contient une année, on affiche le message suivant
    if "annee" in url:
        print('Téléchargement des fichiers de données de l\'année', url[-4:], 'depuis l\'API en cours...')
    else :
        print('Téléchargement des fichiers de données en temps réel depuis l\'API en cours...')

    # Extract the zip file
    with ZipFile(zip_file_path, 'r') as zip:
        zip.extractall()
    
    # Remove the zip file
    os.remove(zip_file_path)
    print('Téléchargement de données terminé !')

def download_csv(url,file) :
    print("[INFO] téléchargement des données instantanées")
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with request.urlopen(req,context=context) as response, open(file, 'wb') as output_file:
        output_file.write(response.read())
        
if __name__ == '__main__':
    print("[INFO] Le téléchargement des données peut prendre plusieurs minutes si vous avez une connexion lente.")
    download_and_extract_zip_file(url="https://donnees.roulez-eco.fr/opendata/annee/2022", zip_file_path='donneesCompressees.zip')
    convert_xml_to_csv(xml_file_path='PrixCarburants_annuel_2022.xml', csv_file_path='data/PrixCarburants_annuel_2022.csv')

    download_csv("https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/csv?lang=fr&timezone=Europe%2FParis&use_labels=true&delimiter=%3B",'data/PrixCarburants_instantane.csv')
    print("[INFO] fin du téléchargement des données")

    #download_and_extract_zip_file(url="https://donnees.roulez-eco.fr/opendata/instantane", zip_file_path='donneesCompressees2.zip')
    #convert_xml_to_csv(xml_file_path='PrixCarburants_instantane.xml', csv_file_path='data/PrixCarburants_instantane.csv')

    # Utilisation de la fonction avec des valeurs par défaut
    #convert_xml_to_csv(xml_file_path='PrixCarburants_instantane.xml', csv_file_path='data/PrixCarburants_instantane.csv')
    #convert_xml_to_csv(xml_file_path='PrixCarburants_annuel_2023.xml', csv_file_path='data/PrixCarburants_annuel_2023.csv')
    