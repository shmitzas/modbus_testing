from multiprocessing.util import sub_debug
from re import sub
import subprocess
import time
import paramiko


class SSHClient:

    __ssh_client = None
    __addr = None
    __username = None
    __password = None
    __port = None
    __modbus_port = None

    def __init__(self, auth, parser):
        try:
            auth = auth['auth_params']
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
            if parser.p:
                self.__port = parser.p
            else:
                self.__modbus_port = auth['modbus_port']
        except:
            print('Authorization login credentials are invalid')
            exit()
        if not self.__open_connection():
            print('Unable to establish a connection to the server')
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
            self.__ssh_client = client
            time.sleep(1)
            return True
        except:
            return None

    def exec(self, reg_address, reg_amount, ssh_cmd):
        try:
            if reg_address < 10:
                reg_address = '00{}'.format(reg_address)
            elif reg_address > 10 and reg_address < 100:
                reg_address = '0{}'.format(reg_address)

            modbus_msg = 'modbus read -D -w -p {} {} %MW{} {}'.format(
                self.__modbus_port, self.__addr, reg_address, reg_amount)
            modbus_result = subprocess.check_output(modbus_msg, shell=True)
            stdin, stdout, stderr = self.__ssh_client.exec_command(ssh_cmd)
            ssh_res = stdout.readlines()
            return modbus_result, ssh_res

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
