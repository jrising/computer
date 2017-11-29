import os

class DiskServer(object):
    def __init__(self, utup, roots):
        """
        utup: unique tuple ID
        roots: dict(name => absolutepath)
        """
        self.utup = utup
        self.roots = roots
        self.baseroot = os.getcwd()

    def splitpath(self, path):
        if path is None:
            return None, None

        if len(path) > 0 and path[0] == '/':
            return None, path
        if '/' not in path:
            return path, None

        return path[:path.index('/')], path[path.index('/')+1:]

    def fullpath(self, path):
        if path is None:
            return None

        root, path = self.splitpath(path)
        if root is None:
            return path
        if path is None:
            return os.path.join(self.baseroot, self.roots[root])

        return os.path.normpath(os.path.join(self.baseroot, self.roots[root], path))

class SizelessServer(DiskServer):
    def __init__(self, utup, cpus, roots):
        """
        utup: unique tuple ID
        cpus: integer
        roots: dict(name => absolutepath)
        """
        super(SizelessServer, self).__init__(utup, roots)
        self.cpus = cpus

    def push_disk(self, path, localds):
        """
        path: subdirectory
        local: local DiskServer
        """
        raise NotImplementedError()

    def pull_disk(self, path, localds):
        """
        path: subdirectory
        local: local DiskServer
        """
        raise NotImplementedError()

    def list_disk(self, path):
        """
        path: subdirectory
        """
        raise NotImplementedError()

    def has_file(self, filepath):
        """
        path: subdirectory
        """
        basename = os.path.basename(filepath)
        for filename in self.list_disk(os.path.dirname(filepath)):
            if filename == basename:
                return True

        return False

    def read_file(self, filepath):
        "Returns string."
        raise NotImplementedError()

    def start_process(self, command, path=None):
        "Returns process."
        raise NotImplementedError()

    def run_command(self, command, path=None):
        "Returns (output, error) as strings."
        raise NotImplementedError()

    def cwd(self, path):
        "Changes current directory on server."
        raise NotImplementedError()

class SizelessConnectableServer(SizelessServer):
    def __init__(self, utup, cpus, roots, credentials):
        super(SizelessConnectableServer, self).__init__(utup, cpus, roots)
        self.connected = False
        self.credentials = credentials

    def check_connection(self):
        raise NotImplementedError()

    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()
