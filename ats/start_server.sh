#!/bin/bash -v

cd ats
python ats/manage.py migrate
django-admin loaddata groups.json
django-admin loaddata demo_users.json
python ats/manage.py runserver 0.0.0.0:8000
