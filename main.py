from modules.test_handler import TestHandler
from modules.connect import ConnectionHandler
from modules.cfg_handler import ConfigHandler
from modules.csv_saver import CSVHandler
import argparse

cfg = None
conn = None
tests = None
results = None

config_filename = 'config.json'


def init_modules():
    global cfg, conn, tests, csv_saver, router
    try:

        cfg = ConfigHandler(config_filename)
        parser = flags()
        router = str(parser.device).upper()
        conn = ConnectionHandler(cfg.get_param(router), parser)
        tests = TestHandler(conn)
        csv_saver = CSVHandler()

    except IndexError:
        print('No router was specified at launch!')
        exit()
    except Exception as error:
        print(error)
        exit()


def main():
    init_modules()
    print('Running tests for:', router, '\n')
    results = tests.run_tests(cfg.get_param(router))
    results.append(router)
    csv_saver.save(results)


def flags():
    parser = argparse.ArgumentParser()
    parser.add_argument('device', type=str, help='Router name')
    parser.add_argument(
        '--p', type=str, help='Assign Serial connection port (eg.: ttyUSB2)')
    parser.add_argument(
        '--br', type=int, help='Assign Serial connection baudrate (eg.: 115200)')
    parser.add_argument(
        '--ip', type=str, help='Assign SSH connection address (eg.: "192.168.1.1")')
    parser.add_argument(
        '--sp', type=str, help='Assign SSH connection port (eg.: 22)')
    parser.add_argument(
        '--u', type=str, help='Assign SSH connection username (eg.: root)')
    parser.add_argument('--psw', type=str,
                        help='Assign SSH connection password (eg.: admin)')
    return parser.parse_args()


if __name__ == '__main__':
    main()
