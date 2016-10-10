import paramiko, os
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
        os.system("ssh-agent -s")
        sshAgentList = os.popen("find /tmp/ -type s -name agent.* 2>/dev/null | grep '/tmp/ssh-.*/agent.*'").read().split("\n")[:-1]
        retCode = 1
        while retCode != 0:
            os.environ['SSH_AUTH_SOCK'] = sshAgentList[0]
            retCode = os.system("ssh-add /home/jongkai/.ssh/jongkaishackleton.pem")

        #     os.system("ssh-agent -s")
        #     sshAgentList = os.popen("find /tmp/ -type s -name agent.* 2>/dev/null | grep '/tmp/ssh-.*/agent.*'").read().split("\n")[:-1]
        #     os.environ['SSH_AUTH_SOCK'] = sshAgentList[0]
        #     retCode = os.system("ssh-add /home/jongkai/.ssh/jongkaishackleton.pem")

                

        # while True:
        #     os.system("ssh-agent -s")
        #     sshAgentList = os.popen("find /tmp/ -type s -name agent.* 2>/dev/null | grep '/tmp/ssh-.*/agent.*'").read().split("\n")[:-1]
        #     os.environ['SSH_AUTH_SOCK'] = sshAgentList[0]
        #     retCode = os.system("ssh-add /home/jongkai/.ssh/jongkaishackleton.pem")
        #     if retCode == 0:
        #         for i in range(1, len(sshAgentList)):
        #             agentPID = int(sshAgentList[i].split(".")[1])+1
        #             os.system("kill " + str(agentPID))
        #         break
        #     else:
        #         agentPID = int(sshAgentList[0].split(".")[1])+1
        #         # TODO: add sleep
        #         os.system("kill " + str(agentPID))

        # client = paramiko.SSHClient()
        # #proxy = paramiko.ProxyCommand('ssh -A ubuntu@' + self.credentials['instanceip'])
        # proxy = paramiko.ProxyCommand("ssh -o StrictHostKeyChecking=no griffin.opensciencedatacloud.org nc 172.17.199.2 22")
        # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # print('yo')
        # client.connect(self.credentials['loginnode'], username=self.credentials['username'], sock=proxy)
        # paramiko.util.log_to_file("filename.log")
        # print("haa")
        # s = client.get_transport().open_session()
        # paramiko.agent.AgentRequestHandler(s)
        # s.get_pty()
        # s.invoke_shell()


        # client = paramiko.SSHClient()
        # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # client.connect(self.credentials['loginnode'], username=self.credentials['username'])
        # s = client.get_transport().open_session()
        # paramiko.agent.AgentRequestHandler(s)
        # s.get_pty()
        # s.invoke_shell()
        # proxy = paramiko.ProxyCommand("ssh -o ForwardAgent griffin.opensciencedatacloud.org nc 172.17.199.2 22")
        # client2 = paramiko.SSHClient()
        # client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # print('yo')
        # client2.connect(self.credentials['loginnode'], username=self.credentials['username'], sock=proxy)
        # print("haa")
        # s2 = client.get_transport().open_session()
        # paramiko.agent.AgentRequestHandler(s)
        # s2.get_pty()
        # s2.invoke_shell()
        # pring("GO")
        # self.client = client2
        # self.session = s2
        # self.connected = True

        # stdout, stderr = self.run_command('date "+%H:%M:%S   %d/%m/%y" >> arrived')
        
        # self.receive_all()

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh -A jrising@griffin.opensciencedatacloud.org
        client.connect(self.credentials['loginnode'], username=self.credentials['username'])

        # Open up a session
        s = client.get_transport().open_session()
        paramiko.agent.AgentRequestHandler(s)

        s.get_pty()
        s.invoke_shell()

        self.client = client
        self.session = s

        # ssh -A ubuntu@172.17.199.2
        print(s)
        stdout, stderr = self.run_command('ssh -A ubuntu@' + self.credentials['instanceip'])
        print(self, s)
        stdout, stderr = self.run_command('date "+%H:%M:%S   %d/%m/%y" >> arrived')

        self.connected = True

        # while True:
        #     stdout, stderr = self.run_command("hostname")
        #     if stdout != "Griffin":
        #         self.run_command('ssh -A ubuntu@' + self.credentials['instanceip'])
        #     else:
        #         stdout, stderr = self.run_command('date "+%H:%M:%S   %d/%m/%y" >> arrived')
        #         return True


    def check_connection(self):
        if not self.connected:
            return False
        while True:
            stdout, stderr = self.run_command("hostname")
            if stdout != "Griffin":
                self.run_command('ssh -A ubuntu@' + self.credentials['instanceip'])
                time.sleep(0.2)
            else:
                return True
