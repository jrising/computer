## Tasks

class SingleCPUTask(object):
    def __init__(self, dependencies):
        self.dependencies = dependencies

    def prepare(self, server):
        for dependency in self.dependencies:
            if not dependency.satisfied(server):
                print "Installing " + dependency.desc
                dependency.install(server)

    def fullrun(self, server, doublecheck=True):
        for dependency in self.dependencies:
            if doublecheck and not dependency.satisfied(server):
                raise NotImplementedError("Dependency not satisfied at fullrun.")

            dependency.atrun(server)

        self.selfrun(server)

    def selfrun(self, server):
        raise NotImplementedError()

class LambdaTask(SingleCPUTask):
    def __init__(self, dependencies, perform):
        super(LambdaTask, self).__init__(dependencies)
        self.perform = perform

    def selfrun(self, server):
        return self.perform(server)

unimplemented_task = SingleCPUTask([])
noop_task = LambdaTask([], lambda server: None)

## Dependencies

class OnceDependency(object):
    def __init__(self, desc):
        self.desc = desc

    def satisfied(self, server):
        return True

class LambdaDependency(OnceDependency):
    def __init__(self, desc, check, install_func=None, atrun_func=None):
        super(LambdaDependency, self).__init__(desc)
        self.check = check

        if install_func is None and atrun_func is None:
            install_func = lambda server: self.raiseunimplemented()
            atrun_func = lambda server: None
        elif install_func is None:
            install_func = lambda server: None
        elif atrun_func is None:
            atrun_func = lambda server: None

        self.install_func = install_func
        self.atrun_func = atrun_func

    def raiseunimplemented(self):
        raise NotImplementedError()

    def satisfied(self, server):
        return self.check(server)

    def install(self, server):
        self.install_func(server)

    def atrun(self, server):
        self.atrun_func(server)
