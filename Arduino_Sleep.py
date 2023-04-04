import serial ##Imports module for communicating with Arduino
from serial.tools.list_ports import comports
import time ##Imports module for timing
import math
import RPi.GPIO as GPIO

portName1 = '/dev/ttyACM0'
portName3 = '/dev/ttyACM2'
##portName2 = '/dev/ttyAMA0'
baudRate = 115200
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

try:
    ser = serial.Serial(portName3, baudRate)
    ser1 = serial.Serial(portName1, baudRate)
    ##ser2 = serial.Serial(portName2, baudRate)
    print("Opening port " + ser.name)
except:
    print("Couldn't open port")
    ports_list = comports()
    for port_candidate in ports_list:
        print(port_candidate.device)
    exit(-1)
if ser.is_open == True:
    print('Success!')
else:
    print('Unable to open port :(')
##Opens Communication at same rate on correct port
time.sleep(1) ##Waits for 3 seconds before starting after boot up
ser.reset_input_buffer()
ser1.reset_input_buffer()
##ser2.reset_input_buffer()
clife = None
onoff = "Y"
working = True
lowpm = 0
print("Serial is Okay.")

def lifetime(c, v):
    if c >= 10:
        t1 = -3599 + (473*v) + (11.7*(v**2)) + (-2.17*(v**3))
        ta = -3599 + (473*10.5) + (11.7*(10.5**2)) + (-2.17*(10.5**3))
    elif c < 10 and c > 5:
        t1 = -5565 + (1132*v) + (-55.6*(v**2))
        ta = -5565 + (1132*10.5) + (-55.6*(10.5**2))
    else:
        t1 = 5299 + (-2018*v) + 248*(v**2) + (-9.76*(v**3))
        ta = 5299 + (-2018*10.5) + 248*(10.5**2) + (-9.76*(10.5**3))
    time1 = (ta - t1)/60
    print(time1)
    lowpm = time1 - .5
    return time1
    
        
def checklifetime(c, v):
    time = lifetime(c, v)   
    ##peukert = c / 2
    ##time = v * peukert
    if time1 > .5:
        return True
    else:
        return False
try:   
    while working:
        time.sleep(1)
        if ser.in_waiting > 1:
            for x in range (1,3):
                line = ser.readline().decode('utf-8')
                if x == 1:
                    currentf = float(line)
                    print(currentf, end=', ')
                if x == 2:
                    voltage = float(line)
                    print(voltage, end=', ')
            clife = checklifetime(currentf, voltage)
            print(clife)
            if clife:
                print('all good')
                if onoff == 'N':
                    onoff = 'Y'
                    GPIO.output(7, True)
                    time.sleep(1)
                    GPIO.output(7, False)
                    time.sleep(1)
                    ser1.write(str.encode('Y'))      
            else:
                byte_onoff = str.encode('N')
                ser1.write(byte_onoff)
                onoff = 'N'

except KeyboardInterrupt:
    print("Serial Communication Closed.")
    ser.close()
    ser1.close()
    ##ser2.close()
        