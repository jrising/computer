class DiskDependency(object):
    def __init__(self, root, path, size):
        self.root = root
        self.path = path
        self.size = size

    def satisfy_cost(self, server):
        if server.has_file(self.root, self.path):
            return 0
        return self.size

    def satisfy(self, server):
        if self.satisfy_cost(server) > 0:
            server.push_disk(self.root, self.path)

class Manager(object):
    def __init__(self):
        self.priorities = {} # { server: priority }
        self.processes = {} # { server: set(process) }
        self.callbacks = {} # { process: callback }
        self.waiting = Queue() # Q[(root, path, command, dependencies, callback)]

    def add_server(self, server, priority):
        self.priorities[server] = priority
        self.processes[server] = []

    def submit(self, root, path, command, dependencies, callback):
        """
        Does not return process (so we can manage).
        callback only called on check().
        """
        server = prepare_server(dependencies)
        if server is None:
            self.waiting.put((root, path, command, dependencies, callback))
            return
        
        process = server.start_process(root, path, command)
        self.processes[server].add(process)
        self.callbacks[process] = callback
        
    def process_check(self):
        for server, processes in self.server_check()
            for process in processes:
                if not process.is_running():
                    self.callbacks[process](server, process.logfile)
                    process.close()

    def server_check(self):
        for server in self.processes:
            processes = self.processes[server]
            if len(processes) == 0:
                continue

            yield server, processes
                    
    def prepare_server(self, dependencies, required=False):
        """
        Finds a server with resources and minimal transfer requirements;
        transfers additional requirements as needed.
        Returns server.
        """
        server = select_server(dependencies, required)
        if server is None:
            return None
        
        for dependency in dependencies:
            dependency.satisfy(server)

        return server

    def select_server(self, dependencies, required):
        options = {}
        for server in self.priorities:
            priority = self.priorities[server]
            processes = self.servers[server]
            if len(processes) < server.cpus or required:
                cost = 1000 # Need for CPU penalization
                for dependency in dependencies:
                    cost += dependency.satisfy_cost(server)

                # Penalize by the number of active processes
                cost *= 1 + float(len(processes)) / server.cpus

            options[server] = cost

        if len(options) == 0:
            return
        
        return sorted(options, key=newgrades.__getitem__)[0]

    def run_command(self, root, path, command, dependencies):
        server = prepare_server(dependencies, required=True)
        return server.run_command(root, path, command)
        
