bind = 'unix:run/gunicorn.socket'
pidfile = 'run/gunicorn.pid'
workers = 4
accesslog = "logs/dev/gunicorn.access.log"
errorlog = "logs/dev/gunicorn.error.log"