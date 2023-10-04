import os
from urllib import request
from zipfile import ZipFile
 
 
def download_and_extract_zip_file(url, zip_file_path):
    """Download and extract a zip file from an URL."""
    # Download the zip file from the URL
    request.urlretrieve(url, zip_file_path)

    # Extract the zip file
    with ZipFile(zip_file_path, 'r') as zip:
        zip.extractall()
        print('Extraction terminée')
    
    # Remove the zip file
    os.remove(zip_file_path)
        
download_and_extract_zip_file(url="https://donnees.roulez-eco.fr/opendata/annee/2022", zip_file_path='donneesCompressees.zip')
    