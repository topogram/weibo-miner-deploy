from fabric.api import *
import os

from fabric.contrib.console import confirm
from fabric.contrib import files
from fabvenv import virtualenv

DATA_GITHUB_REP="https://github.com/topogram/topogram-data.git"

CODE_DIR="/home/topo/"

DATA_DIR=os.path.join(CODE_DIR,"topogram-data")
RAW_DATA_DIR=os.path.join(CODE_DIR,"data")

VIRTUALENV_PATH=os.path.join(CODE_DIR,'env')

# CONFIG_DIR=os.path.join(CODE_DIR,"config")
# DATA_CONFIG_DIR=os.path.join(DATA_DIR, "config")

def init_dir():
    if not files.exists(DATA_DIR):
        run("git clone %s" % DATA_GITHUB_REP )
    with cd(DATA_DIR):
        git_pull()
    update_requirements()

def download_weiboscope_all():
    with cd(DATA_DIR):
        run("bash dl_raw_data.sh")

def download_weiboscope_sample():
    if not files.exists(RAW_DATA_DIR):
        run("mkdir -p %s"%RAW_DATA_DIR)

    download_weiboscope_week(5)

def download_weiboscope_week(week):
    # print os.path.join(RAW_DATA_DIR,"week%s.zip"%week)

    if not files.exists(os.path.join(RAW_DATA_DIR,"week%s"%week)) and not files.exists(os.path.join(RAW_DATA_DIR,"week%s.zip"%week)):
        with cd(CODE_DIR):
            cmd = ["wget -O"]
            cmd += [os.path.join(RAW_DATA_DIR,("week%s.zip" % week))]
            cmd += ["http://147.8.142.179/datazip/week%s.zip"%week]
            run(' '.join(cmd))

def build_index():
    run("sudo /etc/init.d/elasticsearch restart")
    with cd(CODE_DIR):
        with virtualenv(VIRTUALENV_PATH):
            run("python %s %s" % (os.path.join(DATA_DIR,"es_build_index.py"),RAW_DATA_DIR))

def build_user_api():
    if not files.exists(os.path.join(RAW_DATA_DIR,"userdata.zip")):
        cmd = ["wget -O"]
        cmd += [os.path.join(RAW_DATA_DIR,"userdata.zip")]
        cmd += ["http://147.8.142.179/datazip/userdata.zip"]
        run(' '.join(cmd))

    with cd(RAW_DATA_DIR):
        if not files.exists(os.path.join(RAW_DATA_DIR,"userdata.csv")):
            run("unzip %s" % os.path.join(RAW_DATA_DIR,"userdata.zip"))

    with virtualenv(VIRTUALENV_PATH):
        run("python %s %s" % (os.path.join(DATA_DIR,"utils_build_user_api.py"),os.path.join(RAW_DATA_DIR,"userdata.zip")))

def git_pull():
    run("git pull")

def update_requirements():
  """ update external dependencies on remote host """
  with virtualenv(VIRTUALENV_PATH):
    cmd = ['pip install']
    cmd += ['--requirement %s' %  os.path.join(DATA_DIR,'requirements.txt')]
    run(' '.join(cmd))
