# Topogram deploy

Setup and deployment scripts for Topogram app.

## Deploy

Tested on Debian Wheezy.

Edit ```config/servers.py``` and ```config/settings.py``` according to your needs.

    pip install -r requirements
    fab prod hostconfig # install tools on debian  
    fab prod config_server # write nginx and gunicorn files
    fab prod setup # install virtualenv, pip and deps
    fab prod deploy # update code, upgrade db and reload app

### Use on Virtual Box

    * go to Settings > Network
    * Select NAT
    * Then click on Port Forwarding button.
    * Add a new Rule: "Host port 3022, guest port 22, name ssh, other left blank."

You can now ssh on the server :

    ssh -p 3022 topo@127.0.0.1
    adduser topo sudo


### Installed Deps

Tested on Debian Wheezy

    nvm
    node v10.x
    python 2.7
    MongoDB
    elasticsearch
