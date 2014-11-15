[uwsgi]
uid = www-data
gid = root
chmod-socket = 664
master = true
processes = 2
virtualenv = {{ venv }}
pythonpath = {{ app }}
pidfile = {{ pid }}
socket = {{ socket }}
module = {{ module }}
callable = {{ module }}
logdate = true
