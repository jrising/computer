import os

class DiskServer(object):
    def __init__(self, utup, roots):
        """
        utup: unique tuple ID
        roots: dict(name => absolutepath)
        """
        self.utup = utup
        self.roots = roots

    def fullpath(self, root, path=None):
        if len(root) > 0 and root[0] == '/':
            rootpath = root
        else:
            rootpath = self.roots[root]
        if path is None:
            return rootpath

        return os.path.normpath(os.path.join(rootpath, path))

class SizelessServer(DiskServer):
    def __init__(self, utup, cpus, roots):
        """
        utup: unique tuple ID
        cpus: integer
        roots: dict(name => absolutepath)
        """
        super(SizelessServer, self).__init__(utup, roots)
        self.cpus = cpus

    def push_disk(self, root, path, localds):
        """
        root: name
        path: subdirectory
        local: local DiskServer
        """
        raise NotImplementedError()

    def pull_disk(self, root, path, localds):
        """
        root: name
        path: subdirectory
        local: local DiskServer
        """
        raise NotImplementedError()

    def list_disk(self, root, path):
        """
        root: name
        path: subdirectory
        """
        raise NotImplementedError()

    def has_file(self, root, filepath):
        """
        root: name
        path: subdirectory
        """
        basename = os.path.basename(filepath)
        for filename in self.list_disk(root, os.path.dirname(filepath)):
            if filename == basename:
                return True

        return False

    def read_file(self, root, filepath):
        "Returns string."
        raise NotImplementedError()

    def start_process(self, command, root=None, path=None):
        "Returns process."
        raise NotImplementedError()

    def run_command(self, command, root=None, path=None):
        "Returns (output, error) as strings."
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
