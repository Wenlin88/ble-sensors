# @Author: Wenlin88
# @Date:   29-Feb-2020
# @Email:  Wenlin88@users.noreply.github.com
# @Last modified by:   Wenlin88
# @Last modified time: 08-Mar-2020

import sys

class core(object):
    """docstring for core."""

    def __init__(self):
        super(core, self).__init__()

        print(sys.path.exists('pi_ble_reader.config'))

if __name__ == '__main__':
    core = core()
