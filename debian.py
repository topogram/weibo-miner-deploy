from fabric.api import *
from fabric.contrib import files

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
  with cd("/tmp"):
    run("wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.3.2.deb")
    sudo("dpkg -i elasticsearch-1.3.2.deb ")
    # run("rm elasticsearch-1.3.2.deb")

    # start es by default
    #sudo update-rc.d elasticsearch defaults 95 10

def install_npm_global():
  run("npm -g install bower supervisor forever")

def upstart(appname, script, force=False, location_dir="/tmp", home="/root", user="root", description="Node.js server App"):
  dst="/etc/init/%s.conf" % appname
  logfile="/var/log/%s.log" % appname
  context = {'appname':appname
        , 'script':script
        , 'logfile':logfile
        , 'location_dir':location_dir
        , 'home':home
        , 'user':user
        , 'description':description}
  if not files.exists(dst) or force:
    files.upload_template('upstart.template'
      , dst
      , use_sudo=True
      , context=context)
    sudo("chown root:root %s" % dst)
    sudo("touch %s" % logfile)
    sudo("chown %(user)s:%(user)s %(logfile)s" % context)
