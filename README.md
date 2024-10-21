# Détection Automatique des Modifications dans les PDF

## Description

Ce projet permet d'identifier automatiquement les modifications apportées à des fichiers PDF et de générer un rapport de comparaison détaillé. Il est conçu pour être utilisé dans un environnement Docker afin d'assurer une gestion isolée et reproductible des fichiers PDF ainsi que des métadonnées associées, stockées dans une base de données PostgreSQL.

## Fonctionnalités

- **Détection de modifications PDF** : Analyse des fichiers PDF pour identifier les changements (contenu, structure, etc.).
- **Comparaison visuelle** : Génération de rapports comparatifs incluant des images illustrant les différences.
- **Stockage des métadonnées** : Utilisation de PostgreSQL pour gérer les informations relatives aux PDF.
- **Automatisation via Docker** : Configuration d'un environnement Docker pour faciliter le déploiement et l'exécution du projet.
- **Rapport de comparaison** : Les rapports sont générés et sauvegardés avec un sous-dossier daté dans un répertoire défini.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- **Docker** et **Docker Compose**
- **Git** (pour le versionnement du code)

## Installation

1. Clonez ce dépôt Git sur votre machine locale
2. copier tous les fichiers et coller les dans le dossier ou vous voulez lancer le programme
3. Attention : Le programme va comparer tous les fichiers PDF présents dans le répertoire spécifié ainsi que dans ses sous-répertoires, mais il n'analysera pas les PDF situés dans d'autres répertoires.



## Utilisation
Pour lancer le programme, utilisez la commande suivante :
make

Les rapports générés seront stockés dans le dossier rapport_comparaison, avec un sous-dossier daté automatiquement.

Pour supprimer toutes les images Docker ainsi que les volumes (attention, cela supprime également la base de données), utilisez la commande suivante :
make adios

Pour accéder aux logs des conteneurs Docker, utilisez la commande suivante :
make log

