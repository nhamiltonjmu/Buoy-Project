import sqlite3
import time
import serial
import datetime
import adafruit_gps
#comms imports
from digi.xbee.devices import XBeeDevice
#from digi.xbee.models.mode import NeighborDiscoveryMode
#from digi.xbee.models.options import DiscoveryOptions



def calibrateDO(calibrationConstant, rawDO):
    ##calibration equation to take raw voltage and turn it into a percent saturation value
    sat = (float(rawDO)/calibrationConstant) * 100 * 1.01368474
    return sat


def calibrateTurb(rawTurb):
    ##calibration equation to take raw voltage and turn it into a turbidity value (NTU)
    voltage = float(rawTurb) *(5.0/1024.0)
    turbidity = (-839.04*voltage) + 3217.7 - 49
    
    return turbidity


def decToDMS(lat, lon):
    ##determine N/S and E/W
    lat_direction = 'N' if lat >= 0 else 'S'
    lon_direction = 'E' if lon >= 0 else 'W'
    
    ##convert numbers to absolute value so the math works
    latABS = abs(lat)
    lonABS = abs(lon)
    
    ##calculating degrees, minutes, and seconds (rounded to four decimals)
    lat_deg = int(latABS)
    lat_min = int((latABS - lat_deg) * 60)
    lat_sec = (((latABS - lat_deg) * 60 - lat_min) * 60)
    rounded_lat_sec = round(lat_sec, 4)
    
    ##same but for longitude
    lon_deg = int(lonABS)
    lon_min = int((lonABS - lon_deg) * 60)
    lon_sec = ((((lonABS - lon_deg) * 60) - lon_min) * 60)
    rounded_lon_sec = round(lon_sec, 4)
    
    ##converting to strings so it writes properly
    ##PROBABLY A BETTER WAY TO DO THIS
    lat_direction_str = str(lat_direction)
    lon_direction_str = str(lon_direction)
    lat_deg_str = str(lat_deg)
    lat_min_str = str(lat_min)
    lat_sec_str = str(rounded_lat_sec)
    lon_deg_str = str(lon_deg)
    lon_min_str = str(lon_min)
    lon_sec_str = str(rounded_lon_sec)
    
    ##creating strings in DMS format
    latDMS = str(lat_deg_str + "° " + lat_min_str + "' " + lat_sec_str + "\" " + lat_direction_str)
    longDMS = str(lon_deg_str + "° " + lon_min_str + "' " + lon_sec_str + "\" " + lon_direction_str)
    
    return(latDMS + ", " + longDMS)


def writeToSQL(databaseName, saturation, turbidity, latDMS, lonDMS, formatted_time, date_string):
    ##connect to specific datebase, "SampleDatabase.db", and create cursor
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()
    
    ##write values into respective columns of table, "TestTable"
    c.execute("INSERT INTO dataTable (saturation, turbidity, latitude, longitude, time, date) VALUES (?, ?, ?, ?, ?, ?)", (saturation, turbidity, latDMS, lonDMS, formatted_time, date_string))
    
    ##commit updates to table
    conn.commit()
    conn.close()
    
def writeToSQL2(latDMS, lonDMS, formatted_time, date_string):
    
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()
    
    c.execute("INSERT INTO dataTable2 (latitude, longitude, time, data) VALUES (?, ?, ?, ?)", (latDMS, lonDMS, formatted_time, date_string))
    
    conn.commit()
    conn.close()
    
def getDateTime():
    ##uses datetime import to get current time and date
    current_time = datetime.datetime.now()   
    current_date = datetime.date.today()
    
    ##Formates time and date into H:M:S and Y-m-d respectively 
    formatted_time = current_time.strftime('%H:%M:%S')
    date_string = current_date.strftime('%Y-%m-%d')
    
    #creates string with formatted time and date
    dateTimeOutput = (formatted_time + ", " + date_string)
    
    return dateTimeOutput
    
def slaveSerial(slavePort):
    slave = serial.Serial(slavePort, 115200, timeout=1.0)
    slave.reset_input_buffer()
    while True:
        time.sleep(0.01)
        if slave.in_waiting > 0:
            slaveData = slave.readline().decode('utf-8')
            slave.close()
            return(slaveData)
        
def masterSerial(masterPort):
    master = serial.Serial(masterPort, 115200, timeout=1.0)
    master.reset_input_buffer()
    while True:
        time.sleep(0.01)
        if master.in_waiting > 0:
            masterData = master.readline().decode('utf-8')
            master.close()
            return(float(masterData))

def lowPowerMode(v):
    
    v = v*3
    
    t1 = 5299 + (-2018*v) + 248*(v**2) + (-9.76*(v**3))
    ta = 5299 + (-2018*10.5) + 248*(10.5**2) + (-9.76*(10.5**3))
    time1 = (ta - t1)/60
    
    if time1 <= .5:
        return True
    else:
        return False
    
def gatherGPSData(gpsPort):
    #create serial instance to talk with USB GPS    uart = serial.Serial(serial_port_name, baudrate=115200, timeout=10)

    # Create a GPS module instance.
    gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial

    # Initialize the GPS module by changing what data it sends and at what rate.
    # These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
    # PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
    # the GPS module behavior:
    #   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

    # Turn on the basic GGA and RMC info (what you typically want)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    # Turn on just minimum info (RMC only, location):
    # gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
    # Turn off everything:
    # gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
    # Turn on everything (not all of it is parsed!)
    # gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

    # Set update rate to once every 1000ms (1hz) which is what you typically want.
    gps.send_command(b"PMTK220,1000")


    # Main loop runs forever printing the location, etc. every second.
    last_print = time.monotonic()
    while True:
        # Make sure to call gps.update() every loop iteration and at least twice
        # as fast as data comes from the GPS unit (usually every second).
        # This returns a bool that's true if it parsed new data (you can ignore it
        # though if you don't care and instead look at the has_fix property).
        gps.update()

        # Every second print out current location details if there's a fix.
        current = time.monotonic()
        if current - last_print >= 1.0:
            last_print = current
            if not gps.has_fix:

                # Try again if we don't have a fix yet.
                print("Waiting for fix...")

                #continue to loop (while)
                continue

            # print the lat and long to the PI screen up to 6 decimal places
            print("Lat: {0:.6f}".format(gps.latitude))
            print("Long: {0:.6f}".format(gps.longitude))

            ##prepare data for transmission through Radio connected via USB

            # limit decimal places of latitude and longitude
            limited_lat = "{:.6f}".format(gps.latitude)
            limited_long = "{:.6f}".format(gps.longitude)

            # convert from float to string
            lat_in_string = str(limited_lat)
            long_in_string = str(limited_long)

            # concatenate string
            gps_string = lat_in_string + "," + long_in_string

            # convert from string to bytes
            gps_data = str.encode(gps_string)
            break
            # send data down USB port to radio.
            #data_out_port.write(gps_data)

def gatherNetwork(radio):
    xnet = radio.get_network()
    xnet.start_discovery_process()
    while xnet.is_discovery_running():
        time.sleep(0.5)
    nodes = xnet.get_devices()
    node_str = ''
    for node in nodes:
        node_str += str(node) + ', '
    return node_str


