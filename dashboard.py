from dash import Dash, dcc, html, Input, Output
import dash
import pandas as pd
import plotly.express as px
from constants import COULEURS_CARBURANTS, ANNEE_CHOISIE
from map import drawMap





# Charger les données CSV
df = pd.read_csv('data/PrixCarburants_annuel_'+str(ANNEE_CHOISIE)+'.csv', sep=';')

# Créer une application Dash
app = dash.Dash(__name__)

# Options de carburant pour le dropdown
carburant_options = [{'label': carburant, 'value': carburant}
                     for carburant in df['nom_carburant'].unique()]

app.title = "CarbuViz - Projet Python"
app._favicon = "CarbuViz.ico"


# Mise en page de l'application
app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='assets/css/style.css'
    ),
        # image centrée LOGO
    html.Img(id="logo_carbu_viz", src="assets/img/carbuVizLogo.png"),


    # Div contenant le dropdown et le rectangle de couleur
    html.Div([

        # Rectangle de couleur du carburant
        html.Div(
            id='carburant-color-rectangle',
            style={
                'background-color': COULEURS_CARBURANTS[carburant_options[0]['value']][0], }
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

    
  
    
    html.H1("Carte des prix des carburants en temps réel 🌍 🔴"),
    
    # Carte
    html.Div([
        html.Iframe(id='map', srcDoc=open('generated/map.html', 'r').read(), width='100%', height='600')
    ]),
    
    
    
      html.Hr(
        id='separator',
        style={
            'border-top': '2px solid '+COULEURS_CARBURANTS[carburant_options[0]['value']][0],
        }
    ),
    
    
    

    html.H1("Statistiques par type de carburant en "+str(ANNEE_CHOISIE)+" ⛽️"),



    dcc.Graph(id='nombre-stations-graph'),
    
    
    dcc.Graph(id='prix-moyen-graph'),

    dcc.Graph(id='prix-semaine-graph'),

    dcc.Graph(id='penurie_graph'),


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
                   title=f'Nombre de stations-service vendant du {selected_carburant} par mois en '+str(ANNEE_CHOISIE),
                   labels={'mois': 'Mois', 'id': 'Nombre de Stations-Service'},
                   color_discrete_sequence=[
                       COULEURS_CARBURANTS[selected_carburant][0]],
                   template='plotly_white',
                   )

# Fonction auxiliaire pour générer le graphique de tarif moyen
def generate_prix_moyen_graph(selected_carburant, mois_moyen):
    return px.line(mois_moyen, x='mois', y='valeur_carburant',
                  title=f'Tarif moyen du {selected_carburant} par mois en '+str(ANNEE_CHOISIE),
                  labels={'mois': 'Mois', 'valeur_carburant': 'Tarif Moyen'},
                  color_discrete_sequence=[
                      COULEURS_CARBURANTS[selected_carburant][0]],
                  template='plotly_white'
                  )

# Fonction auxiliaire pour générer le graphique des prix par semaine
def generate_prix_semaine_graph(selected_carburant,semaine_moyen):
    fig = px.histogram(
        semaine_moyen,x='semaine',y='valeur_carburant',
        title=f'Tarif moyen du {selected_carburant} par semaine en '+str(ANNEE_CHOISIE),
        labels={'semaine': 'Semaine', 'valeur_carburant': 'Tarif Moyen'},
        color_discrete_sequence=[
            COULEURS_CARBURANTS[selected_carburant][0]],
        template='plotly_white',
        nbins = 26,
        histfunc='avg'
    )

    #suppression hover
    fig.update_traces(hovertext="none")

    #séparation des bandes
    fig.update_layout(bargap=0.2)

    return fig

# Fonction auxiliaire pour générer le graphique des penuries
def generate_evolution_penurie_annee(selected_carburant,station_penurie):
    return px.line(station_penurie, x='semaine', y='id',
                  title=f'Nombre de station sans {selected_carburant} sur '+str(ANNEE_CHOISIE),
                  labels={'date': 'date', 'id': 'Nombre de Stations-Service'},
                  color_discrete_sequence=["#FF0020"],
                  template='plotly_white'
                  )

# Callback pour mettre à jour les graphiques en fonction du type de carburant sélectionné
@app.callback(
    [Output('prix-moyen-graph', 'figure'),
     Output('nombre-stations-graph', 'figure'),
     Output('prix-semaine-graph','figure'),
     Output('penurie_graph', 'figure'),
     Output('carburant-color-rectangle', 'style'),
     Output('prix-median-text', 'children'),
     Output('prix-moyen-text', 'children'),
     Output('separator', 'style'),
     Output('map', 'srcDoc')
    ],
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

    #Extraire la semaine de l'année via la date
    filtered_df['semaine'] = filtered_df['date'].dt.isocalendar().week

    #Extraire le tarif moyen pour chaque semaine 
    semaine_moyen = filtered_df.groupby('semaine')['valeur_carburant'].mean().reset_index()

    #Calculer le tarif moyen pour chaque mois
    mois_moyen = filtered_df.groupby(
        'mois')['valeur_carburant'].mean().reset_index()

    #Calculer le nombre de stations-service pour chaque mois
    nombre_stations = filtered_df.groupby(
        'mois')['id'].nunique().reset_index()

    #Calculer le nombre de stations services ne proposant pas le carburant selectionné par jour
    oposite_mask = ~df['id'].isin(filtered_df['id'])
    oposite_filtered_df = df[oposite_mask]
    oposite_filtered_df['date'] = pd.to_datetime(oposite_filtered_df['date'], format='mixed', dayfirst=True)
    oposite_filtered_df['semaine'] = oposite_filtered_df['date'].dt.isocalendar().week
    station_penurie = oposite_filtered_df.groupby('semaine').nunique().reset_index()

    # Générer les graphiques de tarif moyen, de nombre de stations-service et du prix par semaine
    fig_prix_moyen = generate_prix_moyen_graph(selected_carburant, mois_moyen)
    fig_nombre_stations = generate_nombre_stations_graph(selected_carburant, nombre_stations)
    fig_semaine_moyen = generate_prix_semaine_graph(selected_carburant,semaine_moyen)
    fig_penurie = generate_evolution_penurie_annee(selected_carburant,station_penurie)

    # Calculer le prix médian et moyen
    prix_median = filtered_df['valeur_carburant'].median().round(3)
    prix_moyen = filtered_df['valeur_carburant'].mean().round(3)

    # Style pour les mots "médian" en bleu et "moyen" en rouge
    style_median, style_moyen = generate_style_for_median_moyen('blue', 'red')

    # Générer le texte des prix médian et moyen
    median_text, moyen_text = generate_text_for_median_moyen(prix_median, prix_moyen, style_median, style_moyen)
    
    # Générer la carte des prix des carburants
    drawMap(selected_carburant)

    return fig_prix_moyen, fig_semaine_moyen, fig_nombre_stations, fig_penurie, {'background-color': COULEURS_CARBURANTS[selected_carburant][0]}, median_text, moyen_text, {'border-top': '2px solid '+COULEURS_CARBURANTS[selected_carburant][0]}, open('generated/map.html', 'r').read()


if __name__ == '__main__':
    app.run_server(debug=True)
