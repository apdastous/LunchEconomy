from getpass import getuser

user = getuser()

if user == 'jenkins':
    from jenkins import *
else:
    from local import *