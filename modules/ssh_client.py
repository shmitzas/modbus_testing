import time
import paramiko


class Connection:

    __ssh_client = None
    __addr = None
    __username = None
    __password = None
    __port = None

    def __init__(self, auth, parser):
        try:
            if parser.ip:
                self.__addr = parser.ip
            else:
                self.__addr = auth['address']
            if parser.u:
                self.__username = parser.u
            else:
                self.__username = auth['username']
            if parser.psw:
                self.__password = parser.psw
            else:
                self.__password = auth['password']
            if parser.sp:
                self.__port = parser.sp
            else:
                self.__port = auth['port']
        except:
            print('SSH login credentials are invalid')
            exit()
        if not self.__open_connection():
            print('Unable to connect to SSH server')
            exit()

    def close_connection(self):
        if self.__ssh_client:
            self.__ssh_client.close()

    def __open_connection(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(self.__addr, self.__port,
                           self.__username, self.__password, timeout=10)
            self.__ssh_client = client.invoke_shell()
            time.sleep(1)
            self.__ssh_client.send(
                'socat /dev/tty,raw,echo=0,escape=0x03 /dev/ttyUSB3,raw,setsid,sane,echo=0,nonblock ; stty sane\r')
            time.sleep(1)
            clear = self.__ssh_client.recv(-1)
            time.sleep(1)
            return True
        except:
            return None

    def exec(self, command, result):
        acceptable_results = [
            'OK', 'ERROR', 'NO CARRIER'
        ]
        try:
            self.__ssh_client.send(str(command) + '\r')
            time.sleep(1)
            if result:
                time_limit = time.time()+180
                while time.time() < time_limit:
                    res = self.__ssh_client.recv(
                        -1).decode('utf-8').split('\n\n')
                    try:
                        msg = str(res[-1]).replace('\n', '')
                    except:
                        pass
                    if msg in acceptable_results:
                        return msg
                    time.sleep(5)
                return 'ERROR'
        except Exception as error:
            print(error)
            exit()

    def retry_connection(self):
        counter = 0
        limit = 3
        while counter < limit:
            if self.__open_connection():
                break
            counter += 1
            time.sleep(5)
        if counter < limit:
            return True
        else:
            return False

    # def get_router_data(self):
    #     data = {}
    #     self.__ssh_client.close()
    #     time.sleep(1)
    #     client = paramiko.SSHClient()
    #     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     try:
    #         client.connect(self.__addr, self.__port,
    #                        self.__username, self.__password, timeout=10)
    #         self.__ssh_client = client
    #         stdin, stdout, stderr = self.__ssh_client.exec_command(
    #             'gsmctl -w -m -y')
    #         res = (stdout.readlines())
    #         try:
    #             data['manufacturer'] = res[1].replace('\r\n', '')
    #             data['board'] = res[3].replace('\r\n', '')
    #             data['revision'] = res[5].replace('\r\n', '')
    #         except IndexError:
    #             data['manufacturer'] = res[0].replace('\r\n', '')
    #             data['board'] = res[1].replace('\r\n', '')
    #             data['revision'] = res[2].replace('\r\n', '')

    #         stdin, stdout, stderr = self.__ssh_client.exec_command(
    #             'ubus call mnfinfo get_value \'{\"key\": \"name\"}\'')
    #         res = str(stdout.readlines()[1]).split(':')

    #         data['model'] = res[1][1:8]

    #         self.__ssh_client.close()
    #         time.sleep(1)
    #         if not self.__open_connection():
    #             print('Unable to connect to SSH server')
    #             exit()

    #         return data

    #     except:
    #         print('Could not get data about the router')
    #         exit()

    def __del__(self):
        self.close_connection()
