#!/bin/bash

# Simple script for installing ZeroRPC on Debian Wheezy

# System dependencies

# First install ZeroMQ
sudo apt-get install libzmq-dev

# Next install libevent, an event notification library required by zerorpc
sudo apt-get install libevent-dev

# Python dependencies

# Now install pyzmq: Python bindings for ZeroMQ
# If you don't already have pip installed:
sudo apt-get install python-setuptools
sudo apt-get install python-pip
sudo pip install pyzmq

# Now we can install ZeroRPC
sudo pip install zerorpc

# Node.js dependencies

# Just install the ZeroRPC node module
sudo npm install -g zerorpc