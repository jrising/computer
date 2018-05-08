from local_server import LocalServer
from login_server import LoginServer

server_types = {'local': LocalServer, 'login': LoginServer}

class UserException(Exception):
    pass

def config_or_prompt_several(mapping, config, prompter, callback):
    config_or_prompt_remaining(copy.copy(mapping), mapping, copy.copy(config), config, prompter, callback)

def config_or_prompt_remaining(mapping, mapping_remaining, original_config, config, prompter, callback):
    key = mapping.next()
    if len(mapping) == 1:
        def getnext(config):
            try:
                callback(config)
            except:
                config_or_prompt_several(mapping, original_config, prompter, callback)
    else:
        newmapping = copy.copy(mapping)
        del newmapping[key]
        def getnext(config):
            config_or_prompt_remaining(mapping, newmapping, original_config, config, prompter, callback)
            
    return config_or_prompt(key, mapping[key], config, prompter, getnext)

def config_or_prompt(key, prompt, config, prompter, callback):
    """Get config value from either the config dict or a prompt; repeating as necessary until callback succeeds."""
    try:
        if key in config:
            return callback(config)
    except ex:
        print ex
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
        
