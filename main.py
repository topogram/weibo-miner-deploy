from fabric.api import *
import os

from fabric.contrib.console import confirm
from fabric.contrib import files
from fabvenv import virtualenv, make_virtualenv

MAIN_GITHUB_REP="https://github.com/topogram/topogram.git"

HOME_DIR="/home/topo/"
CODE_DIR=os.path.join(HOME_DIR,"topogram")
VIRTUALENV_PATH=os.path.join(HOME_DIR,'env')
CONFIG_DIR=os.path.join(HOME_DIR,"config")

def create_config_files():

    if not files.exists(CONFIG_DIR):
        run("mkdir -p %s"%CONFIG_DIR)
        with cd(CONFIG_DIR):
            run('cp %s %s' % (os.path.join(CODE_DIR, "config.py.sample"), "config.py"))

    if files.exists(os.path.join(CONFIG_DIR,"config.py")) and not files.exists(os.path.join(CODE_DIR, "config.py")) :

            run('ln -s %s %s' % (os.path.join(CONFIG_DIR,"config.py"), os.path.join(CODE_DIR, "config.py")))

def create_virtual_env():
    if not files.exists(VIRTUALENV_PATH):
        make_virtualenv(VIRTUALENV_PATH)

def setup_topogram():
    create_config_files()
    create_virtual_env()
    update()

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
    update_requirements()

def update_requirements():
    """ update external dependencies on remote host """

    with virtualenv(VIRTUALENV_PATH):
        cmd = ['pip install']
        cmd += ['--requirement %s' %  os.path.join(CODE_DIR,'requirements.txt')]
        run(' '.join(cmd))

def bower_install():
    with cd(CODE_DIR):
        run("bower install")

def update_db():
    with cd(os.path.join(CODE_DIR)):
        run('python db_create.py')

def dev_run():
  update()
  with virtualenv(VIRTUALENV_PATH):
    run("python %s" % os.path.join(MINER_DIR,"run.py"))

def git_pull():
    run("git pull")
