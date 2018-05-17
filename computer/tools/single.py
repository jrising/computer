import sys, yaml
import configure
from local_server import LocalServer

with open(sys.argv[1], 'r') as fp:
    config = yaml.load(fp)

def connect(server):
    if not isinstance(server, LocalServer):
        server.connect()

    return server

server = configure.initialize_server(config, raw_input, connect)

command = ' '.join(sys.argv[2:])
output, error = server.run_command(command)

if error:
    print "ERROR:", error
print output
