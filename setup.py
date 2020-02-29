# @Author: Wenlin88
# @Date:   29-Feb-2020
# @Email:  Wenlin88@users.noreply.github.com
# @Last modified by:   Wenlin88
# @Last modified time: 29-Feb-2020

from setuptools import setup, find_packages

setup(name='pi_ble_reader',
      version='0.0.1',
      description='Python module to read all sorts of BLE sensors with Raspberry Pi',
      url='https://github.com/Wenlin88/Pi_BLE_Reader',
      author='Wenlin88',
      author_email='Wenlin88@users.noreply.github.com',
      license='GPL-3.0',
      packages=find_packages(),
      install_requires=["ruuvitag_sensor>=0.13.0",
      "paho-mqtt>=1.5.0",
      "influxdb>=5.2.3"],
      classifiers=['Programming Language :: Python :: 3'],
      zip_safe=False)
