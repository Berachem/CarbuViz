import folium
import pandas as pd

#colors
color = {
    "Gazole" : "YlOrBr",
    "SP95" : "BuGn",
    "E85" : "PuBu",
    "SP98" : "BuGn",
    "GPLc" : "Blues",
    "E10" : "Greens"
}

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
        columns=['code_departement',gasType+'_prix'],              # numerical data key/value pair
        key_on='feature.properties.code',                        # geographical property used to establish correspondance with numerical data
        fill_color=color[gasType],
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Prix essence'
    ).add_to(map)


    map.save(outfile='map.html')

drawMap("E10")