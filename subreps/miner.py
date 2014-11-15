from fabric.api import *
import debian
from fabvenv import make_virtualenv, virtualenv
import os
from fabric.contrib import files


MINER_GITHUB_REP="https://github.com/topogram/topogram-miner.git"

CODE_DIR="/home/topo/"
CONFIG_DIR=os.path.join(CODE_DIR,"config")
MINER_DIR=os.path.join(CODE_DIR,"topogram-miner")
MINER_CONFIG_DIR=os.path.join(MINER_DIR, "config")

VIRTUALENV_PATH=os.path.join(CODE_DIR,'env')
# env.virtualenv_root

def init_dir():
    if not files.exists(MINER_DIR):
        run("git clone %s" % MINER_GITHUB_REP )

    if not files.exists(VIRTUALENV_PATH):
      make_virtualenv(VIRTUALENV_PATH)

    update()

def update_requirements():
  """ update external dependencies on remote host """
  with virtualenv(VIRTUALENV_PATH):
    cmd = ['pip install']
    cmd += ['--requirement %s' %  os.path.join(MINER_DIR,'requirements.txt')]
    run(' '.join(cmd))

def update():
  with cd(MINER_DIR):
    git_pull()
    update_requirements()

def dev_run():
  update()
  with virtualenv(VIRTUALENV_PATH):
    run("python %s" % os.path.join(MINER_DIR,"server.py"))

def git_pull():
    run("git pull")
