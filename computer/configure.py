from local_server import LocalServer
from login_server import LoginServer

server_types = {'local': LocalServer, 'login': LoginServer}

class UserException(Exception):
    pass

def config_or_prompt_several(mapping, config, prompter, callback):
    for key in mapping:
        config_or_prompt(key, mapping[key], config, prompter, ...)
        ## TODO: Think through this.  If fail, want to go through
        ## entire list again.
        
        return callback(config)
        
def config_or_prompt(key, prompt, config, prompter, callback):
    try:
        if key in config:
            return callback(config)
    except UserException as ex:
        print ex
    except ex:
        print "Unknown error.  Please try again."
    finally:
        config[key] = prompter(prompt)
        return config_or_prompt(key, prompt, config, prompter)

def initialize_server(config, prompter):
    assert 'type' in config and 'utup' in config and 'cpus' in config and 'roots' in config, "Incomplete configuration: always define type, utup, cpus, and roots."
    assert config['type'] in server_types, "Unknown server type %s" % config['type']

    Server = server_types[config['type']]

    if Server == LocalServer:
        return Server(config['utup'], config['cpus'], config['roots'])

    if Server == LoginServer:
        config_or_prompt('username', "Username:", config, prompter)
        username = prompter("username")
        
