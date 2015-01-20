[program:{{ domain }}]

directory={{ app_dir}}
environment={{ VENVPATH}}/bin

command={{VENVPATH}}/bin/gunicorn wsgi:app -c {{gunicorn_conf}}

stdout_logfile={{ log }}/gunicorn.access.log
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=2

stderr_logfile={{ log }}/gunicorn.error.log
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=2

user=www-data
autostart=true
autorestart=true

redirect_stderr=true
stopsignal=QUIT
exitcodes=0
