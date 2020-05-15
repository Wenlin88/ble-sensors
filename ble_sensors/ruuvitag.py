# @Author: Wenlin88
# @Date:   07-Mar-2020
# @Email:  Wenlin88@users.noreply.github.com
# @Last modified by:   Wenlin88
# @Last modified time: 07-Mar-2020

from ruuvitag_sensor.ruuvi import RuuviTagSensor
import ruuvitag_sensor.log
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from influxdb import InfluxDBClient
import os


from ble_sensors import ble_sensor_config, wenlins_logger, ruuvitag, influxDB


# Init logger
logger =  wenlins_logger.loggerClass(name = 'ruuvitag', file_logging = False, logging_level = 'debug')
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
exception = logger.exception





def find_ruuvitags():
    # Tällä funkkarilla voi etsiä tarvittavat
    ruuvitag_sensor.log.enable_console()
    RuuviTagSensor.find_ruuvitags()
def get_data(ruuvitags = '', timeout = 5):
    # Tällä funktiolla voi hakea useammasta ruuvitagista datan samalla kertaa
    debug('Reading data from RuuviTags for {:}s'.format(timeout))
    data = RuuviTagSensor.get_data_for_sensors(ruuvitags, timeout)
    debug('Recieved data:')
    debug(data)
    return data
def fetch_data_and_send(listening_time = 10):
    print('Fetching data...')
    data = RuuviTagSensor.get_data_for_sensors(search_duratio_sec = listening_time)
    print('Data fetch OK!')
    print('Found tags:')
    if len(data) > 0:
        for i,value in enumerate(data):
            print(str(i+1) + ' : ' + value)
            write_to_influxdb(list(data.items())[i])
    print('Data send succesfully!')
def puplish_single_example():
    #Tämän tein vain esimerkiksi. En raskinut kuitenkaan poistaa, jos tarvitsee käyttää single rakennetta jatkossa
    auth = {
      'username':"*******",
      'password':"*******"
    }



    publish.single("home-assistant/henkka/mood",
      payload="Toimii!",
      hostname=broker_address,
      client_id='PI4',
      auth=auth,
      port=1883,
      protocol=mqtt.MQTTv311)
def handle_data(found_data):
    print('MAC ' + found_data[0])
    print(found_data[1])
def old_stuff():
    # # TODO: ENNEN kun julkaiset tätä niin muista vaihtaa nämä salasanat HA:sta!. DONE!
    # MQTT muuttujat
    ha_address="192.168.10.48"
    client = mqtt.Client("PI4")
    client.username_pw_set(username='*****',password='*****')

    #influxDB alustus ruuvitageja vartendfvg
    client = InfluxDBClient(host=ha_address, port=8086, database='ruuvi',username='*****', password='*****')

    class reader(object):
        """ --- docstring for reader ---
        This class is used to manage ruuvitag reader configuration and tasks to read
        ruuvitags through """

        def __init__(self):
            super(reader, self).__init__()


if __name__ == '__main__':
    pass
