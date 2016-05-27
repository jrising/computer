#### Testing LocalServer

import time, os
from computer.local_server import LocalServer

def test_io():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    server = LocalServer('localhost', 1, {'cc': '..'})
    assert('test/test_local_server.py' in list(server.list_disk('cc')))

    assert(server.has_file('cc/test/test_local_server.py'))

    assert(server.read_file('cc/test/test_local_server.py')[0:4] == '####')

def test_proc():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    server = LocalServer('localhost', 1, {'cc': '..'})

    lines = server.run_command('ls -1', 'cc')
    assert('local_server.py' in lines.split('\n'))

    proc = server.start_process('ls -1', 'cc/log.txt', 'cc')
    while proc.is_running():
        time.sleep(.1)

    lines = server.read_file('cc/log.txt')
    assert('local_server.py' in lines.split('\n'))
    proc.close()
