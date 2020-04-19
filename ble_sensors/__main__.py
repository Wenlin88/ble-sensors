import sys
import argparse
from ble_sensors import config, wenlins_logger
import importlib

# Init logger
logger =  wenlins_logger.loggerClass(name = 'main', file_logging = False, logging_level = 'debug')
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
exception = logger.exception

print('Moi!')

def get_parser():
    """
    Creates a new argument parser.
    """
    version = ble_sensors.__version__
    formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=60,width = 115)
    parser = argparse.ArgumentParser('ble_sensors',description='Python module to read all sorts of BLE sensors with Raspberry Pi', formatter_class=formatter)
    version = '%(prog)s ' + version
    parser.add_argument('--version', action='Get ble_sensors version', version='%(prog)s {}'.format(ble_sensors.__version__))
    parser.add_argument('-l', '--listen_tags', dest = 'listen_action', help='Find broadcasting RuuviTags', action='store_true')
    return parser

def main(args = None):
    info('----------------------------------------------- ')
    info('-------- Welcome to ble_sensors CLI UI -------- ')
    info('----------------------------------------------- ')

    # Check that config file exists
    config.get_config()

    parser = get_parser()
    args = parser.parse_args(args)

    if args.listen_action:
        sensor = RuuviTag(args.mac_address, args.bt_device)
        state = sensor.update()
        log.info(state)
    else:
        parser.print_usage()


    info('--------------------------------')
    info('-------- End of program --------')
    info('--------------------------------')
    # if not d['add'] == None:
    #     print('Löytyy!')
    # elif not d['account_name'] == None:
    #     general.write_account_name_to_config_file(d['account_name'][0])
    # elif not d['calendar_name'] == None:
    #     general.write_calendar_name_to_config_file(d['calendar_name'][0])
    #
    #
if __name__ == '__main__':
    main()
