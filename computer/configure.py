import copy
from local_server import LocalServer
from login_server import LoginServer

server_types = {'local': LocalServer, 'login': LoginServer}

class UserException(Exception):
    pass

def config_or_prompt_several(mapping, config, prompter, callback):
    return config_or_prompt_remaining(copy.copy(mapping), mapping, copy.copy(config), config, prompter, callback)

def config_or_prompt_remaining(mapping, mapping_remaining, original_config, config, prompter, callback):
    key = mapping_remaining.keys()[0]
    if len(mapping_remaining) == 1:
        def getnext(config):
            try:
                return callback(config)
            except Exception as ex:
                print ex
                return config_or_prompt_several(mapping, original_config, prompter, callback)
    else:
        newmapping = copy.copy(mapping_remaining)
        del newmapping[key]
        def getnext(config):
            return config_or_prompt_remaining(mapping, newmapping, original_config, config, prompter, callback)
            
    return config_or_prompt(key, mapping[key], config, prompter, getnext)

def config_or_prompt(key, prompt, config, prompter, callback):
    """Get config value from either the config dict or a prompt; repeating as necessary until callback succeeds."""
    if key in config:
        return callback(config)

    config[key] = prompter(prompt)
    return callback(config)

def initialize_server(config, prompter, callback):
    assert 'type' in config and 'utup' in config and 'cpus' in config and 'roots' in config, "Incomplete configuration: always define type, utup, cpus, and roots."
    assert config['type'] in server_types, "Unknown server type %s" % config['type']

    Server = server_types[config['type']]

    if Server == LocalServer:
        return callback(LocalServer(config['utup'], config['cpus'], config['roots']))

    if Server == LoginServer:
        return callback(config_or_prompt_several({'domain': "Domain: ",
                                                  'username': "Username: ",
                                                  'password': "Password: "}, config, prompter,
                                                 lambda config: LoginServer(config['utup'], config['cpus'], config['roots'], config)))
    
    
