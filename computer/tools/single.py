import sys, yaml
import configure

config = yaml.load(sys.argv[1])
server = configure.initialize_server(config, prompter)

## TODO: Now run the rest of sys.argv on that server and print result
