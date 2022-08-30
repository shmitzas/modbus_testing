import datetime
import os
from posixpath import dirname


class CSVHandler:
    __date = datetime.datetime.now()

    def __init__(self):
        pass

    def save(self, data):
        header = 'Command, Expected, Returned, Result'
        router_data = data[0]
        try:
            router_name = str(data[-1])
            dir_name = './results/'
            if os.path.exists(dir_name):
                pass
            else:
                os.mkdir(dir_name)
                os.chmod(dir_name, 0o777)
            filename = dir_name + router_name + '_' + str(self.__date.year) + '-' + str(self.__date.month) + '-' + str(
                self.__date.day) + '-' + str(self.__date.hour) + '-' + str(self.__date.minute) + '_test.csv'

            with open(filename, 'w') as f:
                f.write(self.router_formatter(router_data))
                f.write(header+'\n')
                for item in data[1:-1]:
                    f.write(self.formatter(item)+'\n')
            f.close()
        except:
            print('Could not save results to a file')
            exit()

    def formatter(self, test):
        return str(test['command']).replace('"', '') + ',' + str(test['expected']) + ',' + str(test['returned']) + ',' + str(test['result'])

    def router_formatter(self, test):
        if test['model']:
            return 'Model: ' + str(test['model']).replace('"', '') + ',Manufacturer: ' + str(test['manufacturer']) + ',Board: ' + str(test['board']) + ',Revision: ' + str(test['revision']+'\n')
        else:
            return 'Manufacturer: ' + str(test['manufacturer']) + ',Board: ' + str(test['board']) + ',Revision: ' + str(test['revision']+'\n')
