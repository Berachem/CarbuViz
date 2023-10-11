import folium
import pandas as pd

#données
gas_data = pd.read_csv("data/PrixCarburants_instantane.csv",sep=";")
gas_name = gas_data["nom_carburant"]
mask = (gas_name.str.startswith("Gazole"))
gas_data = gas_data[mask]


folium.Choropleth(
    geo_data="data/departements.geojson",                              # geographical data
    name='choropleth',
    data=gas_data,                                    # numerical data
    columns=['id','valeur_carburant'],                     # numerical data key/value pair
    key_on='feature.properties.id',       # geographical property used to establish correspondance with numerical data
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Prix essence'
).add_to(map)


#carte
coords = (47.0,2.0)
map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=5.0)

f = lambda x :{'fillColor':'#E88300', 'fillOpacity':0.5, 'color':'#E84000', 'weight':1, 'opacity':1}

folium.GeoJson(
    data="data/departements.geojson",
    name="idf",
    style_function= f
).add_to(map)

map.save(outfile='map.html')