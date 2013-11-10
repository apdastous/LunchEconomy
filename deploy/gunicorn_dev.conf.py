bind = 'unix:run/gunicorn.socket'
pidfile = 'run/gunicorn.pid'
workers = 4
accesslog = "/var/log/dev/gunicorn.access.log"
errorlog = "/var/log/dev/gunicorn.error.log"