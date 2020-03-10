# @Author: Wenlin88
# @Date:   29-Feb-2020
# @Email:  Wenlin88@users.noreply.github.com
# @Last modified by:   Wenlin88
# @Last modified time: 10-Mar-2020

import sys
import os
import pathlib

class core(object):
    """docstring for core."""

    def __init__(self):
        super(core, self).__init__()
        file = pathlib.Path("pi_ble_reader.config")
        if file.exists ():
            print ("File exist")
        else:
            create_config_file('pi_ble_reader.config')


def create_config_file(file_path):
    with open("pi_ble_reader.config", "w") as f:
        f.write("##\t{:^24s}\t##\n".format('--- General ---'))
        f.write('mqtt_enabled = True\n')
        f.write('indluxdb_enabled = True\n')
        f.write('ruuvitags_enabled = True\n')


if __name__ == '__main__':
    core = core()
    os.getcwd()
    create_config_file('pi_ble_reader.config')
