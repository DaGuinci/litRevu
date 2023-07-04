    # DaGuinci - Python support

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

``` bach
/projectLab python manage.py runserver
```

## Commandes utiles

* Desactiver environnement virtuel :

``` bash
deactivate
```

* Sauvegarder dépendances

``` bash
pip freeze > requirements.txt
```

* Mettre à jour la base de données

``` bash
python manage.py makemigrations
python manage.py migrate
```