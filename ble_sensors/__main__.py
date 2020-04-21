import sys
import argparse
import pkg_resources  # part of setuptools
from ble_sensors import ble_sensor_config, wenlins_logger, ruuvitag
import importlib
import configparser

config_file = "ble-sensors.config"

# Init logger
logger =  wenlins_logger.loggerClass(name = 'main', file_logging = False, logging_level = 'debug')
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
exception = logger.exception


def get_parser():
    """
    Creates a new argument parser.
    """
    version = pkg_resources.require("ble_sensors")[0].version
    formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=60,width = 115)
    parser = argparse.ArgumentParser('ble_sensors',description='Python module to read all sorts of BLE sensors with Raspberry Pi', formatter_class=formatter)
    version = '%(prog)s ' + version
    parser.add_argument('-v', '--version', action='version', version=version, help='get ble-sensors module version')
    parser.add_argument('-f', '--find_tags', dest = 'find_action', help='Find broadcasting RuuviTags', action = 'store_true')
    return parser
def find_ruuvitags(config):
    number_of_known_ruuvitags = int(config['Ruuvitag general']['known ruuvitags'])
    info('Already know RuuviTags found from config: ' + str(number_of_known_ruuvitags))
    try:
        listening_time = int(input('\n\nGive the desired listening time in seconds: '))
    except ValueError:
        error('Give number value!')
        return False
    print('\n')
    info('Listening ruuvitag broadcasts for '+ str(listening_time) + 's...')
    data = ruuvitag.get_data(timeout = listening_time)

    nro_new_tags = len(data) - number_of_known_ruuvitags
    info('Data recieved from ' + str(len(data)) + ' ruuvitag(s)!')

    tag_list = ble_sensor_config.read_known_ruuvitags()
    known_macs = [tag_list[tag]['mac'] for tag in tag_list]

    new_macs = list()
    if len(data) > 0:
        temp_macs = data.keys()
        for mac in temp_macs:
            if not mac in known_macs:
                new_macs.append(mac)

    info(str(len(new_macs)) + ' new ruuvitags found!')

    if len(new_macs) > 0:
        ans = input("Add new tags to config? (y/n): ")
        if ans == 'y':
            ble_sensor_config.add_new_ruuvitag_to_config_file(new_macs)
def main(args = None):
    print('\n----------------------------------------------- ')
    print('-------- Welcome to ble_sensors CLI UI -------- ')
    print('----------------------------------------------- \n')

    # Check that config file exists
    # ble_sensor_config.create_config_file()
    config = ble_sensor_config.get_config()

    parser = get_parser()
    args = parser.parse_args(args)

    if args.find_action:
        find_ruuvitags(config)
    else:
        parser.print_usage()
if __name__ == '__main__':
    main()
