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
    def __init__(self, utup, cpus, roots):
        super(LocalServer, self).__init__(utup, cpus, roots)

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

