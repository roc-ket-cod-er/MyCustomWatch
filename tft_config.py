from machine import Pin, SPI
import gc9a01, time

TFA = 0
BFA = 0
WIDE = 0
TALL = 1

def config(rotation=0, buffer_size=0, options=0, speed=40_000_000):
    spi = SPI(1, baudrate=speed, sck=Pin(12), mosi=Pin(11))

    return gc9a01.GC9A01(
        spi,
        240,
        240,
        reset=Pin(48, Pin.OUT),
        cs=Pin(10, Pin.OUT),
        dc=Pin(14, Pin.OUT),
        backlight=Pin(47, Pin.OUT),
        rotation=rotation,
        options=options,
        buffer_size= buffer_size)