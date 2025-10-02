print("\n\n ============================ STARTING TEST_MAIN ============================")

import network
import os
import gc9a01
import utime
import my_secrets
import tft_config
import sys
import random
from umqtt.robust import MQTTClient
from machine import Timer, Pin, PWM, UART
import vga1_bold_16x32 as font
from micropyGPS import MicropyGPS


buzzer = Pin(15, Pin.OUT)

def beep(frequency=3600):
    buzzer_pwm = PWM(buzzer, freq=frequency)
    buzzer_pwm.duty_u16(32768)
    utime.sleep(0.075)
    buzzer_pwm.duty_u16(0)
    buzzer_pwm.deinit()

tft = tft_config.config(tft_config.TALL)
tft.rotation(0)
tft.init()
tft.fill(gc9a01.BLACK)

print("Got all imports!")
beep()
utime.sleep(0.1)
beep()

HOUR_OFFSET = -4
MIN_OFFSET = 0
SEC_OFFSET = 0#-0.086

gps_serial = UART(1, baudrate=9600, tx=17, rx=18)
my_gps = MicropyGPS()

previous_timstamp = [0,0,0]
connected_to_gps = False

while True:
    satsInUse = 0
    satsInView = 0
    while gps_serial.any():
        data = gps_serial.read()
        for byte in data:
            stat = my_gps.update(chr(byte))
            if stat is not None:
                #print(my_gps.timestamp)
                print(my_gps.satellites_in_use, my_gps.satellites_in_view)

                if my_gps.satellites_in_use > satsInUse:
                    satsInUse = my_gps.satellites_in_use
                if my_gps.satellites_in_view > satsInView:
                    satsInView = my_gps.satellites_in_view

                if my_gps.satellites_in_use >= 1:
                    connected_to_gps = True
                else:
                    connected_to_gps = False

                timestamp = my_gps.timestamp
                if timestamp != previous_timstamp:
                    hour = timestamp[0] + HOUR_OFFSET
                    min = timestamp[1] + MIN_OFFSET
                    sec = round(timestamp[2] + SEC_OFFSET)
                    milisec = (timestamp[2] + SEC_OFFSET) % 1

                    if hour < 0:
                        hour += 24

                    print(f"{hour:02}h {min:02}:{sec:02}", milisec)


                    #tft.fill(0)

                    '''if not connected_to_gps:
                        print("CONNECTING TO GPS...")
                        tft.text(
                            font,
                            "Connecting..",
                            36, 136, gc9a01.RED
                        )
                        tft.text(
                            font,
                            f"{satsInUse}/{satsInView} SATs",
                            50, 174, gc9a01.RED
                    else:'''
                    print("CONNECTED TO GPS!")
                    tft.text(
                        font,
                        "Connected",
                        36, 136, gc9a01.BLUE
                    )
                    tft.text(
                        font,
                        f"{satsInUse}/{satsInView} SATs",
                        50, 174, gc9a01.BLUE
                    )
                    tft.text(font,
                            f"{hour:02}h {min:02}:{sec:02}",
                            48, 84, gc9a01.WHITE)
                    previous_timstamp = timestamp


secrets = my_secrets.secrets()

ps = Pin(16, Pin.OUT)
ps.off()

WIFI_SSID = secrets.ssid
WIFI_PWD = secrets.wifi_password

ADAFRUIT_KEY = secrets.aio_key
ADAFRUIT_USERNAME = secrets.user_name
ADAFRUIT_IO_URL = 'io.adafruit.com'

SPEED_FEED_ID = 'speed'
BATTERY_FEED_ID = 'Battery %'

MQTT_CLIENT_ID = bytes('WATCH1', 'uft-8')

speed = random.randint(1, 35)

client = MQTTClient(client_id=MQTT_CLIENT_ID, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_KEY,
                    ssl=False)


print("This directory contains: ", " | ".join(os.listdir()))


def connect_to_wifi():
    station = network.WLAN(network.STA_IF)

    station.active(True)


    station.connect(WIFI_SSID, WIFI_PWD)

    while not station.isconnected():
        print("Connecting to Wi-Fi...")
        utime.sleep(0.5)
    print("\nConnected to Wi-Fi!")

    print("Network config:", station.ifconfig())

connect_to_wifi()

try:            
    mute_out = client.connect()
    print("connected to MQTT")
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

speed_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, SPEED_FEED_ID), 'utf-8')

def pub_data(data):
    global speed

    change_by = speed - 17
    change_by /= 3

    print(change_by)
    
    change_by = abs(change_by)
    change_by = 3 if change_by < 3 else change_by

    print(change_by)

    speed += random.uniform(-change_by, change_by)
    
    speed = 5 if speed <= 5 else speed
    speed = 35 if speed >= 35 else speed


    client.publish(speed_feed,    
                  bytes(str(speed), 'utf-8'),   # Publishing Temp feed to adafruit.io
                  qos=0)
    print(f"published! {speed}")
    print("Message from Timer5\n\n")
    return None



timer5 = Timer(0)
timer5.init(period=2500, mode=Timer.PERIODIC, callback = pub_data)

while True:
    try:
        utime.sleep(1)
    except KeyboardInterrupt as e:
        print(e)
        print ("Stopping Timer5")
        timer5.deinit()
        sys.exit()