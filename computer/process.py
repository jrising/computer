class SingleCPUProcess(object):
    def __init__(self, server, pid, logfile=None):
        self.server = server
        self.logfile = logfile
        self.pid = pid

    def is_running(self):
        "Returns bool."
        raise NotImplemented()

    def close(self):
        if self.is_running():
            self.kill()
        self.clean()

    def kill(self):
        """
        Kill process if running
        """
        raise NotImplemented()

    def clean(self):
        """
        Remove the log file
        """
        raise NotImplemented()
