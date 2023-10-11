import folium
import pandas as pd
import branca.colormap as cm

#données
gas_data = pd.read_csv("data/PrixCarburants_instantane.csv",sep=";")
gas_name = gas_data["Carburants disponibles"]
mask = (gas_name.str.contains("Gazole").fillna(False))
gas_data = gas_data[mask]

#carte
coords = (47.0,2.0)
map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=5.0)

colormap = cm.LinearColormap(['white', 'yellow'], vmin=min(gas_data['Gazole_prix']), vmax=max(gas_data['Gazole_prix']),caption="Prix de l'essence")

folium.Choropleth(
    geo_data="data/departements.geojson",                    # geographical data
    name='choropleth',
    data=gas_data,                                           # numerical data
    columns=['code_departement','Gazole_prix'],              # numerical data key/value pair
    key_on='feature.properties.code',                        # geographical property used to establish correspondance with numerical data
    style_function=lambda feature : {
        "fillColor" : colormap(gas_data[feature['Gazole_prix']]),
        #fillOpacity : 0.7,
        #lineOpacity : 0.2
    },
    legend_name='Prix essence'
).add_to(map)

colormap.add_to(map)
map.save(outfile='map.html')