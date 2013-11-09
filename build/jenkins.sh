#!/bin/bash

virtualenv --clear --no-site-packages env

source env/bin/activate

pip install -r requirements/jenkins.txt

python manage.py jenkins --coverage-exclude=COVERAGE_EXCLUDES_FOLDERS  --settings=settings.jenkins