import serial
import methodList2
import time
import datetime
import math
import sqlite3
import adafruit_gps
from digi.xbee.devices import XBeeDevice, XBee64BitAddress, XBee16BitAddress, RemoteXBeeDevice, DigiMeshDevice

##temporary because gps is not plugged in
lat = 38.435064
lon = -78.869581

calibrationConstant = 73
maxs = 10

##name serial ports
slavePort = '/dev/ttyACM1'
masterPort = '/dev/ttyACM0'
ports = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2"]
##gpsPort = 'yada-yada'
##radioPort = 'yada-yada'

##name the database file
databaseName = 'Database'
radio = XBeeDevice("/dev/ttyUSB0", 115200)
radio.set_sync_ops_timeout(6)
time.sleep(1)
homeradio = RemoteXBeeDevice(radio, XBee64BitAddress.from_hex_string("0013A20041EBAD4A"))
##name radios
radio.open()
nodes = methodList2.gatherNetwork(radio)
radio.send_data(homeradio, nodes.encode('utf-8'))
radio.close()
try:
    while True:
        ##Publish a list of network nodes and adresses
        radio.open()
        
        ##retrieve slave data
        slaveData = methodList2.slaveSerial(slavePort)
        rawDO, rawTurb = slaveData.split(", ")
        
        ##retrieve master data
        masterData = methodList2.masterSerial(masterPort)
        v = masterData
        calibratedV = v*(5.0/1024.0)
        Low = methodList2.lowPowerMode(calibratedV)
        
        
        ##retrieve data/time data
        dateTime = methodList2.getDateTime()
        formatted_time, date_string = dateTime.split(", ")
        
        ##retrieve gps data
        coord = methodList2.decToDMS(lat, lon)
        
        ##calibrate DO
        saturation = methodList2.calibrateDO(calibrationConstant, rawDO)
        
        ##calibrate turb
        turbidity = methodList2.calibrateTurb(rawTurb)
        
        ##format gps
        DMS = methodList2.decToDMS(lat, lon)
        latDMS, lonDMS = DMS.split(", ")
        
        print('Sensor collection worked')
        print(saturation, turbidity, calibratedV)
        ##write to SQL

        methodList2.writeToSQL(databaseName, saturation, turbidity, latDMS, lonDMS, formatted_time, date_string)
        #methodList2.writeToSQL2(databaseName, latDMS, lonDMS, formatted_time, date_string)
        conn = sqlite3.connect(databaseName)
        c = conn.cursor()
        select_stmt = "SELECT * FROM dataTable ORDER BY id DESC LIMIT 1"
        c.execute(select_stmt)
        record = c.fetchall()
        time.sleep(1)
        
        record_str = ','.join([str(value) for value in record])
        radio.send_data(homeradio, record_str.encode('utf-8'))
        print('Broadcasting...')
        
        if Low:
            maxs = 30
        else:
            maxs = 10   
        radio.close()
        time.sleep(maxs)   
        
        
except KeyboardInterrupt:
    conn.close()
    radio.close()
    ##slave.close()
    ##masterPort.close()
    ##gpsPort.close()
    ##radioPort.close()
    ##xbee.close()
    print("Serial Communication Closed.")
    


