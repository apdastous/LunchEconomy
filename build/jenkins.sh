virtualenv --clear --no-site-packages env

source activate env

pip install -r requirements/jenkins.txt

python manage.py jenkins --coverage-exclude=COVERAGE_EXCLUDES_FOLDERS