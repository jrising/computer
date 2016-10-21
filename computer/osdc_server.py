import paramiko, os, time
from paramiko_server import ParamikoServer
from process import SingleCPUProcess


class OSDCProcess(SingleCPUProcess):
    def __init__(self, pid, logfile):
        super(OSDCProcess, self).__init__(logfile)
        self.pid = pid

    def is_running(self):
        raise NotImplementedError("Not implemented yet.")

    def kill(self):
        raise NotImplementedError("Not implemented yet.")

    def clean(self):
        raise NotImplementedError("Not implemented yet.")


class OSDCServer(ParamikoServer):
    def __init__(self, utup, cpus, roots, credentials):
        super(OSDCServer, self).__init__(utup, cpus, roots, credentials)

    def connect(self):
        # Logging into the OSDC server requires adding ssh identity to ssh-agent first.
        # If there's an existing agent, just find its name and use it, instead of creating a new one.
        # Only create a new one when all the existing ssh-agent failed.
        # "Using" a ssh-agent means setting the shell variable SSH_AUTH_SOCK to its tmp file.
        retCode = 1
        try_count = 0
        while retCode != 0:
            sshAgentList = os.popen("find /tmp/ -type s -name agent.* 2>/dev/null | grep '/tmp/ssh-.*/agent.*'").read().split("\n")[:-1]
            for i in len(sshAgentList):
                os.environ['SSH_AUTH_SOCK'] = sshAgentList[i]
                retCode = os.system("ssh-add /var/www/jongkaishackleton-www.pem")
                if retCode == 0:
                    break
            if retCode != 0:
                os.system("ssh-agent -s")
            if try_count > 99:
                raise SystemExit("Cannot add ssh identity!")
            try_count += 1

        # Other setups are similar to using paramiko to login to shackleton.
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.credentials['loginnode'], username=self.credentials['username'])
        s = client.get_transport().open_session()
        paramiko.agent.AgentRequestHandler(s)
        s.get_pty()
        s.invoke_shell()
        self.client = client
        self.session = s

        # Except for having to manually login into computation node.
        stdout, stderr = self.run_command('ssh -A ubuntu@' + self.credentials['instanceip'])
        stdout, stderr = self.run_command('date "+%H:%M:%S   %d/%m/%y" >> arrived')

        self.connected = True

    def check_connection(self):
        # This method checks both the connection to login node and the computation node.
        # If connection to computation node is dropped, retry.
        # But not worry about reconnection to login node, which would be handle by the caller.
        # This design is for the consistency of caller's behavior.
        if not self.connected:
            return False
        while True:
            # Log the arrive time for manual checking, if this time info appears in login node,
            # then I know the connection to computation node had dropped;
            # if this info appears in shackleton, then I know that not only the connection to login node had dropped, 
            # but also the self.connected is not performing as expected.
            self.run_command('date "+%H:%M:%S   %d/%m/%y" >> arrived')

            # If hostname is shackleton, then the connection to login node is dropped, should reconnect.
            stdout, stderr = self.run_command("hostname")
            if stdout == "shackleton":
                return False
            elif stdout == "conflicts":
                return True
            else:
                self.run_command('ssh -A ubuntu@' + self.credentials['instanceip'])
                time.sleep(0.2)
