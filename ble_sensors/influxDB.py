#Tähän fileen teen kaikki indluxDB funktiot
from influxdb import InfluxDBClient
from ble_sensors import wenlins_logger

# Init logger
logger =  wenlins_logger.loggerClass(name = 'influxDB', file_logging = False, logging_level = 'info')
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
exception = logger.exception

def connect_to_server(host, port, username, password):
    client = InfluxDBClient(host=host, port= port, username = username, password = password)
    client.ping()
    info('Successfully connected to inluxDB server!')
    return client
def connect_to_database(client, database):
    db_list = list_databases(client)
    db_list = [db['name'] for db in db_list]
    if database in db_list:
        client.switch_database(database)
        info('Database found! Client connected to database.')
    else:
        info('{} not found from server. New database created!'.format(database))
        client.create_database(database)
        client.switch_database(database)
    return client
def list_databases(client):
     db_list = client.get_list_database()
     debug('Databases found from connected server:')
     for i, db in enumerate(db_list):
         debug('{} - {}'.format(i,db['name']))
     return db_list
def write_ruuvidata_to_influxdb(client, received_data):
    """
    Convert data into RuuviCollector naming schme and scale
    returns:
        Object to be written to InfluxDB
    """
    mac = received_data[0]
    payload = received_data[1]
    tag_name = received_data[2]

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
                'dataFormat': dataFormat,
                'tagName': tag_name
            },
            'fields': fields
        }
    ]
    print(json_body)
    client.write_points(json_body)

if __name__ == '__main__':
    client = connect_to_server(host, port, username, password)
    client = connect_to_database(client, 'environmental_measurements')
    client.close()
