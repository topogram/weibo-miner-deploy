[program:{{ name }}]
; Point the command to the specific rqworker command you want to run.
; If you use virtualenv, be sure to point it to

; Also, you probably want to include a settings module to configure this
; worker.  For more info on that, see http://python-rq.org/docs/workers/
command={{ virtualenv }}/bin/rqworker  taf
process_name=%(program_name)s

; If you want to run more than one worker instance, increase this
numprocs=1

; This is the directory from which RQ is ran. Be sure to point this to the
; directory where your source code is importable from
directory={{ app_dir }}

stdout_logfile={{ log }}/{{ name  }}.access.log
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=2

stderr_logfile={{ log }}/{{ name }}.error.log
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=2

; RQ requires the TERM signal to perform a warm shutdown. If RQ does not die
; within 10 seconds, supervisor will forcefully kill it
stopsignal=TERM

; These are up to you
autostart=true
autorestart=true
