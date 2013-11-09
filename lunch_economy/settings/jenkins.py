from base import *

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
)

COVERAGE_EXCLUDES_FOLDERS = ['/usr/local/*']