from fabric.api import *
from fabric.contrib import files
import debian
import os

UI_GITHUB_REP="https://github.com/topogram/topogram-ui.git"

CODE_DIR="/home/topo/"
CONFIG_DIR=os.path.join(CODE_DIR,"config")
UI_DIR=os.path.join(CODE_DIR,"topogram-ui")
UI_CONFIG_DIR=os.path.join(UI_DIR, "config")

def init_dir():
    if not files.exists(UI_DIR):
        # run("mkdir -p %s" % UI_CODE_DIR)
        run("git clone %s" % UI_GITHUB_REP )

    with cd(UI_DIR):
        git_pull()
        npm_install()
        bower_install()

def npm_install():
    with cd(UI_DIR):
        run("npm install")

def bower_install():
    with cd(UI_DIR):
        run("bower install")

def git_pull():
    run("git pull")

def dev_start():
    with cd(UI_DIR):
        run("./dev_start.sh")

def create_config_file():
    if files.exists(CONFIG_DIR) and not files.exists(UI_CONFIG_DIR) :
        run('ln -s %s %s' % (CONFIG_DIR, UI_CONFIG_DIR))
