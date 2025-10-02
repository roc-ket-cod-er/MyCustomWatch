import machine
from utime import sleep
from micropyGPS import MicropyGPS

print("Got Imports!")

# Instantiate the micropyGPS object
my_gps = MicropyGPS()

# Define the UART pins and create a UART object
gps_serial = machine.UART(2, baudrate=9600, tx=17, rx=18)

while True:
    while gps_serial.any():
        data = gps_serial.read()
        for byte in data:
            stat = my_gps.update(chr(byte))
            if stat is not None:
                # Print parsed GPS data
                print('UTC Timestamp:', my_gps.timestamp)
                print('Date:', my_gps.date_string('long'))
                print('Latitude:', my_gps.latitude_string())
                print('Longitude:', my_gps.longitude_string())
                print('Altitude:', my_gps.altitude)
                print('Satellites in use:', my_gps.satellites_in_use)
                print('Horizontal Dilution of Precision:', my_gps.hdop)
                print()