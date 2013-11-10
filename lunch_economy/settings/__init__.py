from getpass import getuser

user = getuser()

if user == 'jenkins':
    from jenkins import *
elif user == 'www-lunch':
    from base import *
else:
    from local import *