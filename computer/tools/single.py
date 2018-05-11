import sys, yaml
import configure

with open(sys.argv[1], 'r') as fp:
    config = yaml.load(fp)
server = configure.initialize_server(config, raw_input)

command = ' '.join(sys.argv[2:])
output, error = server.run_command(command)

if error:
    print "ERROR:", error
print output
