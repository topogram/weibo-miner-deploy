#!/bin/bash
 
echo "+Adding nginx repositories..."
echo "" >> /etc/apt/sources.list
echo "deb http://nginx.org/packages/debian/ squeeze nginx" >> /etc/apt/sources.list
echo "deb-src http://nginx.org/packages/debian/ squeeze nginx" >> /etc/apt/sources.list
gpg --keyserver keyserver.ubuntu.com --recv-key ABF5BD827BD9BF62
gpg -a --export ABF5BD827BD9BF62 | apt-key add -
apt-get update
 
echo "+Installing nginx package..."
if [ $(uname -m) == 'x86_64' ]; then
  wget http://snapshot.debian.org/archive/debian/20110406T213352Z/pool/main/o/openssl098/libssl0.9.8_0.9.8o-7_amd64.deb
  dpkg -i libssl0.9.8_0.9.8o-7_amd64.deb
  rm libssl0.9.8_0.9.8o-7_amd64.deb
else
  wget http://snapshot.debian.org/archive/debian/20110406T213352Z/pool/main/o/openssl098/libssl0.9.8_0.9.8o-7_i386.deb
  dpkg -i libssl0.9.8_0.9.8o-7_i386.deb
  rm libssl0.9.8_0.9.8o-7_i386.deb
fi
apt-get update
apt-get install -q -y nginx
