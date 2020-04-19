# @Author: Wenlin88
# @Date:   29-Feb-2020
# @Email:  Wenlin88@users.noreply.github.com
# @Last modified by:   Henri Wenlin
# @Last modified time: 2020-03-21T15:18:14+02:00

import sys
import os
import pathlib
import logger
import logging
import distutils.util

# Init logger
logger =  logger.loggerClass(name = 'Reader init', file_logging = True, logging_level = logging.DEBUG)
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
exception = logger.exception

config_file = "pi_ble_reader.config"

def read_config_file():
    file = pathlib.Path(config_file)
    if not file.exists ():
        info('Config file not found greating a new one!')
        create_config_file('pi_ble_reader.config')
    with open(config_file) as f:
        lines = f.readlines()
        for row, line in enumerate(lines):
            if 'Account name' in line:
                account_name = line.split(' = ')[1][:-1])
                debug('Used account name is: {}'.format(account_name))


    config = dict()
    config['account_name'] = account_name

def create_config_file():
    with open("pi_ble_reader.config", "w") as f:
        f.write("##\t{:^24s}\t##\n".format('--- Ruuvitags ---'))
        f.write('ruuvitags_enabled = True\n')
        f.write('ruuvitag_scan_interval = 1\n')
        f.write('find_ruuvitags_at_start = True\n')
        f.write('Known ruuvitags:\n')

        f.write("\n##\t{:^24s}\t##\n".format('--- InfluxDB ---'))
        f.write('indluxdb_enabled = False\n')
        f.write('influx_address = 127.0.0.1\n')
        f.write('influx_port = 8086\n')
        f.write('influx_database = \n')
        f.write('influx_username = \n')
        f.write('influx_password = \n')


if __name__ == '__main__':
    create_config_file()
    cread_config_file()
