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
          sudo('echo "deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen">mongodb.list')            
          sudo("sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10")
          apt_update()
          apt_install("mongodb-10gen")


def install_nodejs():
  listfile='chris-lea-node_js-natty.list'
  with cd(SOURCES_D):
      if not files.exists(listfile):
          files.append(listfile, "deb http://ppa.launchpad.net/chris-lea/node.js/ubuntu natty main", use_sudo=True)
          sudo("sudo apt-key adv --keyserver keyserver.ubuntu.com --recv C7917B12")
          apt_update()
  
  if not cmd_exists('node'):
      apt_install("nodejs nodejs-dev")

  #npm 
  if not cmd_exists('curl'):
      apt_install("curl")

  if not cmd_exists('npm'):
      sudo("curl http://npmjs.org/install.sh | sh")



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
