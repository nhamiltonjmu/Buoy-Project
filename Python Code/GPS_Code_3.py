#needed to count time
import time

#can only be installed via pip install adafruit-circuitpython-gps (at the moment)
import adafruit_gps

#import serial via PySerial
import serial


def getGPSdata():
    ## Original program based upon Adafruit Ultimate GPS Demo
    ## https://github.com/adafruit/Adafruit_CircuitPython_GPS/blob/master/examples/gps_simpletest.py
    ## Modifications made by Collete Higgins and Jason Forsyth (forsy2jb@jmu.ed)

    #add in code to search for USB...
    serial_port_name="/dev/ttyUSB0"

    #create serial instance to talk with USB GPS
    uart = serial.Serial(serial_port_name, baudrate=9600, timeout=10)

    # Create a GPS module instance.
    gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial

    # Turn on the basic GGA and RMC info (what you typically want)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

    # Set update rate to once every 1000ms (1hz) which is what you typically want.
    gps.send_command(b"PMTK220,1000")

    # Main loop runs forever printing the location, etc. every second.
    last_print = time.monotonic()
    while True:
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

            lat = gps.latitude
            lon = gps.longitude

            # limit decimal places of latitude and longitude
            limited_lat = "{:.6f}".format(gps.latitude)
            limited_long = "{:.6f}".format(gps.longitude)

            # convert from float to string
            lat_in_string = str(limited_lat)
            long_in_string = str(limited_long)

            # concatenate string
            gps_string = lat_in_string + "," + long_in_string



def decToDMS(lat, lon):
    ##determine N/S and E/W
    latDirection = 'N' if lat >= 0 else 'S'
    lonDirection = 'E' if lon >= 0 else 'W'
    
    ##convert numbers to absolute value so the math works
    latABS = abs(lat)
    lonABS = abs(lon)
    
    ##calculating degrees, minutes, and seconds (rounded to four decimals)
    latDeg = int(latABS)
    latMin = int((latABS - latDeg) * 60)
    latSec = (((latABS - latDeg) * 60 - latMin) * 60)
    roundedLatSec = round(latSec, 4)
    
    ##same but for longitude
    lonDeg = int(lonABS)
    lonMin = int((lonABS - lonDeg) * 60)
    lonSec = ((((lonABS - lonDeg) * 60) - lonMin) * 60)
    roundedLonSec = round(lonSec, 4)
    
    ##creating strings in DMS format
    latDMS = f"{latDeg}° {latMin}' {latSec}\" {latDirection}"
    lonDMS = f"{lonDeg}° {lonMin}' {lonSec}\" {lonDirection}"
    
    return(latDMS + ", " + longDMS)

coord = getGPSdata()
lat, lon = coord.split(", ")
DMS = decToDMS(lat, lon)
latDMS, lonDMS = DMS.split(", ")

print f"{latDMS}, {lonDMS}"
