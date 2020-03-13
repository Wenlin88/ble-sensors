# @Author: Wenlin88
# @Date:   29-Feb-2020
# @Email:  Wenlin88@users.noreply.github.com
# @Last modified by:   Wenlin88
# @Last modified time: 13-Mar-2020

import sys
import os
import pathlib
import logger
import logging
import distutils.util

# Init logger
logger =  logger.loggerClass(name = 'Test logger', file_logging = True, logging_level = logging.DEBUG)
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
exception = logger.exception

class core(object):
    """docstring for core."""

    config_file = "pi_ble_reader.config"

    def __init__(self):
        super(core, self).__init__()
        file = pathlib.Path(self.config_file)
        if not file.exists ():
            info('Config file not found greating a new one!')
            create_config_file('pi_ble_reader.config')
        with open(self.config_file) as f:
            lines = f.readlines()
            for row, line in enumerate(lines):
                if 'run_ruuvitag_scan' in line:
                    run_tag_scan = bool(distutils.util.strtobool(line.split(' = ')[1][:-1]))
                    debug('Ruuvitag scan at start enabled: {}'.format(run_tag_scan))
                elif 'ruuvitags_enabled' in line:
                    ruuvitags_enabled = bool(distutils.util.strtobool(line.split(' = ')[1][:-1]))
                    debug('Ruuvitags enabled: {}'.format(ruuvitags_enabled))
                elif 'Known ruuvitags:' in line:
                    print(lines[row+1] == '\n')
        #     for num, line in enumerate(config_file, 1):
        #         if "##\t{:^24s}\t##\n".format('--- Ruuvitags ---') in line:
        #             print('found at line:' +  str(num))
        # with open(self.config_file) as f:
        #     if "##\t{:^24s}\t##\n".format('--- Ruuvitags ---') in f.read():
        #         print("true")



def create_config_file(file_path):
    with open("pi_ble_reader.config", "w") as f:
        f.write("##\t{:^24s}\t##\n".format('--- Ruuvitags ---'))
        f.write('ruuvitags_enabled = False\n')
        f.write('run_ruuvitag_scan = True\n')
        f.write('Known ruuvitags:\n')

        f.write("\n##\t{:^24s}\t##\n".format('--- InfluxDB ---'))
        f.write('indluxdb_enabled = False\n')
        f.write('influx_address = \n')
        f.write('influx_port = \n')
        f.write('influx_database = \n')
        f.write('influx_username = \n')
        f.write('influx_password = \n')



if __name__ == '__main__':
    core = core()
    os.getcwd()
    create_config_file("pi_ble_reader.config")
