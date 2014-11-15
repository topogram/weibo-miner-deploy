[program:{{ domain }}]
command=/usr/local/bin/uwsgi
  --socket uwsgi.sock
  --pythonpath /
  --touch-reload /app.wsgi
  --chmod-socket 666
  --uid www-data
  --gid www-data
  --processes 1
  --master
  --no-orphans
  --max-requests 5000
  --module {{ module }}
  --callable app
directory={{ root }}
stdout_logfile={{ root }}/uwsgi.log
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stopsignal=QUIT
