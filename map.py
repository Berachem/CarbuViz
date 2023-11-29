import folium
import pandas as pd
from constants import COULEURS_CARBURANTS

#données
def drawMap(gasType) :
    gas_data = pd.read_csv("data/PrixCarburants_instantane.csv",sep=";")
    gas_name = gas_data["Carburants disponibles"]
    mask = (gas_name.str.contains(gasType).fillna(False))
    gas_data = gas_data[mask]

    #carte
    coords = (47.0,2.0)
    map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=5.0)

    folium.Choropleth(
        geo_data="data/departements.geojson",                    # geographical data
        name='choropleth',
        data=gas_data,                                           # numerical data
        columns=['code_departement',gasType+'_prix'],            # numerical data key/value pair
        key_on='feature.properties.code',                        # geographical property used to establish correspondance with numerical data
        fill_color=COULEURS_CARBURANTS[gasType][1],
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Prix essence'
    ).add_to(map)


    map.save(outfile='generated/map.html')


if __name__ == '__main__':
    drawMap("E10")