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







def find_ruuvitags():
    # Tällä funkkarilla voi etsiä tarvittavat
    ruuvitag_sensor.log.enable_console()
    RuuviTagSensor.find_ruuvitags()
def get_data(ruuvitags = '', timeout = 5):
    # Tällä funktiolla voi hakea useammasta ruuvitagista datan samalla kertaa
    data = RuuviTagSensor.get_data_for_sensors(ruuvitags, timeout)
    return data
def write_to_influxdb(received_data):
    """
    Convert data into RuuviCollector naming schme and scale
    returns:
        Object to be written to InfluxDB
    """
    mac = received_data[0]
    payload = received_data[1]

    dataFormat = payload['data_format'] if ('data_format' in payload) else None
    fields = {}
    fields['temperature']               = payload['temperature'] if ('temperature' in payload) else None
    fields['humidity']                  = payload['humidity'] if ('humidity' in payload) else None
    fields['pressure']                  = payload['pressure'] if ('pressure' in payload) else None
    fields['accelerationX']             = payload['acceleration_x'] if ('acceleration_x' in payload) else None
    fields['accelerationY']             = payload['acceleration_y'] if ('acceleration_y' in payload) else None
    fields['accelerationZ']             = payload['acceleration_z'] if ('acceleration_z' in payload) else None
    fields['batteryVoltage']            = payload['battery']/1000.0 if ('battery' in payload) else None
    fields['txPower']                   = payload['tx_power'] if ('tx_power' in payload) else None
    fields['movementCounter']           = payload['movement_counter'] if ('movement_counter' in payload) else None
    fields['measurementSequenceNumber'] = payload['measurement_sequence_number'] if ('measurement_sequence_number' in payload) else None
    fields['tagID']                     = payload['tagID'] if ('tagID' in payload) else None
    fields['rssi']                      = payload['rssi'] if ('rssi' in payload) else None
    json_body = [
        {
            'measurement': 'ruuvi_measurements',
            'tags': {
                'mac': mac,
                'dataFormat': dataFormat
            },
            'fields': fields
        }
    ]
    client.write_points(json_body)
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
      'username':"mqtt",
      'password':"ruuvitag"
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
