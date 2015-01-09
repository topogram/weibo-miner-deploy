from fabric.api import *
import os

from fabric.contrib.console import confirm
from fabric.contrib import files
from fabvenv import virtualenv, make_virtualenv
from config.settings import *

def create_config_files():

    if not files.exists(CONFIG_DIR):
        run("mkdir -p %s"%CONFIG_DIR)
        with cd(CONFIG_DIR):
            run('cp %s %s' % (os.path.join(CODE_DIR, "config.py.sample"), "config.py"))

    if files.exists(os.path.join(CONFIG_DIR,"config.py")) and not files.exists(os.path.join(CODE_DIR, "config.py")) :

            run('ln -s %s %s' % (os.path.join(CONFIG_DIR,"config.py"), os.path.join(CODE_DIR, "config.py")))

def create_uploads_dir():
    run("mkdir -p %s"%UPLOADS_DIR)

# def create_db_dir():
#     run("mkdir -p %s"%DB_DIR)

def create_virtual_env():
    if not files.exists(VIRTUALENV_PATH):
        make_virtualenv(VIRTUALENV_PATH)

def setup_topogram():
    update_code_from_git()
    create_config_files()
    create_virtual_env()
    update_requirements()
    create_uploads_dir()
    # if not files.exists(DB_DIR): # for SQLite
    if not files.exists(DB_PATH):
        create_db()
    update()
    install_gunicorn()

def update():
    update_code_from_git()
    update_requirements()
    bower_install()
    update_db()

def update_code_from_git():
    """ download latest version of the code from git """
    if not files.exists(CODE_DIR):
        run("git clone %s" % MAIN_GITHUB_REP )

    with cd(CODE_DIR):
        git_pull()

def update_requirements():
    """ update external dependencies on remote host """

    with virtualenv(VIRTUALENV_PATH):
        cmd = ['pip install']
        cmd += ['--requirement %s' %  os.path.join(CODE_DIR,'requirements.txt')]
        run(' '.join(cmd))

def bower_install():
    with cd(CODE_DIR):
        run("bower install")

def create_db():
    # create_db_dir()
    with virtualenv(VIRTUALENV_PATH):
        run("python %s" % os.path.join(CODE_DIR,"manage.py db upgrade"))

def update_db():
    with virtualenv(VIRTUALENV_PATH):
        run("python %s" % os.path.join(CODE_DIR,"manage.py db upgrade"))

def dev_run():
  update()
  with virtualenv(VIRTUALENV_PATH):
    run("python %s" % os.path.join(CODE_DIR,"run.py"))

def git_pull():
    run("git pull")

def install_gunicorn():
  with virtualenv(VIRTUALENV_PATH):
    run("pip install gunicorn==0.16.1")
  
