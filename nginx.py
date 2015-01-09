#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import StringIO
 
from fabric.api import *
from fabric.operations import get, put
from fabric.contrib.files import upload_template,exists
from jinja2 import Template
from config.settings import *

APP_ROOT = CODE_DIR
NGINX_VHOST_DIR = '/etc/nginx/sites-'

SUPERVISOR_DIR = '/etc/supervisor/conf.d/'
USGWI_CONFIG_FILE=os.path.join(CONFIG_DIR,"uwsgi.ini")
GUNICORN_CONFIG_FILE=os.path.join(CONFIG_DIR,"gunicorn-conf.py")
WEBPORT=5000

def _render_template(string, context):
    return Template(string).render(context)

def make_supervisor_conf():
    
    # print USGWI_CONFIG_FILE
    
    supervisor_context={
        'domain': VHOST_NAME,
        'log' : LOG_DIR,
        'app_dir' : CODE_DIR,
        # "uswgi" : USGWI_CONFIG_FILE,
        "gunicorn_conf" : GUNICORN_CONFIG_FILE,
        "VENVPATH"      : VIRTUALENV_PATH
    }
    
    if not exists(SUPERVISOR_DIR):
        sudo('mkdir -p %s' % SUPERVISOR_DIR)

    upload_template("supervisor_gunicorn.tpl", "%s%s.conf"%(SUPERVISOR_DIR,VHOST_NAME), context=supervisor_context, use_jinja=True, use_sudo=True,backup=False)

def make_nginx_vhost():
    nginx_context={
        'domain': VHOST_NAME,
        'root': CODE_DIR,
        'log' : LOG_DIR,
        'static': STATIC,
        'socket':USGWI_SOCKET,
        "port" : WEBPORT
    }

    # upload_template("nginx.tpl", "%s%s"%(NGINX_VHOST_DIR,"nginx.conf"), context=nginx_context, use_jinja=True, use_sudo=True, backup=False)

    upload_template("nginx.tpl", "%savailable/%s"%(NGINX_VHOST_DIR,VHOST_NAME), context=nginx_context, use_jinja=True, use_sudo=True, backup=False)

    if not exists(os.path.join("%senabled/%s"%(NGINX_VHOST_DIR,VHOST_NAME))):
        sudo('ln -s %(src)s %(tar)s' % {'src': '%(nginx)savailable/%(vhost)s' % {'nginx': NGINX_VHOST_DIR, 'vhost': VHOST_NAME},'tar': '%(nginx)senabled/%(vhost)s' % {'nginx': NGINX_VHOST_DIR, 'vhost': VHOST_NAME}})

    if not exists(LOG_DIR):
        run('mkdir -p %s' % LOG_DIR)
        run('touch %s/access.log' % LOG_DIR)
        run('touch %s/error.log' % LOG_DIR)

def make_usgwi_config():
    usgwi_context={
        'pid' : TOPOGRAM_PID,
        'app' : CODE_DIR,
        'venv': VIRTUALENV_PATH,
        'module': 'run.py',
        'socket': USGWI_SOCKET
        }

    upload_template("usgwi_flask.tpl", USGWI_CONFIG_FILE, context=usgwi_context, use_jinja=True, use_sudo=True)

def make_gunicorn_config():
    gunicorn_context={
        'pid' : TOPOGRAM_PID,
        'app' : CODE_DIR,
        'venv': VIRTUALENV_PATH,
        'module': 'run.py',
        'socket': USGWI_SOCKET,
        'log' : LOG_DIR
    }

    upload_template("gunicorn.tpl",GUNICORN_CONFIG_FILE, context=gunicorn_context, use_jinja=True, use_sudo=True,backup=False)

def reload_webserver():
    sudo("sudo service nginx restart")

# supervisor
def stop_supervisor():
    sudo('supervisorctl stop %s' % VHOST_NAME)

def reload_supervisor():
    sudo('supervisorctl restart %s' % VHOST_NAME)

def start_app():
    sudo('supervisorctl start %s' % VHOST_NAME)

def restart_app():
    sudo('supervisorctl restart %s' % VHOST_NAME)

def reload_app(touch=True):
    if touch:
        with cd(APP_ROOT):
            run('touch app.wsgi')
        # start_app()
    else:
        sudo('supervisorctl restart %s' % VHOST_NAME)

def init_deploy():
    make_nginx_vhost("nginx_uwsgi.tpl")
    make_usgwi_config()
    make_supervisor_conf()

    reload_supervisor()
    reload_webserver()
    start_app()

def init_deploy_with_socketio():
    make_nginx_vhost("nginx_socketio.tpl")
    make_gunicorn_config()
    reload_webserver()
    # start_app()
    # gunicorn wsgi:app --debug --log-level debug -c tests/gunicorn.py

def deploy():
    reload_app()

def restart():
    reload_supervisor()
    reload_webserver()
