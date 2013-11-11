from base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_NAME': 'test_database.db'
    }
}

INSTALLED_APPS += ('discover_jenkins',)

TEST_RUNNER = 'discover_jenkins.runner.DiscoverCIRunner'

TEST_PROJECT_APPS = (
    'lunch_economy.apps.core',
    'lunch_economy.apps.groups',
    'lunch_economy.apps.lunch',
    'lunch_economy.apps.mail',
    'lunch_economy.apps.users',
)

TEST_TASKS = (
    'discover_jenkins.tasks.with_coverage.CoverageTask',
    'discover_jenkins.tasks.run_pylint.PyLintTask',
)

TEST_COVERAGE_EXCLUDES_FOLDERS = [
    '/usr/local/*',
]

TEST_COVERAGE_EXCLUDES = [
    'lunch_economy.apps.core.tests',
    'lunch_economy.apps.groups.tests',
    'lunch_economy.apps.lunch.tests',
    'lunch_economy.apps.mail.tests',
    'lunch_economy.apps.users.tests',
]