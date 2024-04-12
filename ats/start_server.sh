#!/bin/bash -v

cd ats
python manage.py migrate
django-admin loaddata groups.json
django-admin loaddata demo_users.json
python manage.py runserver 0.0.0.0:8000
