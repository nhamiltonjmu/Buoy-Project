def decimal_to_dms(lat, long);
    lat_direction = 'N' if lat >= 0 else 'S'
    lon_direction = 'E' if long >= 0 else 'W'
    
    lat_deg = int(lat)
    lat_min = int((lat - lat_deg) * 60)
    lat_sec = (((lat - lat_deg) * 60_ - lat_min) * 60)
    
    lon_deg = int(long)
    lon_min = int((long - long_deg) * 60)
    lon_sec = int((((long - lon_deg) * 60) - lon_min) * 60)
    
    return (lat_deg, lat_min, lat_sec, lat_direction), (lon_deg, lon_min, lon_sec, lon_direction)

lat_dms, lon_dms = decimal_to_dms(lat, long)
print("Latitude (DMS):", lat_dms)
print("Longitude (DMS):", lon_dms)