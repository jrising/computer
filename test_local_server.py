#### Testing LocalServer

import time
from local_server import LocalServer

def test_io():
    server = LocalServer('localhost', 1, {'': '.'})
    assert('test_local_server.py' in list(server.list_disk('', '.')))

    assert(server.has_file('', 'test_local_server.py'))

    assert(server.read_file('', 'test_local_server.py')[0:4] == '####')

def test_proc():
    server = LocalServer('localhost', 1, {'': '.'})

    lines = server.run_command('',  '.', 'ls -1')
    assert('test_local_server.py' in lines.split('\n'))

    proc = server.start_process('', '.', 'ls -1', 'log.txt')
    while proc.is_running():
        time.sleep(.1)

    lines = server.read_file('', 'log.txt')
    assert('test_local_server.py' in lines.split('\n'))
    proc.close()
