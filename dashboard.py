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
    html.Img(id="gas_station_img", src="static/assets/img/gas_station.png"),

    html.H1("Tarif moyen par type de carburant en 2022 ⛽️"),

    # Div contenant le dropdown et le rectangle de couleur
    html.Div([

        # Rectangle de couleur du carburant
        html.Div(
            id='carburant-color-rectangle',
            style={'background-color': couleursCarburant[carburant_options[0]['value']][0],}
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

    # Graphique de dispersion
    dcc.Graph(id='prix-moyen-graph'),


    html.H5(id="credits_developpeurs",
            children="Réalisé par Berachem MARKRIA & Joshua LEMOINE",
            ),

    # Lien vers le code source
    #html.A(href="https://github.com/Berachem/CarbuCheck",
       #    target="_blank", id="github_link", children="Code source"),


])

# Callback pour mettre à jour le graphique en fonction du type de carburant sélectionné


@app.callback(
    [Output('prix-moyen-graph', 'figure'),
     Output('carburant-color-rectangle', 'style')],
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

    # Créer le graphique de dispersion
    fig = px.line(mois_moyen, x='mois', y='valeur_carburant',
                  title=f'Tarif moyen du {selected_carburant} par mois en 2022',
                  labels={'mois': 'Mois', 'valeur_carburant': 'Tarif Moyen'},
                  color_discrete_sequence=[
                      couleursCarburant[selected_carburant][0]],
                  template='plotly_white'
                  )

    return fig, {'background-color': couleursCarburant[selected_carburant][0]}


if __name__ == '__main__':
    app.run_server(debug=True)
