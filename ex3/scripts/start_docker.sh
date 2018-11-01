#!/usr/bin/env bash
pipenv run ex3_proj/manage.py migrate
pipenv run ex3_proj/manage.py runserver 0.0.0.0:8000
