import paramiko, getpass
from paramiko_server import ParamikoServer
import time


class LoginServer(ParamikoServer):
    def __init__(self, utup, cpus, roots, credentials):
        super(LoginServer, self).__init__(utup, cpus, roots, credentials)
        # self.password = getpass.getpass("Password for " + credentials['domain'] + ": ")

    def connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.credentials['domain'], username=self.credentials['username'], password=self.credentials['password'])  # password=self.password)
        # Open up a session
        s = client.get_transport().open_session()
        paramiko.agent.AgentRequestHandler(s)

        s.get_pty()
        s.invoke_shell()

        self.client = client
        self.session = s
        self.connected = True

        self.receive_all()

    def get_cpu_util(self):
        '''
        implement the idea of getting cpu_percents in psutil
        http://stackoverflow.com/questions/23367857/accurate-calculation-of-cpu-usage-given-in-percentage-in-linux
        '''
        prev_time = [x for x in self.run_command('head -' + str(self.cpus+1) + ' /proc/stat')[0].split('\n')][1:]
        time.sleep(1)
        post_time = [x for x in self.run_command('head -' + str(self.cpus+1) + ' /proc/stat')[0].split('\n')][1:]
        ret = []
        for i in range(self.cpus):
            prev_sum = sum([int(x) for x in prev_time[i].split()[1:]])
            post_sum = sum([int(x) for x in post_time[i].split()[1:]])
            prev_busy = prev_sum - int(prev_time[i].split()[4]) - int(prev_time[i].split()[5])
            post_busy = post_sum - int(post_time[i].split()[4]) - int(post_time[i].split()[5])

            ret.append((prev_time[i].split()[0], float(post_busy - prev_busy)/(post_sum - prev_sum)*100))
        return ret
