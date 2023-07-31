\# DaGuinci \- Python support

## Installation

* Créer environnement virtuel :

``` bash
python -m venv env
```

* Activer environnement virtuel :

``` bash
source env/bin/activate
```

* Installer dépendances

``` bash
pip install -r requirements.txt
```

## Exécution

* Exécuter un script :

``` bash
python xxx.py
```

* Lancer le serveur

``` bash
/projectLab python manage.py runserver
```

* Si besoin de modifier les styles, installer [sass](https://sass-lang.com/install/)

``` bash
sass static/styles/styles.scss static/styles/styles.css --watch
```

## Content

Tasks related to new content.

* [x] Supprimer l'animation de la page posts
* [x] Repasser l'historique du projet
* [x] Repasser les critères d'évaluation
* [x] Empecher la reponse aux billets deja traites, en backend
* [x] titre/texte alternatifs aux images, aux liens
* [x] design accessible
* [ ] générer rapport flake8
* [x] Supprimer bouton repondre en cours de reponse
* [x] Mettre en place les msg d'erreurs sur home
* [x] Reserver la modif et suppression des post a la page posts