from __future__ import with_statement
from fabric.api import env
from fabric.api import *

from fabric.contrib.console import confirm
from fabric.contrib.project import upload_project
import ubuntu
import protobuf

def staging():
    env.hosts = ['10.100.0.70',]
    env.remote_admin = 'sysadmin'
 
 
def ssh():
  for host in env.hosts:
        local("ssh-copy-id %s@%s" % (env.remote_admin, host))


def hostconfig():
    ubuntu.apt_upgrade()
    ubuntu.install_git()
    ubuntu.install_mongodb()
    ubuntu.install_nodejs()


def install_protobuf():
    protobuf.install_protobuf()
    protobuf.install_protobuf_node()


def testapp():
    install_protobuf()
    with cd('~/projects'):
        upload_project('./receiver', '/home/sysadmin/projects')
    ubuntu.upstart("receiver", "app.js", 
        user=env.remote_admin
        , home="/home/%s" % env.remote_admin
        ,location_dir='/home/sysadmin/projects/receiver/')

    sudo("stop receiver")
    sudo("start receiver")
