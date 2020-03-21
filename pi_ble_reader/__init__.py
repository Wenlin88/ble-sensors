# @Author: Wenlin88
# @Date:   29-Feb-2020
# @Email:  Wenlin88@users.noreply.github.com
# @Last modified by:   Henri Wenlin
# @Last modified time: 2020-03-21T15:14:07+02:00

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
            if 'find_ruuvitags_at_start' in line:
                find_ruuvitags_at_start = bool(distutils.util.strtobool(line.split(' = ')[1][:-1]))
                info('Find ruuvitags at first start enabled: {}'.format(find_ruuvitags_at_start))
            elif 'ruuvitags_enabled' in line:
                ruuvitags_enabled = bool(distutils.util.strtobool(line.split(' = ')[1][:-1]))
                info('Ruuvitags enabled: {}'.format(ruuvitags_enabled))
            elif 'ruuvitag_scan_interval' in line:
                ruuvitag_scan_interval = int(line.split(' = ')[1][:-1])
                info('Ruuvitag scan interval in minutes: {}'.format(ruuvitag_scan_interval))
            elif 'Known ruuvitags:' in line:
                i = 1
                info('Known ruuvitags: ')
                while not lines[row+i] == '\n':
                    info(lines[row+i][:-1])
                    i += 1
                info(str(i-1) + ' known ruuvitags in total')
            elif 'indluxdb_enabled' in line:
                indluxdb_enabled = bool(distutils.util.strtobool(line.split(' = ')[1][:-1]))
                info('IndluxDB enabled: {}'.format(indluxdb_enabled))
            elif 'influx_address' in line:
                influx_address = line.split(' = ')[1][:-1]
                info('IndluxDB server ip adress: {}'.format(influx_address))
            elif 'influx_port' in line:
                influx_port = line.split(' = ')[1][:-1]
                info('IndluxDB port: {}'.format(influx_port))
            elif 'influx_database' in line:
                influx_database = line.split(' = ')[1][:-1]
                info('IndluxDB database: {}'.format(influx_database))
            elif 'influx_username' in line:
                influx_username = line.split(' = ')[1][:-1]
                info('IndluxDB username: {}'.format(influx_username))
            elif 'influx_password' in line:
                influx_password = line.split(' = ')[1][:-1]
                info('IndluxDB password: {}'.format(influx_password))

    reader_setup = dict()
    reader_setup['find_ruuvitags_at_start'] = find_ruuvitags_at_start
    reader_setup['ruuvitags_enabled']       = ruuvitags_enabled
    reader_setup['influx_address']          = influx_address
    reader_setup['influx_port']             = influx_port
    reader_setup['influx_database']         = influx_database
    reader_setup['influx_username']         = influx_username
    reader_setup['influx_password']         = influx_password
    return reader_setup
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
