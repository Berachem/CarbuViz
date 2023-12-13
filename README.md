# CarbuViz ⛽️


https://github.com/Berachem/CarbuViz/assets/61350744/b4dfe3f8-4b00-4cce-9ac1-96bf40995216


Made by Berachem MARKRIA & Joshua LEMOINE 🤩

## Stack
[![My Skills](https://skillicons.dev/icons?i=python,html,css,js)](https://skillicons.dev)

## Description du Projet 🚀

Le mini-projet CarbuCheck a pour objectif d'éclairer un sujet d'intérêt public, en l'occurrence, les données sur les carburants en France (annuelles et instantanées). L'utilisation de données publiques Open Data, accessibles et non modifiées, est au cœur de notre approche.

## Données Utilisées 📊

Les données utilisées sont issues de la plateforme Open Data du gouvernement français. Elles sont disponibles à l'adresse suivante : 

- https://www.data.gouv.fr/fr/datasets/prix-des-carburants-en-france/
- https://donnees.roulez-eco.fr/opendata/annee/2022

### Qu'est-ce que l'Open Data ? 📊

L'open data (ou donnée ouverte) est une donnée numérique d'origine publique ou privée. Elle peut être produite par une collectivité, un service public ou une entreprise. Elle est diffusée de manière structurée selon une méthode et une licence ouverte garantissant son libre accès et sa réutilisation par tous, sans restriction technique, juridique, ou financière.

(Wikipedia)

## Objectif du Projet 🎯

Le choix du sujet est libre, mais le résultat doit être un code Python structuré en plusieurs fichiers, permettant d'exécuter un dashboard dans un navigateur standard. Le dashboard doit contenir a minima un histogramme et une représentation géolocalisée, avec au moins l'un des graphiques étant dynamique.

__Consigne :__

> "Vous devez produire du code Python qui recueille et nettoie les données sur les carburants en France, les organise et les représente graphiquement de manière interactive. Le projet doit illustrer votre point de vue sur le sujet."

## Commandes à Exécuter pour Lancer le Projet 🚀 : le "User Guide"

1. Installez les dépendances avec la commande : 
`pip install -r requirements.txt`
2. Récupérez les données de l'année 2022 et celles en direct avec : 
`python get_data.py`
3. Lancez le dashboard avec : 
`python main.py`

Ces commandes garantissent une installation facile et rapide du projet CarbuCheck. Explorez et visualisez les données sur les carburants en France de manière interactive dans votre navigateur préféré. Bonne exploration ! 🌐

## 🧑‍💻 Developer Guide

#### Architecture du Projet

```
.
├── assets
│   ├── css
│   │   └── style.css
│   ├── img
│   │   ├── carbuVizLogo.png
│   │   └── gas_station.png
│   └── CarbuViz.ico
├── data
│   └── ... (données brutes)
├── generated
│   └── ... (cartes générées)
├── constants.py
├── get_data.py
├── dashboard.py
├── map.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

Si vous souhaitez enrichir le projet, voici quelques endroits où vous pouvez commencer :

- `constants.py` : contient les constantes utilisées dans le projet (les types de carburants associés à leur couleur et l'année des données à récupérer)

- `get_data.py` : contient les fonctions permettant de récupérer les données sur les carburants en France (annuelles et instantanées) et de les nettoyer

- `map.py` : contient les fonctions permettant de générer les cartes (au format .html)

- `dashboard.py` : contient les fonctions permettant de générer les graphiques 


## 🧐 Rapport d'Analyse

### 1. Carte

- La carte représente le prix moyen du carburant par département. Elle est générée à partir des données instantanées. 
> On observe que Paris et la Corse possèdent les prix moyens du carburant les plus élevés. 

### 2. Graphiques

- L'histogramme représente le nombre de stations-services qui proposent un prix moyen du carburant par intervalle de prix. Il est généré à partir des données annuelles.
>On peut observer que la majorité des stations-services proposent un prix moyen du carburant entre 1,5€ et 2€. Et qu'il existe tout de même des stations-services qui proposent un prix moyen du carburant supérieur à 2,5€ parfois et __très__ rarement inférieur à 1€.

- Le graphique représente le prix moyen du carburant par mois. Il est généré à partir des données annuelles.
> On peut observer que le prix moyen du carburant a subit des piques en Mars et Juin 2022. Ces piques se font même ressentir au niveau des médias : [exemple d'article](https://www.turbo.fr/actualite-automobile/carburants-les-prix-senvolent-le-diesel-depasse-largement-les-2-euros-184722).

- Le graphique représente le prix moyen du carburant par semaine. Il est généré à partir des données annuelles.
> On retrouve les mêmes piques que sur le graphique précédent mais avec une plus grande précision et donc une fluctuation plus faible.

- Le graphique représente le nombre de stations-services sans le carburant sélectionné par semaine. Il est généré à partir des données annuelles.
> On peut observer qu'il y a une correlation entre le prix moyen du carburant et le nombre de stations-services qui ne le proposent pas. En effet, lorsque le nombre de stations-services qui ne proposent pas le carburant sélectionné augmente, le prix moyen du carburant augmente également.






