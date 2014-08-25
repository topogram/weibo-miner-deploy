import os
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib import files

import debian
import miner
import ui
import data

CODE_DIR="/home/topo/"
DEPLOY_FILES_DIR=os.path.join(CODE_DIR,"topogram-deploy")
CONFIG_DIR=os.path.join(CODE_DIR,"config")

CONFIG_GITHUB_REP="https://github.com/topogram/topogram-deploy.git"

def staging():
    env.hosts = ['127.0.0.1']
    env.user  = 'topo'
    env.remote_admin  = 'topo'
    env.port="3022"
 
def uptime():
    run('uptime')

def production():
    env.hosts = ['X.X.X.X']
    env.remote_admin  = 'xxx'

def ssh():
  for host in env.hosts:
        local("ssh-copy-id -p %s %s@%s" % (env.port, env.remote_admin, host))

def remote_info():
    run('uname -a')

def local_info():
    local('uname -a')

def hostconfig():
    debian.apt_upgrade()
    debian.install_git()
    debian.install_libs()
    debian.install_mongodb()
    debian.install_nodejs()
    debian.install_elasticsearch()
    debian.install_npm_global()
    debian.install_virtualenv()

def setup_miner():
    miner.init_dir()
    # miner.update_requirements()
    # miner.install_zeroRPC()

def miner_dev_start():
    miner.dev_run()

def config_files():
    if not files.exists(DEPLOY_FILES_DIR):
        run("git clone %s" % CONFIG_GITHUB_REP )

    with cd(DEPLOY_FILES_DIR):
        git_pull()

    if not files.exists(CONFIG_DIR):
        run("ln -s %s/config %s" % (DEPLOY_FILES_DIR,CONFIG_DIR))

def setup_ui():
    ui.init_dir()
    ui.create_config_file()

def setup_data():
  data.init_dir()
  # data.download_weiboscope_sample()
  # data.build_index()
  # data.download_weiboscope_all()
  data.build_user_api()

def ui_dev_start():
    ui.dev_start()

def git_pull():
    run("git pull")
