import xmltodict
import pandas as pd

def convert_xml_to_csv(xml_file_path, csv_file_path):
    """
    Convertir un fichier XML en un fichier CSV.
    :param xml_file_path: Chemin vers le fichier XML à convertir.
    :param csv_file_path: Chemin vers le fichier CSV à créer.
    :return: None
    """
    # Charger le fichier XML
    with open(xml_file_path, 'rb') as xml_file:
        xml_data = xml_file.read()

    # Convertir le XML en un dictionnaire Python
    data_dict = xmltodict.parse(xml_data, xml_attribs=True)

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
                    if "@nom" not in prix or "@id" not in prix or "@maj" not in prix or "@valeur" not in prix:
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

    # Créer un DataFrame pandas à partir de la liste de données
    df = pd.DataFrame(data_list)

    # Enregistrer le DataFrame au format CSV
    df.to_csv(csv_file_path, index=False, sep=';')

# Utilisation de la fonction avec des valeurs par défaut
convert_xml_to_csv(xml_file_path='PrixCarburants_instantane.xml', csv_file_path='data/PrixCarburants_instantane.csv')
convert_xml_to_csv(xml_file_path='PrixCarburants_annuel_2023.xml', csv_file_path='data/PrixCarburants_annuel_2023.csv')
convert_xml_to_csv(xml_file_path='PrixCarburants_annuel_2022.xml', csv_file_path='data/PrixCarburants_annuel_2022.csv')















    
    