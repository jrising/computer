import os

class SizelessServer(object):
    def __init__(self, cpus, roots):
        """
        cpus: integer
        roots: dict(name => absolutepath)
        """
        self.cpus = cpus
        self.roots = roots

    def fullpath(self, root, path):
        return os.path.normpath(os.path.join(self.roots[root], path))
        
    def push_disk(self, root, path):
        """
        root: name
        path: subdirectory
        """
        raise NotImplemented()

    def pull_disk(self, root, path):
        """
        root: name
        path: subdirectory
        """
        raise NotImplemented()

    def list_disk(self, root, path):
        """
        root: name
        path: subdirectory
        """
        raise NotImplemented()

    def has_file(self, root, filepath):
        """
        root: name
        path: subdirectory
        """
        raise NotImplemented()        

    def read_file(self, root, filepath):
        "Returns string."
        raise NotImplemented()

    def start_process(self, root, path, command):
        "Returns process."
        raise NotImplemented()

    def run_command(self, root, path, command):
        "Returns output."
        raise NotImplemented()
