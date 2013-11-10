bind = 'unix:/opt/lunch-economy/prod/run/gunicorn.socket'
pidfile = '/opt/lunch-economy/prod/run/gunicorn.pid'
workers = 4
accesslog = "/var/log/lunch-economy/prod/gunicorn.access.log"
errorlog = "/var/log/lunch-economy/prod/gunicorn.error.log"