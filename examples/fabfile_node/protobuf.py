from fabric.api import *
from fabric.contrib import files
import ubuntu


def install_protobuf():
  if not ubuntu.cmd_exists('protoc'):
    version="2.4.1"
    folder="protobuf-%s" % version
    filename="%s.tar.bz2" % folder
    source="http://protobuf.googlecode.com/files/%s" & filename
    with cd('/tmp'):
      run("wget %s" % source)
      run("tar -jxf %s" % filename)
    with cd('/tmp/%s' % folder):
      run("./configure --prefix=/usr")
      run("make")
      sudo("make install")

    with cd('/tmp/'):
      run("rm -Rf %s*" % folder)


def install_protobuf_node():
  if not files.exists(".node_libraries/protobuf_for_node.node"):
    if not ubuntu.cmd_exists('hg'):
      ubuntu.apt_install('mercurial')

    source="hg clone https://code.google.com/p/protobuf-for-node/"

    with cd('/tmp'):
      run(source)
    with cd('/tmp/protobuf-for-node'):
      run("PROTOBUF=/usr node-waf configure clean build")
      run("node-waf install")

    with cd('/tmp'):
      run("rm -Rf protobuf-for-node")


