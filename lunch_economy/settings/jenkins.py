from base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_NAME': 'test_database.db'
    }
}

INSTALLED_APPS += ('django_jenkins',)

PROJECT_APPS = (
    'lunch_economy.apps.core',
    'lunch_economy.apps.users',
    'lunch_economy.apps.groups',
    'lunch_economy.apps.mail',
    'lunch_economy.apps.lunch',
)

JENKINS_TASKS = (
    'django_jenkins.tasks.dir_tests',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pylint',
)

COVERAGE_EXCLUDES_FOLDERS = ['/usr/local/*']