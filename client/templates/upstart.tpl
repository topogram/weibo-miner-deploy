## /etc/init/{{name}}.conf

description "{{url}}"
author      "{{email}}"

# Automatically Run on Startup
start on started mountall
stop on shutdown

# Automatically Respawn:
respawn
respawn limit 99 5

script
    export HOME="{{root}}"
    export MONGO_URL='mongodb://{{mongo.host}}:{{mongo.port}}/meteor'
    export ROOT_URL='https://{{url}}'
    export PORT='{{port}}'

    exec /usr/local/bin/node {{root}}/main.js >> /var/log/myapp.log 2>&1
end script
