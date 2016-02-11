# Topogram-client deploy scripts

You need to edit ```config.json``` file to fit your needs.

### create upstart config

upstart config file will be written in ```deploy/upstart.conf``` 

    pip install -r requirements.txt
    python prepare_deploy.py # 


### prepare meteor files

    ./bin/prepare.sh

### copy file to server

    scp ./build user@host:/deploy-dir
