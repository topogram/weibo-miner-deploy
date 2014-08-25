from fabric.api import *
import debian
from fabvenv import make_virtualenv, virtualenv


def install_virtualenv():
    sudo_pip_install('virtualenv')

def create_virtual_env():
    virtualenv_path="/home/%s/%s"%(env.user,'topogram_env')
    make_virtualenv(virtualenv_path)

def install_zeroRPC():
  virtualenv_path="/home/%s/%s"%(env.user,'topogram_env')
  debian.apt_install("install python-dev libzmq-dev libevent-dev python-setuptools python-pip python-zmq")
  with virtualenv(virtualenv_path):
    pip_install("pyzmq zerorpc")
  run("npm install -g zerorpc")

def pip_install(packages):
    run("pip install %s" % packages)

def sudo_pip_install(packages):
    sudo("pip install %s" % packages)

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

def deploy():
    code_dir = '/srv/django/myproject'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone user@vcshost:/path/to/repo/.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")
