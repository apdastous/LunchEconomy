from base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/opt/lunch_economy/dev/db/lunch_economy.db',
    }
}