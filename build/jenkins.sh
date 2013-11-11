#!/bin/bash

virtualenv --clear --no-site-packages env

source env/bin/activate

pip install -r requirements/jenkins.txt

python manage.py test --jenkins --settings=lunch_economy.settings.jenkins