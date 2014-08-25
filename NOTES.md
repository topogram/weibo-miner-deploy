# Deploy notes

* Manage remote daemons with supervisord
    http://supervisord.org/    

* Manage python packages with pip (and use `pip freeze`)
    http://pypi.python.org/pypi/pip
    http://www.pip-installer.org/en/latest/requirements.html

* Manage production environments with virtualenv
    http://www.virtualenv.org/

* Manage Configuration 
    http://puppetlabs.com/
    http://www.opscode.com/chef/ (requires Ruby)
    http://ansible.github.com (Python core)
    https://github.com/sebastien/cuisine (chef-like functionality to fabric.)

* Automate local and remote sys admin tasks with Fabric
    http://fabfile.org

* Celery for task management
    http://celeryproject.org/

* Twisted for event-based python.
    http://twistedmatrix.com/trac/

* nginx / gunicorn for your python web server stack
    http://www.nginx.com/
    http://gunicorn.org/

NB : Strongly consider rolling your own DEB/RPMs for your Python application. 



# HOWTO Install Mitras
tested on Debian Server Wheezy


## Setup VirtualBox

#### SSH setup

After Ubuntu install :
* install ssh on the server : ```$ apt-get install openssh-server```
* go to Settings > Network 
* Select NAT
* Then click on Port Forwarding button. 
* Add a new Rule: "Host port 3022, guest port 22, name ssh, other left blank."

You can now ssh on the server : 

    $ ssh -p 3022 mitras@127.0.0.1

#### Port forwarding
(the VM should be shutdown for a 2nd adapter)

Bridge to use the server with a domain name
    * Settings / Network
    * Select Adapter 2 (Adapter 1 is your ssh)

### Prepare server

    sudo apt-get update
    sudo apt-get -y install build-essential libssl-dev curl git
    apt-get upgrade

You may need a specific user : 

    adduser mitras

### Install node/npm via nvm

    cd ~
    git clone git://github.com/creationix/nvm.git
    . ~/nvm/nvm.sh

    nvm install v0.8.8
    nvm use v0.8.8
    nvm alias default v0.8.8
    # npm is now bundled in node !

Add nvm to bash profile

    echo "source ~/.nvm/nvm.sh" >> ~/.bashrc
    source ~/.bashrc
    ~/.bashrc

### Install MongoDB

    sudo apt-get install mongodb

    sudo service mongodb status
    # mongodb start/running, process 21090

    # may be useful for newest version of mongo... 
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
    touch /etc/apt/sources.list.d/10gen.list
    "deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen"
    sudo apt-get update


### Install Nginx

    # install latest version
    sudo apt-get install python-software-properties
    sudo add-apt-repository ppa:nginx/stable
    sudo apt-get update
    sudo apt-get install nginx

    # fix apache config 
    sudo service apache2 stop
    update-rc.d apache remove   # prevent apache from loading at start

    sudo service nginx start
    update-rc.d nginx defaults   # ensure be up after reboots


### Install Redis 
    
    sudo apt-get install redis-server
    sudo update-rc.d redis-server defaults

### Install neo4j

    bash setup/install_neo4j.sh

## Deployment & config

### Config Nginx

    sudo cat /etc/nginx/sites-available/default
    
Create a config file for your Nginx host

```sudo nano /etc/nginx/sites-available/mitras```

Copy paste ```mitrax-nginx.conf```

Save and enable the site on nginx

    sudo ln -s /etc/nginx/sites-available/mitras /etc/nginx/sites-enabled/mitras
    # test
    nginx -t
    # reload
    nginx -s reload

### Web server with Capistrano

You need ruby (1.9.7 using rvm recommended)
    
    gem install capistrano
    gem install capistrano-ext

Then you can deploy
    
    cd mitras-conf
    cap -t
    cap deploy:setup
    cap deploy:check
    cap deploy

### Create config files

    cd config
    cp db.json.sample db.json
    cp apikeys.json.sample apikeys.json

Fill the config files with your db information and API credentials

## Install NEO4J

Install as a service
    
    # get java
    sudo apt-get install openjdk-6-jre-headless

    #get latest release
    curl -O http://dist.neo4j.org/neo4j-community-1.9.2-unix.tar.gz
    tar -xf neo4j-community-*.tar.gz
    rm neo4j-community-*.tar.gz
    
    # test it
    neo4j-community-1.9.2/bin/neo4j start
    neo4j-community-1.9.2/bin/neo4j stop

    # Install as a service

    # add path 
    export NEO4J_HOME=/home/clemsos/Softwares/neo4j-community-1.9.2 >> ~/.bashrc

    # install
    sudo neo4j-community-1.9.2/bin/neo4j install

    # now you can do
    sudo service neo4j-service start


http://www.genericarticles.com/mediawiki/index.php?title=Installing_Neo4j_in_Linux#As_a_Linux_Service
