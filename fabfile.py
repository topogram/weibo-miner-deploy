import os
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib import files

from config.servers import staging, prod
import debian
import main
import nginx

CODE_DIR="/home/topo/"
DEPLOY_FILES_DIR=os.path.join(CODE_DIR,"topogram-deploy")
CONFIG_DIR=os.path.join(CODE_DIR,"config")

CONFIG_GITHUB_REP="https://github.com/topogram/topogram-deploy.git"

def uptime():
    run('uptime')

def ssh():
  for host in env.hosts:
        local("ssh-copy-id -p %s %s@%s" % (env.port, env.remote_admin, host))
def remote_info():
    run('uname -a')

def local_info():
    local('uname -a')

def git_pull():
    run("git pull")

def hostconfig():
    # debian.apt_upgrade()
    # debian.install_git()
    # debian.install_libs()
    # debian.install_mongodb()
    # debian.install_elasticsearch()
    # debian.install_virtualenv()
    # debian.install_nodejs()
    # debian.install_npm_global()
    # debian.install_nginx()
    # debian.install_supervisor()
    debian.install_uwsgi()

def topogram_setup():
    main.setup_topogram()
    nginx.init_deploy()

def deploy():
    main.update()
    nginx.deploy()

## functions
def run_test():
    with settings(warn_only=True):
        result = local('./manage.py test my_app', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()


"""
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
  # data.build_user_api()

def ui_dev_start():
    ui.dev_start()

"""
