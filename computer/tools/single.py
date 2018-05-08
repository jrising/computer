import sys, yaml
import configure

config = yaml.load(sys.argv[1])
server = configure.initialize_server(config, prompter)

command = ' '.join(argv[1:])
output, error = server.run_command(command)

if error:
    print "ERROR:", error
print output
