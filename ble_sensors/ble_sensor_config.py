import os
import pathlib
import logging
from ble_sensors import wenlins_logger
import configparser

config_file = os.path.expanduser('~/ble-sensors.config')

# Init logger
logger =  wenlins_logger.loggerClass(name = 'config', file_logging = False, logging_level = 'debug')
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
    config.add_section('Ruuvitag general')
    config.set('Ruuvitag general','Ruuvitag reading enabled','True')
    config.set('Ruuvitag general','Ruuvitag scan interval [min]','1')
    config.set('Ruuvitag general','Known ruuvitags','0')


    config.add_section('InfluxDB')
    config.set('InfluxDB','enabled','False')
    config.set('InfluxDB','address','127.0.0.1')
    config.set('InfluxDB','port','8086')
    config.set('InfluxDB','database','')
    config.set('InfluxDB','username','')
    config.set('InfluxDB','password','')
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
def add_new_ruuvitag_to_config_file(new_tag_list):
    config = configparser.ConfigParser()
    config.read(config_file)
    number_of_known_ruuvitags = int(config['Ruuvitag general']['known ruuvitags'])

    for i, tag in enumerate(new_tag_list):
        number_of_known_ruuvitags
        tag_string = 'Ruuvitag ' + str(i+1+number_of_known_ruuvitags)
        config.add_section(tag_string)
        config.set(tag_string,'mac',tag)
        config.set(tag_string,'name',tag_string)
        config.set(tag_string,'temperature calibration value','0.0')
        config.set(tag_string,'humidity calibration value','0.0')
        config.set(tag_string,'pressure calibration value','0.0')
    config.set('Ruuvitag general','known ruuvitags',str(len(new_tag_list)+number_of_known_ruuvitags))
    with open(config_file, 'w') as configfile:
        config.write(configfile)
def read_known_ruuvitags():
    config = configparser.ConfigParser()
    config.read(config_file)
    number_of_known_ruuvitags = int(config['Ruuvitag general']['known ruuvitags'])

    tags = dict()
    for i in range(number_of_known_ruuvitags):
        tag_string = 'Ruuvitag ' + str(i+1)
        tags.update({tag_string:
        {'mac': config[tag_string]['mac'],
        'name': config[tag_string]['name'],
        'T_cal_value': config[tag_string]['temperature calibration value'],
        'RH_cal_value': config[tag_string]['humidity calibration value'],
        'P_cal_calue': config[tag_string]['pressure calibration value']}})
    return tags
if __name__ == '__main__':
    create_config_file()
