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
        '''
        Before looking into how this class is implemented, reader should look at login_server.py to see an easier implementation.

        Logging into the OSDC server are two-stages: 
        1. Logging into griffin, the login node
        2. From griffin, do a run_command to get into the computation node. This step is presumably less reliable, 
           as it is not really handled by paramiko. But we do this regardlessly for current stage due to the fact
           that we don't really know how to implement port-forwarding and that we have less control over Shackleton.

        Since there are two stages of connecting, for the consistency of caller's behavior, this method would handle the
        connection for both stages. It will first check the hostname of the current machine, then decide what to do accordingly.

        Also, the way we forward authentication agent requires adding ssh identity to ssh-agent first. 
        Here's how we do this:
            If there's an existing agent, just find its name and use it, instead of creating a new one.
            Only create a new one when all the existing ssh-agent failed.
            "Using" a ssh-agent means setting the shell variable SSH_AUTH_SOCK to its tmp file.
        '''
        stdout = os.popen("hostname").read().strip()
        if stdout == self.credentials['instanceName']:
            self.connected = True
            return "success"
        elif stdout == "shackleton":
            retCode = 1
            try_count = 0
            try:
                while retCode != 0:
                    sshAgentList = os.popen("find /tmp/ -type s -name agent.* 2>/dev/null | grep '/tmp/ssh-.*/agent.*'").read().split("\n")[:-1]
                    for i in range(len(sshAgentList)):
                        os.environ['SSH_AUTH_SOCK'] = sshAgentList[i]
                        retCode = os.system("ssh-add " + self.credentials['pem'])
                        if retCode == 0:
                            break
                    if retCode != 0:
                        os.system("ssh-agent -s")
                    if try_count > 99:
                        raise paramiko.ssh_exception.AuthenticationException("Cannot add ssh identity!")
                    try_count += 1
            except paramiko.ssh_exception.AuthenticationException as err:
                return err

            # Following steps are similar to using paramiko to login to shackleton.
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.credentials['loginNode'], username=self.credentials['userName'])
            s = client.get_transport().open_session()
            paramiko.agent.AgentRequestHandler(s)
            s.get_pty()
            s.invoke_shell()
            self.client = client
            self.session = s
        
        # Error catching if something weird happens, the hostname should never be anything else than this 3.
        elif stdout != self.credentials['loginNode']:
            raise paramiko.ssh_exception.AuthenticationException("This should never happen!")

        # Second stage, unreliably login into computation node with run_command. 
        # If the connection from loginNode to computation is dropped, the Hostname should be the loginNode, 
        # then only this stage would be executed.
        stdout, stderr = self.run_command('ssh -A ubuntu@' + self.credentials['instanceIP'])
        stdout, stderr = self.run_command('date "+%H:%M:%S   %d/%m/%y" >> arrived')
        self.connected = True
        return "success"

    def check_connection(self):
        '''
        This method checks both the connection to login node and the computation node.
        If connection to computation node is dropped, "self.connected" might not be changed, so have to do manual checking here.
        But not worry about reconnection, that should be handle by the caller, by calling server.connect().
        '''
        if not self.connected:
            return False
        else:
            # Log the arrive time for manual checking, if this time info appears in login node,
            # then I know the connection to computation node had dropped;
            # if this info appears in shackleton, then I know that not only the connection to login node had dropped, 
            # but also the self.connected is not performing as expected.
            self.run_command('date "+%H:%M:%S   %d/%m/%y" >> arrived')

            # If hostname is the computation node, then the connection is good. All else situations the connection is dropped, should reconnect.
            stdout, stderr = self.run_command("hostname")
            if stdout == self.credentials['instanceName']:
                return True
            else:
                self.connected = False
                return False
