#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import StringIO
 
from fabric.api import *
from fabric.operations import get, put
from jinja2 import Template
 
env.hosts = ['vps']
env.user = "starenka"
 
VHOST = 'my.domain.net'
APPS_DIR = '/www'
APP_ROOT = '%s%s' % (APPS_DIR, VHOST.replace('.', '_'))
MODULE = 'main_app_module_filename'
 
REPOS = '/repos/hg'
STATIC = 'static'
SUPERVISOR_DIR = '/etc/supervisor/conf.d/'
NGINX_DIR = '/etc/nginx/sites-'

def render_template(string, context):
    return Template(string).render(context)

def make_supervisor_conf():
    template = StringIO.StringIO()
    get('%ssupervisor_flask.tpl' % SUPERVISOR_DIR, template)
    interpolated = StringIO.StringIO()
    interpolated.write(_render_template(template.getvalue(), {
        'domain': VHOST,
        'root': APP_ROOT,
        'module': MODULE
    }))
    put(interpolated, '%(supervisor_dir)s%(vhost)s.conf' % {'supervisor_dir': SUPERVISOR_DIR, 'vhost': VHOST},
        use_sudo=True)

def make_vhost():
    template = StringIO.StringIO()
    get('%snginx_flask.tpl' % NGINX_DIR, template)
    interpolated = StringIO.StringIO()
    interpolated.write(_render_template(template.getvalue(), {
        'domain': VHOST,
        'root': APP_ROOT,
        'static': STATIC
    }))
    put(interpolated, '%(nginx)savailable/%(vhost)s' % {'nginx': NGINX_DIR, 'vhost': VHOST}, use_sudo=True)
    sudo('ln -s %(src)s %(tar)s' % {'src': '%(nginx)savailable/%(vhost)s' % {'nginx': NGINX_DIR, 'vhost': VHOST},
                                    'tar': '%(nginx)senabled/%(vhost)s' % {'nginx': NGINX_DIR, 'vhost': VHOST}}
    )
    run('touch %s/access.log' % APP_ROOT)
    run('touch %s/error.log' % APP_ROOT)

def _reload_webserver():
    sudo("/etc/init.d/nginx reload")

def _reload_supervisor():
    sudo('supervisorctl update')

def _start_app():
    sudo('supervisorctl start %s' % VHOST)

def _reload_app(touch=True):
    if touch:
        with cd(APP_ROOT):
            run('touch app.wsgi')
    else:
        sudo('supervisorctl restart %s' % VHOST)
 
 
def init_deploy():
    _clone_repo()
    _make_vhost()
    _make_supervisor_conf()
    _reload_webserver()
    _reload_supervisor()
    _start_app()

def deploy():
    _update_repo()
    _reload_app()
