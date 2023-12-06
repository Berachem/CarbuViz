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
            clearable = False,
        )
    ],
        style={
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center'
    }

    ),

    # Titre de l'application
    html.H1("Carte des prix des carburants en temps réel 🌍 🔴"),
    
    # Carte
    html.Div([
        html.Iframe(id='map', srcDoc=open('generated/map.html', 'r').read(), width='100%', height='600')
    ]),
    
    # Séparateur
      html.Hr(
        id='separator',
        style={
            'border-top': '2px solid '+COULEURS_CARBURANTS[carburant_options[0]['value']][0],
        }
    ),
    
    
    # Titre de la partie graphique
    html.H1("Statistiques par type de carburant en "+str(ANNEE_CHOISIE)+" ⛽️"),

    dcc.Graph(id='regroupement-prix-graph'), # Histogramme des prix pour le nombre de stations-service

    dcc.Graph(id='prix-moyen-graph'), # Graphique de tarif moyen par mois

    dcc.Graph(id='prix-semaine-graph'), # Graphique de tarif moyen par semaine

    dcc.Graph(id='penurie_graph'), # Graphique des pénuries par semaine


    # Prix moyen et median enregustrés pour le carburant sélectionné
    html.Div([
        html.Div(id='prix-median-moyen-container', children=[
            html.Span(children="Chiffres annuels : "),
            html.Span(id='prix-median-text'),
            html.Span(id='prix-moyen-text')
        ])
    ]),
    
    # Crédits
    html.H5(id="credits_developpeurs",
            children="Réalisé par Berachem MARKRIA & Joshua LEMOINE",
            ),
])


def generate_style_for_median_moyen(median_color, moyen_color):
    """
    Fonction pour générer le style des mots "médian" et "moyen"

    Args:
        median_color (str): Couleur du mot "médian"
        moyen_color (str): Couleur du mot "moyen"
        
    Returns:
        style_median (dict): Style du mot "médian"
        style_moyen (dict): Style du mot "moyen"
    """
    style_median = {'color': median_color, 'font-weight': 'bold'}
    style_moyen = {'color': moyen_color, 'font-weight': 'bold'}
    return style_median, style_moyen

def generate_text_for_median_moyen(prix_median, prix_moyen, style_median, style_moyen):
    """
    Fonction pour générer le texte des prix médian et moyen
    
    Args:
        prix_median (float): Prix médian
        prix_moyen (float): Prix moyen
        style_median (dict): Style du mot "médian"
        style_moyen (dict): Style du mot "moyen"
        
    Returns:
        median_text (list): Texte du prix médian
        moyen_text (list): Texte du prix moyen
    """
    median_text = [html.Span('Médiane : ', style=style_median), f'{prix_median} €']
    moyen_text = [html.Span('Moyenne : ', style=style_moyen), f'{prix_moyen} €']
    return median_text, moyen_text

def generate_nombre_stations_graph(selected_carburant, nombre_stations):
    """
    Fonction auxiliaire pour générer le graphique de nombre de stations-service
    
    Args:
        selected_carburant (str): Carburant sélectionné
        nombre_stations (DataFrame): Nombre de stations-service pour chaque mois
        
    Returns:
        fig (plotly.graph_objects.Figure): Graphique de nombre de stations-service
    """
    return px.bar(nombre_stations, x='mois', y='id',
                   title=f'Nombre de stations-service vendant du {selected_carburant} par mois en '+str(ANNEE_CHOISIE),
                   labels={'mois': 'Mois', 'id': 'Nombre de Stations-Service'},
                   color_discrete_sequence=[
                       COULEURS_CARBURANTS[selected_carburant][0]],
                   template='plotly_white',
                   )

def generate_prix_moyen_graph(selected_carburant, mois_moyen):
    """
    Fonction auxiliaire pour générer le graphique des tarifs moyens par mois
    
    Args :
        selected_carburant (str): Carburant sélectionné
        mois_moyen (DataFrame): Tarif moyen pour chaque mois
        
    Returns:
        fig (plotly.graph_objects.Figure): Graphique de tarif moyen par mois
    """
    return px.line(mois_moyen, x='mois', y='valeur_carburant',
                  title=f'Tarif moyen du {selected_carburant} par mois en '+str(ANNEE_CHOISIE),
                  labels={'mois': 'Mois', 'valeur_carburant': 'Tarif Moyen'},
                  color_discrete_sequence=[
                      COULEURS_CARBURANTS[selected_carburant][0]],
                  template='plotly_white'
                  )

def generate_prix_semaine_graph(selected_carburant,semaine_moyen):
    """
    Fonction auxiliaire pour générer le graphique des tarifs moyens par semaine
    
    Args :
        selected_carburant (str): Carburant sélectionné
        semaine_moyen (DataFrame): Tarif moyen pour chaque semaine
        
    Returns:
        fig (plotly.graph_objects.Figure): Graphique de tarif moyen par semaine
    """
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

def generate_evolution_penurie_annee(selected_carburant,station_penurie):
    """
    Fonction auxiliaire pour générer le graphique des penuries
    
    Args :
        selected_carburant (str): Carburant sélectionné
        station_penurie (DataFrame): Nombre de stations sans le carburant sélectionné
        
    Returns:
        fig (plotly.graph_objects.Figure): Graphique des penuries
    """
    return px.line(station_penurie, x='semaine', y='id',
                  title=f'Nombre de station sans {selected_carburant} sur '+str(ANNEE_CHOISIE),
                  labels={'date': 'date', 'id': 'Nombre de Stations-Service'},
                  color_discrete_sequence=["#FF0020"],
                  template='plotly_white'
                  )

def generate_repartition_prix_nombre_station(selected_carburant,prix_moyen_annee):
    """
    Fonction auxiliaire pour générer l'histogramme des stations regroupées par prix
    
    Args : 
        selected_carburant (str): Carburant sélectionné
        prix_moyen_annee (DataFrame) : Intervalles contenant les moyennes de prix sur l'année de chaque station
        
    Return :
        fig (plotly.graph_objects.Figure): Graphique des répartition des prix moyens annuels
    """
    fig = px.histogram(
        prix_moyen_annee,x='valeur_carburant',y='id',
        title=f'Repartition des prix pour le {selected_carburant} sur '+str(ANNEE_CHOISIE),
        labels={'valeur_carburant': 'prix', 'id': 'Nombre de stations'},
        color_discrete_sequence=[
            COULEURS_CARBURANTS[selected_carburant][0]],
        template='plotly_white',
        nbins = 24,
        histfunc = "count",
    )

    fig.update_xaxes(tickformat=".2f")
    fig.update_layout(bargap=0.1)

    return fig

# Callback pour mettre à jour les graphiques en fonction du type de carburant sélectionné
@app.callback(
    [
     Output('regroupement-prix-graph', 'figure'),
     Output('prix-moyen-graph', 'figure'),
     #Output('nombre-stations-graph', 'figure'),
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
    """
    Fonction pour mettre à jour les graphiques en fonction du type de carburant sélectionné. 
    Cette fonction va par ailleurs générer la carte des prix des carburants instantannées.
    
    Args:
    
        selected_carburant (str): Carburant sélectionné
        
    Returns:
        Tous les éléments de la mise en page à mettre à jour (voir la liste des retours "Outputs")
    """
    # Filtrer les données pour le carburant sélectionné
    mask = (df['nom_carburant'] == selected_carburant)
    filtered_df = df.loc[mask].copy()

    # Convertir la colonne 'date' en datetime avec le format spécifié
    filtered_df['date'] = pd.to_datetime(filtered_df['date'], format='mixed', dayfirst=True)

    # Extraire le mois et l'année de la date
    filtered_df['mois'] = filtered_df['date'].dt.strftime('%m/%Y')

    #Extraire la semaine de l'année via la date
    filtered_df['semaine'] = filtered_df['date'].dt.isocalendar().week

    #Regrouper les stations par prix
    station_par_prix = filtered_df.groupby("id")['valeur_carburant'].mean().reset_index()

    #Extraire le tarif moyen pour chaque semaine 
    semaine_moyen = filtered_df.groupby('semaine')['valeur_carburant'].mean().reset_index()

    #Calculer le tarif moyen pour chaque mois
    mois_moyen = filtered_df.groupby('mois')['valeur_carburant'].mean().reset_index()

    #Calculer le nombre de stations-service pour chaque mois
    nombre_stations = filtered_df.groupby('mois')['id'].nunique().reset_index()

    #Calculer le nombre de stations services ne proposant pas le carburant selectionné par jour
    oposite_mask = ~df['id'].isin(filtered_df['id'])
    oposite_filtered_df = df.loc[oposite_mask].copy()
    oposite_filtered_df['date'] = pd.to_datetime(oposite_filtered_df['date'], format='mixed', dayfirst=True)
    oposite_filtered_df['semaine'] = oposite_filtered_df['date'].dt.isocalendar().week
    station_penurie = oposite_filtered_df.groupby('semaine').nunique().reset_index()

    #Générer les graphiques de tarif moyen, de nombre de stations-service et du prix par semaine
    fig_regroupement_prix = generate_repartition_prix_nombre_station(selected_carburant,station_par_prix)
    fig_prix_moyen = generate_prix_moyen_graph(selected_carburant, mois_moyen)
    fig_nombre_stations = generate_nombre_stations_graph(selected_carburant, nombre_stations)
    fig_semaine_moyen = generate_prix_semaine_graph(selected_carburant,semaine_moyen)
    fig_penurie = generate_evolution_penurie_annee(selected_carburant,station_penurie)

    # Calculer le prix médian et moyen sur l'annee
    prix_median = filtered_df['valeur_carburant'].median().round(3)
    prix_moyen = filtered_df['valeur_carburant'].mean().round(3)

    # Style pour les mots "médian" en bleu et "moyen" en rouge
    style_median, style_moyen = generate_style_for_median_moyen('blue', 'red')

    # Générer le texte des prix médian et moyen
    median_text, moyen_text = generate_text_for_median_moyen(prix_median, prix_moyen, style_median, style_moyen)
    
    # Générer la carte des prix des carburants
    drawMap(selected_carburant)

    #eventuellement fig_nombre_stations
    return fig_regroupement_prix,fig_prix_moyen, fig_semaine_moyen, fig_penurie, {'background-color': COULEURS_CARBURANTS[selected_carburant][0]}, median_text, moyen_text, {'border-top': '2px solid '+COULEURS_CARBURANTS[selected_carburant][0]}, open('generated/map.html', 'r').read()


if __name__ == '__main__':
    app.run_server(debug=False)
