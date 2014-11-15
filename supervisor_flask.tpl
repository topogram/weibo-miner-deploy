[program:{{ domain }}]
command=uwsgi {{ uswgi }}
stdout_logfile={{ log }}/uwsgi.log
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stopsignal=QUIT
exitcodes=0
