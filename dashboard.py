from dash import Dash, dcc, html, Input, Output
import dash
import pandas as pd
import plotly.express as px

# Créer un dictionnaire de couleurs pour chaque carburant
couleursCarburant = {
    "Gazole": ["#FFC300", "#000000"],
    "SP95": ["#013210", "#FFFFFF"],
    "E85": ["#35CCEB", "#000000"],
    "SP98": ["#013210", "#FFFFFF"],
    "GPLc": ["#033371", "#FFFFFF"],
    "E10": ["#2CD32C", "#000000"],
}

# Charger les données CSV
df = pd.read_csv('data/PrixCarburants_annuel_2022.csv', sep=';')

# Créer une application Dash
app = dash.Dash(__name__)

# Options de carburant pour le dropdown
carburant_options = [{'label': carburant, 'value': carburant}
                     for carburant in df['nom_carburant'].unique()]

# Mise en page de l'application
app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='/static/assets/css/style.css'
    ),

    # image centrée static/assets/gas_station.png
    html.Img(id="logo_carbu_viz", src="static/assets/img/carbuVizLogo.png"),

    html.H1("Statistiques par type de carburant en 2022 ⛽️"),

    # Div contenant le dropdown et le rectangle de couleur
    html.Div([

        # Rectangle de couleur du carburant
        html.Div(
            id='carburant-color-rectangle',
            style={
                'background-color': couleursCarburant[carburant_options[0]['value']][0], }
        ),


        # Dropdown pour sélectionner le type de carburant
        dcc.Dropdown(
            id='carburant-dropdown',
            options=carburant_options,
            value=carburant_options[0]['value'],
        )
    ],
        style={
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center'
    }

    ),



    dcc.Graph(id='nombre-stations-graph'),
    
    
    dcc.Graph(id='prix-moyen-graph'),


    # Prix minimum et maximum enregustrés pour le carburant sélectionné
    html.Div([
        html.Div(id='prix-median-moyen-container', children=[
            html.H5(id='prix-median-moyen-text', children=[
                html.Span(id='prix-median-text'),
                html.Span(id='prix-moyen-text')
            ])
        ])
    ]),


    html.H5(id="credits_developpeurs",
            children="Réalisé par Berachem MARKRIA & Joshua LEMOINE",
            ),

    # Lien vers le code source
    # html.A(href="https://github.com/Berachem/CarbuCheck",
    #    target="_blank", id="github_link", children="Code source"),


])


# Fonction pour générer le style des mots "médian" et "moyen"
def generate_style_for_median_moyen(median_color, moyen_color):
    style_median = {'color': median_color, 'font-weight': 'bold'}
    style_moyen = {'color': moyen_color, 'font-weight': 'bold'}
    return style_median, style_moyen

# Fonction pour générer le texte des prix médian et moyen
def generate_text_for_median_moyen(prix_median, prix_moyen, style_median, style_moyen):
    median_text = [html.Span('Médiane : ', style=style_median), f'{prix_median} €']
    moyen_text = [html.Span('Moyenne : ', style=style_moyen), f'{prix_moyen} €']
    return median_text, moyen_text

# Fonction auxiliaire pour générer le graphique de nombre de stations-service
def generate_nombre_stations_graph(selected_carburant, nombre_stations):
    return px.bar(nombre_stations, x='mois', y='id',
                   title=f'Nombre de stations-service vendant du {selected_carburant} par mois en 2022',
                   labels={'mois': 'Mois', 'id': 'Nombre de Stations-Service'},
                   color_discrete_sequence=[
                       couleursCarburant[selected_carburant][0]],
                   template='plotly_white',
                   )

# Fonction auxiliaire pour générer le graphique de tarif moyen
def generate_prix_moyen_graph(selected_carburant, mois_moyen):
    return px.line(mois_moyen, x='mois', y='valeur_carburant',
                  title=f'Tarif moyen du {selected_carburant} par mois en 2022',
                  labels={'mois': 'Mois', 'valeur_carburant': 'Tarif Moyen'},
                  color_discrete_sequence=[
                      couleursCarburant[selected_carburant][0]],
                  template='plotly_white'
                  )

# Callback pour mettre à jour les graphiques en fonction du type de carburant sélectionné
@app.callback(
    [Output('prix-moyen-graph', 'figure'),
     Output('nombre-stations-graph', 'figure'),
     Output('carburant-color-rectangle', 'style'),
     Output('prix-median-text', 'children'),
     Output('prix-moyen-text', 'children')],
    [Input('carburant-dropdown', 'value')]
)
def update_graph(selected_carburant):
    # Filtrer les données pour le carburant sélectionné
    mask = (df['nom_carburant'] == selected_carburant)
    filtered_df = df[mask]

    # Convertir la colonne 'date' en datetime avec le format spécifié
    filtered_df['date'] = pd.to_datetime(
        filtered_df['date'], format='mixed', dayfirst=True)

    # Extraire le mois et l'année de la date
    filtered_df['mois'] = filtered_df['date'].dt.strftime('%m/%Y')

    # Calculer le tarif moyen pour chaque mois
    mois_moyen = filtered_df.groupby(
        'mois')['valeur_carburant'].mean().reset_index()

    # Calculer le nombre de stations-service pour chaque mois
    nombre_stations = filtered_df.groupby(
        'mois')['id'].nunique().reset_index()

    # Générer les graphiques de tarif moyen et de nombre de stations-service
    fig_prix_moyen = generate_prix_moyen_graph(selected_carburant, mois_moyen)
    fig_nombre_stations = generate_nombre_stations_graph(
        selected_carburant, nombre_stations)

    # Calculer le prix médian et moyen
    prix_median = filtered_df['valeur_carburant'].median().round(3)
    prix_moyen = filtered_df['valeur_carburant'].mean().round(3)

    # Style pour les mots "médian" en bleu et "moyen" en rouge
    style_median, style_moyen = generate_style_for_median_moyen('blue', 'red')

    # Générer le texte des prix médian et moyen
    median_text, moyen_text = generate_text_for_median_moyen(prix_median, prix_moyen, style_median, style_moyen)

    return fig_prix_moyen, fig_nombre_stations, {'background-color': couleursCarburant[selected_carburant][0]}, median_text, moyen_text


if __name__ == '__main__':
    app.run_server(debug=True)
