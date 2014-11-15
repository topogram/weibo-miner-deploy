from fabric.api import *
from fabric.contrib import files

from config.settings import RUN_DIR

SOURCES_D="/etc/apt/sources.list.d"

__all__= ['cmd_exists', 'apt', 'apt_upgrade']

def cmd_exists(cmd):
  #TODO: some sort of run test of the command perhaps
  return files.exists("/usr/bin/%s" % cmd)

def apt(cmdline):
  if not cmd_exists('aptitude'):
        sudo("apt-get -y install aptitude")
  sudo("aptitude %s" % cmdline)

def apt_install(packages):
    apt("-y install %s" % packages)

def apt_update():
    apt("update")

def apt_upgrade():
    apt_update()
    apt("-y safe-upgrade")

def install_git():
  if not cmd_exists('git'):
      apt_install("build-essential git git-core")
      run("git config --global color.ui true")

def install_mongodb():
  with cd(SOURCES_D):
      if not files.exists('mongodb.list'):
          sudo('echo "deb http://downloads-distro.mongodb.org/repo/debian-sysvinit dist 10gen">mongodb.list')            
          sudo("sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10")
          apt_update()
          apt_install("mongodb-org")

def install_nodejs():
  run("source ~/.bashrc")

  if not cmd_exists('node'):
    with cd("/tmp"):
      # get nvm
      run("wget https://raw.githubusercontent.com/creationix/nvm/v0.13.1/install.sh")
      run("bash install.sh")

      # install node
      run("nvm install v0.10.26")
      run("nvm use v0.10.26")
      run("nvm alias default v0.10.26")

      # add to path
      run("echo . ~/.nvm/nvm.sh >> ~/.bashrc")
      run("source ~/.bashrc")

      # run("rm install.sh")

def install_elasticsearch():
  apt_install("")

  if not sudo("service elasticsearch status"):
    with cd("/tmp"):
      run("wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.3.2.deb")
      sudo("dpkg -i elasticsearch-1.3.2.deb ")

  if not files.exists('/usr/share/elasticsearch/config'):
    sudo("ln -s /etc/elasticsearch /usr/share/elasticsearch/config")
    sudo(" echo 'path.logs: /usr/share/elasticsearch/logs' >>  /etc/elasticsearch/elasticsearch.yml ")

  # install plugins
  if not files.exists('/usr/share/elasticsearch/plugins/head'):
    sudo ("/usr/share/elasticsearch/bin/plugin -install mobz/elasticsearch-head")

  if not files.exists('/usr/share/elasticsearch/plugins/analysis-smartcn'):
    sudo ("/usr/share/elasticsearch/bin/plugin -install elasticsearch/elasticsearch-analysis-smartcn/2.1.0")

  sudo("service elasticsearch start")
  # sudo("service elasticsearch status")

def install_libs():
  apt_install("install python-dev libzmq-dev libevent-dev python-setuptools python-pip python-zmq curl openjdk-7-jdk")
  sudo(" update-alternatives --config java")

def install_npm_global():
  run("npm -g install bower supervisor forever")

  # if not files.exists('/usr/local/bin/zerorpc'):
  #   install_libs()
  # run("npm install -g zerorpc")

def install_virtualenv():
    sudo_pip_install('virtualenv')
    
def sudo_pip_install(packages):
    sudo("pip install %s" % packages)

def install_nginx():
  apt_install("nginx")
  sudo("service nginx start")

def install_supervisor():
  apt_install("supervisor")

def install_uwsgi():
  apt_install("uwsgi")
  if not files.exists(RUN_DIR):
    sudo("mkdir -p %s"%RUN_DIR)
  sudo('chown www-data:www-data %s'%RUN_DIR)


# def upstart(appname, script, force=False, location_dir="/tmp", home="/root", user="root", description="Node.js server App"):
#   dst="/etc/init/%s.conf" % appname
#   logfile="/var/log/%s.log" % appname
#   context = {'appname':appname
#         , 'script':script
#         , 'logfile':logfile
#         , 'location_dir':location_dir
#         , 'home':home
#         , 'user':user
#         , 'description':description}
#   if not files.exists(dst) or force:
#     files.upload_template('upstart.template'
#       , dst
#       , use_sudo=True
#       , context=context)
#     sudo("chown root:root %s" % dst)
#     sudo("touch %s" % logfile)
#     sudo("chown %(user)s:%(user)s %(logfile)s" % context)
