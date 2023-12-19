# Projet d'Anonymisation et Réidentification de Données

Ce projet a pour objectif d'explorer les techniques de défense utilisées pour anonymiser des données sensibles, ainsi que les techniques d'attaque pouvant contourner ces méthodes d'anonymisation. Cette initiative revêt une importance cruciale dans le domaine de la sécurité des données, s'intégrant parfaitement dans notre formation de cybersécurité.

## Contenu du Projet

Le jeu de données fourni pour ce projet est un fichier CSV contenant tous les pings de 69 individus ayant participé à une étude. Chaque ping représente la position d'un individu à un moment précis, exprimée en termes de latitude et de longitude. Certains individus émettent des pings chaque seconde, tandis que d'autres le font de manière moins fréquente. L'expérimentation a eu lieu sur une période de 11 semaines, allant de mars à juin 2018.

## Objectifs

- Analyser les techniques d'anonymisation des données dans le contexte des pings de localisation.
- Explorer les méthodes d'attaque potentielles visant à réidentifier les individus malgré l'anonymisation.
- Comprendre les enjeux de sécurité des données liés à la fréquence des pings et à la durée de l'expérimentation.


## Algorithmes Utilisés

- **Pour l'attaque :**
  
  Dans le dossier **partieAttaque**, le fichier `attackAlgorithms.py` contient les différents algorithmes utilisés :
    - **Jointure**
    - **Similitudes de trajectoire**
  Dans le dossier **partieDefense**, le fichier notebook `defend.ipynb` contient les différentes fonctions utilisées pour anonymiser.


## Utilisation du Projet

Pour utiliser ce projet, assurez-vous d'avoir le fichier CSV des pings, puis suivez les instructions fournies dans le code source pour lancer l'analyse des données. Vous trouverez également des informations détaillées sur les techniques d'anonymisation et les stratégies de défense mises en œuvre.

**Note:** Respectez toujours les règles éthiques et légales lors de l'utilisation et de la manipulation de données sensibles.
