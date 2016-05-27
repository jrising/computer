import os, re
from process import RemoteProcess
from server import SizelessConnectableServer

class RemoteLinuxProcess(RemoteProcess):
    def __init__(self, server, pid, logfile):
        super(RemoteLinuxProcess, self).__init__(server, pid, logfile)

    def is_running(self):
        "Returns bool."
        lines = self.server.run_command("ps -l %d; echo $?" % (self.pid))[0].split('\n')
        if lines[-1] == '':
            lines = lines[:-1]
        return lines[-1] == '0'

    def kill(self):
        """
        Kill process if running
        """
        self.server.run_command("kill %d" % (self.pid))

    def halt(self):
        """Temporarily stop a process."""
        self.server.run_command("kill -STOP %d" % (self.pid))

    def resume(self):
        """Resume a halted process."""
        self.server.run_command("kill -CONT %d" % (self.pid))

    def clean(self):
        """
        Remove the log file
        """
        if self.logfile is not None:
            self.server.run_command("rm %s" % (self.logfile))

class SizelessLinuxServer(SizelessConnectableServer):
    def __init__(self, utup, cpus, roots, credentials):
        super(SizelessLinuxServer, self).__init__(utup, cpus, roots, credentials)

    def check_connection(self):
        if not self.connected:
            return False

        try:
            stdout, stderr = self.run_command("date")
            if stdout != '':
                return True
        except:
            pass

        self.connected = False
        return False

    # Basic operations

    def list_disk(self, path):
        """
        path: subdirectory
        """
        ansi_escape = re.compile(r'\x1b[^m]*m')
        stdout, stderr = self.run_command("ls -1 " + self.fullpath(path))
        for filename in stdout.split('\n'):
            yield ansi_escape.sub('', filename)

    def read_file(self, filepath=None):
        "Returns string."
        return self.run_command("cat " + self.fullpath(filepath) + "\n")[0]

    def start_process(self, command, path=None):
        logfile, stderr = self.run_command("mktemp")
        self.run_command("nohup %s >& %s &" % (command, logfile), path)

        pid = int(self.run_command("echo $!")[0].split('\n')[0])
        return RemoteLinuxProcess(self, pid, logfile)

    def cwd(self, path):
        self.run_command("cd " + path + "\n")

    def active_processes(self, procname):
        return int(self.run_command("ps -Af | grep " + procname + " | wc -l")[0]) - 1
