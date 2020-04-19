import os
import pathlib
import logging
from ble_sensors import wenlins_logger
import configparser

config_file = "ble-sensors.config"

# Init logger
logger =  wenlins_logger.loggerClass(name = 'ble-sensors config', file_logging = False, logging_level = 'debug')
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
exception = logger.exception

def create_config_file():
    # lets create that config file for next time...
    debug('making a new config file!')
    config = configparser.ConfigParser()
    cfgfile = open(config_file,'w')

    # add the settings to the structure of the file, and lets write it out...
    config.add_section('Ruuvitags')
    config.set('Ruuvitags','Ruuvitag reading enabled','True')
    config.set('Ruuvitags','Ruuvitag scan interval','1')
    config.set('Ruuvitags','Search new ruuvitags','True')

    config.add_section('InfluxDB')
    config.set('InfluxDB','InfluxDB enabled','True')
    config.set('InfluxDB','InfluxDB address','127.0.0.1')
    config.set('InfluxDB','InfluxDB port','8086')
    config.set('InfluxDB','InfluxDB database','')
    config.set('InfluxDB','InfluxDB username','')
    config.set('InfluxDB','InfluxDB password','')
    config.write(cfgfile)
    cfgfile.close()
    debug('config file done!!')
    return os.path.realpath(cfgfile.name)
def read_config_file():
    config = configparser.ConfigParser()
    config.read(config_file)
    return config
def get_config():
    file = pathlib.Path(config_file)
    if not file.exists ():
        warning('Config file not found! A new one is created automatically!')
        filepath = create_config_file()
    info('Reading config file...')
    config = read_config_file()
    info('Config file read!')
    return config

if __name__ == '__main__':
    create_config_file()
