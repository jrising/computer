import paramiko
from login_server import LoginServer

class SlurmServer(LoginServer):
    def __init__(self, utup, cpus, roots, credentials):
        super(SlurmServer, self).__init__(utup, cpus, roots, credentials)

    def connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.credentials['domain'], username=self.credentials['userName'], password=self.credentials['password'])

        # Open up a session
        s = client.get_transport().open_session()

        s.get_pty()
        s.invoke_shell()

        self.client = client
        self.session = s
        self.connected = True

        self.receive_all()

    def active_processes(self, procname):
        # Ignores procname
        return int(self.run_command("squeue | grep $USER | wc -l")[0])

if __name__ == '__main__':
    import sys, logging
    from interact.main import handle

    ch = logging.StreamHandler(sys.stdout)
    logging.getLogger("paramiko").addHandler(ch)

    credentials = dict(domain=sys.argv[1], userName=sys.argv[2], password=sys.argv[3])
    server = SlurmServer((), 1, {}, credentials)
    server.connect()
    handle(server, sys.argv[4:])
