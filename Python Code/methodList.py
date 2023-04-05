import sqlite3
import datetime


def calibrateDO(calibrationConstant, rawDO):
    ##calibration equation to take raw voltage and turn it into a percent saturation value
    sat = (float(rawDO)/calibrationConstant) * 100 * 1.01368474
    return sat


def calibrateTurb(rawTurb):
    ##calibration equation to take raw voltage and turn it into a turbidity value (NTU)
    voltage = float(rawTurb) *(5.0/1024.0)
    turbidity = (633.15*(voltage**2)) - (5015.5*voltage)+9934.5
    return turbidity


def decToDMS(lat, long):
    ##determine N/S and E/W
    lat_direction = 'N' if lat >= 0 else 'S'
    lon_direction = 'E' if long >= 0 else 'W'
    
    ##convert numbers to absolute value so the math works
    latABS = abs(lat)
    lonABS = abs(long)
    
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


def writeToSQL(saturation, turbidity, NS, EW, formatted_time, date_string):
    ##connect to specific datebase, "SampleDatabase.db", and create cursor
    conn = sqlite3.connect('SampleDatabase.db')
    c = conn.cursor()
    
    ##write values into respective columns of table, "TestTable"
    c.execute("INSERT INTO TestTable (saturation, turbidity, lat, long, currenttime, currentdate) VALUES (?, ?, ?, ?, ?, ?)", (saturation, turbidity, NS, EW, formatted_time, date_string))
    
    ##commit updates to table
    conn.commit()
    
    
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
    
