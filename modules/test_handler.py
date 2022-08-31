from ast import Return
from operator import mod


class TestHandler:
    __conn = None

    def __init__(self, connection):
        self.__conn = connection

    def run_tests(self, cfg):
        passed_cmd = 0
        failed_cmd = 0
        processed_data = []
        for cmd in cfg['commands']:
            data, result = self.test_command(cmd)
            processed_data.append(data)

            if result:
                passed_cmd += 1
            else:
                failed_cmd += 1

        self.__print_results(len(cfg['commands']), passed_cmd, failed_cmd)

        return processed_data

    def test_command(self, cmd):

        data = {}
        result = False
        try:
            modbus_result, ssh_result = self.__conn.exec(
                cmd['reg_address'], cmd['reg_amount'], cmd['ssh_command'])
            result = self.__process_return(
                modbus_result, ssh_result, cmd['reg_address'], cmd['representatio'])
            # data['commands'] = [cmd['reg_address'], cmd['reg_amount'], cmd['ssh_command']]
        except:
            # data['result'] = 'Failed'
            # result = False
            print('\033[91m' + 'Error:' + '\033[0m' + ' Incorrect command!' +
                  '\nCommand: {}'.format(str(cmd['command'])))
        return data, result

    def __process_return(self, modbus_result, ssh_result, reg_address, representation):
        modbus_result = ((modbus_result.decode("utf-8")
                          ).replace('%', '')).split('\n')
        while ('' in modbus_result):
            modbus_result.remove('')
        
        ssh_result = ssh_result[0].replace('\n', '')
        
        if reg_address == 5:
            for i in range(len(modbus_result)):
                if 'MW6' in modbus_result[i]:
                    modbus_mw = modbus_result[i].split('MW6')
                    modbus_mw = modbus_mw[-1].replace(' ', '')
                    modbus_result, ssh_result = self.__process_temp([modbus_mw, ssh_result])
                    print(modbus_result)
                    
        if reg_address:
            pass
                    
        if modbus_result == ssh_result:
            return True
        else:
            return False

    def __process_temp(self, data):
        result = []
        result.append(int(data[0])*0.1)
        result.append(int(data[1])*0.1)
        return result

    def __process_ip(self, data):
        pass

    def __process_text(self, data):
        pass

    def __process_gps(self, data):
        pass

    def __translate(self, number, hex=False):
        if hex:
            pass
        else:
            toBin = bin(number)[2:]

    def __print_results(self, to_test, passed, failed):
        print('\n\n' + 'Commands to test: ' + str(to_test))
        print('\033[92m' + 'Passed: ' + str(passed) + '\033[0m')
        print('\033[91m' + 'Failed: ' + str(failed) + '\033[0m')
