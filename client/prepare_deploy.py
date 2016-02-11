import os
import json
from jinja2 import Environment, FileSystemLoader

CONFIG_ENV = "production"

# Read template in the file
env = Environment(loader=FileSystemLoader('templates'))
upstart_template = env.get_template('upstart.tpl')

# load config
with open('./config.json') as f:
    conf_file = json.load(f)
    conf = conf_file[CONFIG_ENV]

    #upstart
    upstart_conf = upstart_template.render(conf)
    print upstart_conf

    # Save the results
    upstart_conf_path = os.path.join('./deploy/', conf["name"]+'_upstart.conf')
    with open(upstart_conf_path, 'wb') as conf :
        conf.write(upstart_conf)



