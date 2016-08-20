import os, subprocess, shlex, signal
from server import SizelessServer
from process import SingleCPUProcess

class LocalProcess(SingleCPUProcess):
    def __init__(self, server, proc, stdout, logfile):
        super(LocalProcess, self).__init__(server, logfile)
        self.proc = proc
        self.stdout = stdout

    def is_running(self):
        self.proc.poll()
        return self.proc.returncode is None

    def kill(self):
        self.proc.kill()
        self.stdout.close()

    def halt(self):
        """Temporarily stop a process."""
        self.proc.signal(signal.SIGSTOP)

    def resume(self):
        """Resume a halted process."""
        self.proc.signal(signal.SIGCONT)

    def clean(self):
        if self.logfile is not None:
            os.unlink(self.server.fullpath(self.logfile))

class LocalServer(SizelessServer):
    def __init__(self, cpus, roots):
        super(LocalServer, self).__init__((), cpus, roots)

    def list_disk(self, path=None):
        if path is not None:
            os.chdir(self.fullpath(path))
        for root, dirs, files in os.walk('.'):
            for dir in dirs:
                yield os.path.normpath(os.path.join(root, dir))
            for file in files:
                yield os.path.normpath(os.path.join(root, file))

    def has_file(self, path):
        return os.path.exists(self.fullpath(path))

    def read_file(self, path):
        with open(self.fullpath(path), 'r') as fp:
            return fp.read()

    def start_process(self, command, logfile, path=None):
        fp = open(self.fullpath(logfile), 'w')
        proc = subprocess.Popen(shlex.split(command), cwd=self.fullpath(path), stdout=fp)
        return LocalProcess(self, proc, fp, logfile)

    def run_command(self, command, path=None):
        if path is not None:
            os.chdir(self.fullpath(path))
        return (os.popen(command).read(), "")

    def run_interactive(self, command, path=None):
        if path is not None:
            os.chdir(self.fullpath(path))
        proc = subprocess.Popen(shlex.split(command), cwd=self.fullpath(path), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        return proc.stdin, proc.stdout, proc.stderr

if __name__ == '__main__':
    server = LocalServer(1, {})
    stdin, stdout, stderr = server.run_interactive('python -c "import sys\nprint \'Welcome.  More input!\'\nsys.stdout.flush()\nwhile True:\n  print \'Got: \' + raw_input()\n  sys.stdout.flush()\nprint \'Done.\'"')

    # Reading suggestion from http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
    # Writing suggestion from http://stackoverflow.com/questions/3762881/how-do-i-check-if-stdin-has-some-data
    import sys, select
    from threading  import Thread

    try:
        from Queue import Queue, Empty
    except ImportError:
        from queue import Queue, Empty  # python 3.x

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

