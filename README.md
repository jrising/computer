
## Paths

Servers have collections of `roots`, used to abstract away the
location of files.  Most methods take a `path` argument, which can
take three forms:
* Starting with a `/`: An absolute path, not relative to `root`.
* Containing a `/`: The `root` is up to the first slash, and the remaining is a subpath.
* Not containing a `/`: Just a `root` directory.

## Available Servers

### Abstract Servers

* `DiskServer`: A server with a unique ID and a collection of named file root directories.
* `SizelessServer` (`DiskServer`): The main top-level server class, able to transfer data and run commands.  Does not monitor or limit data usage (hence, "sizeless").
* `SizelessConnectableServer` (`SizelessServer`): A server that has a protocol for connecting to it.
* `SizelessLinuxServer` (`SizelessConnectableServer`): A standard Linux server, with everything except `run_command` implemented.
* `ParamikoServer` (`SizelessLinuxServer`): A server connected through ssh, using the Paramiko interface.  The `self.session` variable needs to be set in the `connect` method before these functions will work.

### Concrete Servers

* `LocalServer` (`SizelessServer`): A server representing the local machine, using python commands.
* `LoginServer` (`ParamikoServer`): A server using a Paramiko ssh connection, with a normal password login.


[More Documentation can be found here](http://cli-computer.readthedocs.io/en/latest/index.html)
