workers = 2
worker_class = 'socketio.sgunicorn.GeventSocketIOWorker'
bind = '0.0.0.0:5000'
pidfile= '{{ pid }}'
debug = True
loglevel = 'debug'
errorlog = '{{ log }}/gunicorn.log'
daemon = True
