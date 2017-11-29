def execute(server, commands):
    import warnings
    
    for command in commands:
        stdout, stderr = server.run_command(command)
        print stdout
        if stderr:
            warnings.warn(stderr)

def interact(server):
    # Reading suggestion from http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
    # Writing suggestion from http://stackoverflow.com/questions/3762881/how-do-i-check-if-stdin-has-some-data
    import sys, select
    from threading  import Thread

    try:
        from Queue import Queue, Empty
    except ImportError:
        from queue import Queue, Empty  # python 3.x

    stdin, stdout, stderr = server.run_interactive('python -c "import sys\nprint \'Welcome.  More input!\'\nsys.stdout.flush()\nwhile True:\n  print \'Got: \' + raw_input()\n  sys.stdout.flush()\nprint \'Done.\'"')

    def enqueue_output(out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

    qout = Queue()
    tout = Thread(target=enqueue_output, args=(stdout, qout))
    tout.daemon = True # thread dies with the program
    tout.start()

    qerr = Queue()
    terr = Thread(target=enqueue_output, args=(stderr, qerr))
    terr.daemon = True # thread dies with the program
    terr.start()

    while True:
        stdin.flush()
        sys.stdout.flush()

        try:
            line = qout.get_nowait()
        except Empty:
            pass
        else:
            print line

        try:
            line = qerr.get_nowait()
        except Empty:
            pass
        else:
            print "ERROR:", line

        hasinputs = select.select([sys.stdin],[],[],0.0)[0]
        for hasinput in hasinputs:
            line = sys.stdin.readline()
            stdin.write(line)

            if line[-1] == '\n':
                line = line[:-1]

def handle(server, commands=None):
    import sys

    if commands is None:
        commands = sys.argv[1:]
        
    if len(commands) > 0:
        execute(server, commands)
    else:
        interact(server)

