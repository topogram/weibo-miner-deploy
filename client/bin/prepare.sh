#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..
pwd

# build app
if [ -d "topogram-client" ]; then
    cd topogram-client
    git pull origin master
else
    git clone https://github.com/topogram/topogram-client
    cd topogram-client
fi

# build meteor for deployment
meteor build --directory ../build


