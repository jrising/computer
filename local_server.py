import os, subprocess, shlex
from server import SizelessServer
from process import SingleCPUProcess

class LocalProcess(SingleCPUProcess):
    def __init__(self, proc, stdout, logfile):
        super(LocalProcess, self).__init__(logfile)
        self.proc = proc
        self.stdout = stdout

    def is_running(self):
        self.proc.poll()
        return self.proc.returncode is None

    def kill(self):
        self.proc.kill()
        self.stdout.close()

    def clean(self):
        os.unlink(logfile)

class LocalServer(SizelessServer):
    def __init__(self, cpus, roots):
        super(LocalServer, self).__init__(cpus, roots)

    def list_disk(self, root, path):
        for root, dirs, files in os.walk(self.fullpath(root, path)):
            for dir in dirs:
                yield os.path.normpath(os.path.join(root, dir))
            for file in files:
                yield os.path.normpath(os.path.join(root, file))

    def has_file(self, root, path):
        return os.path.exists(self.fullpath(root, path))

    def read_file(self, root, path):
        with open(self.fullpath(root, path), 'r') as fp:
            return fp.read()

    def start_process(self, root, path, command, logfile):
        fp = open(logfile, 'w')
        proc = subprocess.Popen(shlex.split(command), cwd=self.fullpath(root, path), stdout=fp)
        return LocalProcess(proc, fp, logfile)

    def run_command(self, root, path, command):
        proc = subprocess.Popen(shlex.split(command), cwd=self.fullpath(root, path), stdout=subprocess.PIPE)
        return proc.communicate()[0]

