#Import required modules
import serial
import time
import datetime
import math
import sqlite3
from digi.xbee.devices import DigiMeshDevice, RemoteXBeeDevice, XBee64BitAddress, XBeeDevice


#Connect to SQLite Database
conn = sqlite3.connect('SensorData')
c = conn.cursor()
device = None

#Begins serial connection
ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1.0) ##Opens Communication at same rate on correct port
time.sleep(3) ##Waits for 3 seconds before starting after boot up
ser.reset_input_buffer() ##Stops data collection until buffer

#Checks if conenction is open
if ser.isOpen():
    print("Serial is Okay.")
else:
    print("Serial Connection is not Okay.")

#Main loop, retrieve values from serial, calibration equations
try:
    while True:
        time.sleep(0.01)
        if ser.in_waiting > 1:
            for x in range (1,3):
                line = ser.readline().decode('utf-8')
                #Read first value in serial string (dissolved oxygen)
                if x == 1:
                    place_holder = 74.0
                    sat = (float(line)/place_holder) * 100 * 1.01368474

                #Read second value in serial string (turbidity)
                if x == 2:
                    voltage = float(line) *(5.0/1024.0)
                   # turbidity = (633.15*(voltage**2)) - (5015.5*voltage)+9934.5
            
            #Retrieve time and date information
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime('%H:%M:%S')
            current_date = datetime.date.today()
            date_string = current_date.strftime('%Y-%m-%d')
            sent = "N"
            lattitude = 0
            longitude = 0
            
            #Write to SQLite Database
            c.execute("INSERT INTO sensordata (saturation, turbidity, currentdate, currenttime, lattitude, longitude, sent) VALUES (?, ?, ?, ?, ?, ?, ?)", (sat, voltage, date_string, formatted_time, lattitude, longitude, sent))
            conn.commit()
            time.sleep(1)
            
            #locations = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2", "/dev/ttyUSB3"]
            #for usb in locations:
                ##try:
                    #print('trying ' + usb)
            device = DigiMeshDevice("/dev/ttyUSB0", 115200)
            device.open()
                    #break
                #except:
                    #pass
            
            select_stmt = "SELECT * FROM sensordata"
            c.execute(select_stmt)
            records = c.fetchall()
            

            time.sleep(1)

            for record in records:
                record_str = ','.join([str(value) for value in record])

                device.send_data_broadcast(record_str.encode())
                print('Broadcasting...')
                time.sleep(10)
            c.close()

#Close Communication
except KeyboardInterrupt:
    print("Serial Communication Closed.")
    ser.close()
    conn.close()
    device.close()
