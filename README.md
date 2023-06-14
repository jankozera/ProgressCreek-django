# Django Starter App Backend Server

Backend server written in Django + DRF framework. This project uses python 3.9.4 and Django 4.1.2

## Table of content

- [Before you start](#Before you start)
- [Running server](#Running server)
- [Running server with docker](#Running server with docker)
- [Useful commands](#Useful commands)
- [Documenting API](#Documenting API)
- [Useful links](#Useful links)

## Before you start

- create python's virtual environment that will be used for development  
  `python3 -m venv ./venv`
- activate the environment (**do that each time you open new terminal!!!**)  
  **for linux/macos** `source ./venv/bin/activate`  
  **for windows** `.\venv\Scripts\activate`
- install dependencies  
  `pip install -r ./requirements.txt`
- install pre-commit  
  `pre-commit install`
- migrate the database (if necessary)  
  `python manage.py migrate`

## Running server

In order to start the server:  
`python manage.py runserver`

## Running server with docker

In order to start the server with docker for the first time:  
`docker compose up --build`

In order to start the server with docker without rebuilding:  
`docker compose up`

## Useful commands

- Creating new admin user `python manage.py createsuperuser`
- Create new migrations `python manage.py makemigrations`
- Migrate the database `python manage.py migrate`

## Documenting API

- Swagger documentation is autogenerated and available at [/swagger/](http://127.0.0.1:8000/swagger/)
- Redoc documentation is autogenerated and available at [/redoc/](http://127.0.0.1:8000/redoc/)

## Useful links

- [DRF](https://www.django-rest-framework.org)
- [filtering in DRF](https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html#quickstart)
- [swagger and redoc](https://drf-yasg.readthedocs.io/en/stable/readme.html)
- [pre-commit](https://pre-commit.com)
- [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
