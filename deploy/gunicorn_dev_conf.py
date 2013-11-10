bind = 'unix:/opt/lunch-economy/dev/run/gunicorn.socket'
pidfile = '/opt/lunch-economy/dev/run/gunicorn.pid'
workers = 4
accesslog = "/var/log/lunch-economy/dev/gunicorn.access.log"
errorlog = "/var/log/lunch-economy/dev/gunicorn.error.log"