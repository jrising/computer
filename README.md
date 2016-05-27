## Paths

Servers have collections of `roots`, used to abstract away the
location of files.  Most methods take a `path` argument, which can
take three forms:
* Starting with a `/`: An absolute path, not relative to `root`.
* Containing a `/`: The `root` is up to the first slash, and the remaining is a subpath.
* Not containing a `/`: Just a `root` directory.
