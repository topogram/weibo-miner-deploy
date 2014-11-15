# Topogram deploy

Setup and deployment scripts for Topogram app.

## Deploy

Tested on debian Wheezy. You will need openSSH server and mail

    pip install fabric fabric-virtualenv
    fab staging ssh         # setup ssh remote key
    fab staging hostconfig  # setup tools
    

    fab staging setup_topogram  # update code and dependencies

    fab staging uptime


### Virtual Box

    * go to Settings > Network 
    * Select NAT
    * Then click on Port Forwarding button. 
    * Add a new Rule: "Host port 3022, guest port 22, name ssh, other left blank."

You can now ssh on the server : 

    ssh -p 3022 topo@127.0.0.1
    adduser topo sudo


## Spec

The Topogram application consists of three main parts :

* [Data](https://github.com/topogram/topogram-data)     : data storage (bash / mongo / elasticsearch)
* [Miner](https://github.com/topogram/topogram-miner)   : mining workflow (Python)
* [UI](https://github.com/topogram/topogram-ui)         : visualization (Node / Javascript)

## Requirements

Tested on Debian Wheezy

    nvm
    node v10.x
    python 2.7
    MongoDB
    elasticsearch
