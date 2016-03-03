class SingleCPUProcess(object):
    def __init__(self, logfile):
        self.logfile = logfile
        
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

class RemoteProcess(SingleCPUProcess):
    def __init__(self, server, pid, logfile):
        super(RemoteProcess, self).__init__(logfile)
        self.server = server
        self.pid = pid

