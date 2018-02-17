import serial
import pynmea2
import sys
import math
def configureGPS(GPS_SERIAL_PORT):
	#Configure GPS 
	PMTK_SET_NMEA_BAUDRATE = '$PMTK251,9600*17'
	PMTK_SET_NMEA_UPDATE_5HZ = "$PMTK220,200*2C"
	PMTK_SET_NMEA_OUTPUT_RMCONLY = '$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29'
	PMTK_SET_NMEA_OUTPUT_RMCGGA = "$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28"
	PMTK_SET_NMEA_OUTPUT_GGAONLY = "$PMTK314,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29"

	serial_gps = serial.Serial()
	serial_gps.port = GPS_SERIAL_PORT
	serial_gps.baudrate = 9600
	serial_gps.open()
	serial_gps.write(PMTK_SET_NMEA_BAUDRATE + '\r\n')
	serial_gps.write(PMTK_SET_NMEA_OUTPUT_GGAONLY + '\r\n')
	serial_gps.write(PMTK_SET_NMEA_UPDATE_5HZ + '\r\n')

def getRawGPS(Links = 5):
	line = serial_gps.readline()
	read  = pynmea2.parse(line, check = True)
	if int(read.num_sats) >= Links:
		return True ,[read.latitude, read.longitude]
	else:
		return False, read

def getDestination(waypoint,position):
	deltaLat = waypoint[0] - position[0]
	deltaLong = waypoint[1] - position[1]
	bearing = math.atan2(deltaLat/deltaLong)
	dist = (deltaLong**2+deltaLat**2)**0.5
