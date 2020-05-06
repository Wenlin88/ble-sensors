#/usr/bin/python3
import sys
import argparse
import pkg_resources  # part of setuptools
from ble_sensors import ble_sensor_config, wenlins_logger, ruuvitag, influxDB
import importlib
import configparser
import subprocess
from crontab import CronTab
import os


config_file = os.path.expanduser('~/ble-sensors.config')

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
    Creates a argument parser.
    """
    version = pkg_resources.require("ble_sensors")[0].version
    formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=62,width = 115)
    parser = argparse.ArgumentParser('ble_sensors',description='Python module to read all sorts of BLE sensors with Raspberry Pi', formatter_class=formatter)
    version = '%(prog)s ' + version
    parser.add_argument('-v', '--version', action='version', version=version, help='get ble-sensors module version')
    parser.add_argument('-f', '--find_tags', dest = 'find_action', help='Find broadcasting RuuviTags', action = 'store_true')
    parser.add_argument('-r', '--run_tag_scan', dest = 'scan_time', help='Scan data from known RuuviTags.', nargs='?', const=2, type=int)
    parser.add_argument('-e', '--edit_config', dest = 'config_edit_action', help='Edit config file with Nano editor', action = 'store_true')
    parser.add_argument('-a', '--add_to_crontab', dest = 'add_to_crontab', help='Add ble-sensor scanning to crontab process', action = 'store_true')
    parser.add_argument('-d', '--delete_from_crontab', dest = 'remove_from_crontab', help='Delete ble-sensor scanning from crontab', action = 'store_true')
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
def read_data_from_ruuvitags(timeout = 2, influxDB_client = None):
    tag_list = ble_sensor_config.read_known_ruuvitags()
    known_macs = [tag_list[tag]['mac'] for tag in tag_list]
    raw_data = ruuvitag.get_data(timeout = timeout, ruuvitags = known_macs)
    if len(raw_data) > 0:
        for mac in raw_data:
            tag = [tag for tag in tag_list if tag_list[tag]['mac'] == mac]
            data = [mac]
            data.append(raw_data[mac])
            if tag:
                data.append(tag[0][:])
            else:
                warning('Unknown tag: {}'.format(mac))
                data.append(None)

            info('{}: {:4.1f}C° {:3.1f}RH% {:5.1f}hPa {:4.3f}V'.format(data[-1],data[1]['temperature'],data[1]['humidity'],data[1]['pressure'],data[1]['battery']/1000))
            if not influxDB_client == None:
                influxDB.write_ruuvidata_to_influxdb(influxDB_client,data)
    else:
        warning('No data resieved from ruuvitags!')
def main(args = None):
    print('\n--------------------------------------------- ')
    print('--------  ble_sensors version: {:} -------- '.format(pkg_resources.require("ble_sensors")[0].version))
    print('--------------------------------------------- \n')

    # Check that config file exists
    # ble_sensor_config.create_config_file()
    config = ble_sensor_config.get_config()

    if config['InfluxDB'].getboolean('enabled') == True:
        info('InfluxDB enabled!')
        host = config['InfluxDB']['address']
        port = int(config['InfluxDB']['port'])
        database = config['InfluxDB']['database']
        username = config['InfluxDB']['username']
        password = config['InfluxDB']['password']
        influxDB_client = influxDB.connect_to_server(host, port, username, password)
        influxDB_client = influxDB.connect_to_database(influxDB_client, database)

    else:
        info('InfluxDB not configured!')
        influxDB_client = None


    parser = get_parser()
    args = parser.parse_args(args)
    if args.find_action:
        find_ruuvitags(config)
    elif not args.scan_time == None:
        read_data_from_ruuvitags(timeout = args.scan_time,  influxDB_client = influxDB_client)
    elif args.config_edit_action:
        subprocess.call(['nano', config_file])
    elif args.add_to_crontab:
            info('Writing ble-sensor scanning job to crontab')
            cron = CronTab(user='pi')
            iter = cron.find_comment('Scanning job for ble-sensors')
            jobs = [i for i in iter]
            if len(jobs) > 0:
                warning('ble-sensor scanning job already found from crontab')
            else:
                job = cron.new(command='/usr/bin/python3 -m ble_sensors -r 10', comment='Scanning job for ble-sensors')
                job.minute.every(1)
                cron.write()
                info('Job written successfully to crontab!')
    elif args.remove_from_crontab:
        info('Trying to delete ble-sensor scanning job from crontab')
        cron = CronTab(user='pi')
        iter = cron.find_comment('Scanning job for ble-sensors')
        jobs = [i for i in iter]
        if len(jobs) > 0:
            for job in jobs:
                temp = job.comment
                cron.remove(job)
                cron.write()
                info('{} removed from crontab'.format(temp))
        else:
            warning('ble-sensor scanning job not found from crontab!')
    else:
        parser.print_usage()
    print('\n---------------------------------------------\n')
if __name__ == '__main__':
    main()
    # cron = CronTab(user='pi')
    # for job in cron:
    #     print(job)
