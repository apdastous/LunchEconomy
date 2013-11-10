bind = 'unix:/opt/lunch-economy/dev/run/gunicorn.socket'
pidfile = '/opt/lunch-economy/dev/run/gunicorn.pid'
workers = 4
accesslog = "/var/log/dev/gunicorn.access.log"
errorlog = "/var/log/dev/gunicorn.error.log"