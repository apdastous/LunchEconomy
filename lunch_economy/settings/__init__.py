from getpass import getuser

user = getuser()
print user
if user == 'jenkins':
    from jenkins import *
elif user == 'www-data':
    from base import *
else:
    from dev import *