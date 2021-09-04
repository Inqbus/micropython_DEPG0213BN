from machine import SPI, Pin
from writer import Writer

import DEPG0213BN as epaper

class EInk:
    
    def __init__(self):
        # Setup SPI bus. The pins are mandatory for the TTGO T5 V2.3
        espi = SPI(2,
                   baudrate=4000000,
                   sck=Pin(18),
                   mosi=Pin(23),
                   polarity=0,
                   phase=0,
                   firstbit=SPI.MSB)

        # The pins a mandatory for the TTGO T5 V2.3
        rst = Pin(16, Pin.OUT, value=1)
        dc = Pin(17, Pin.OUT, value=1)
        cs = Pin(5, Pin.OUT, value=1)
        busy = Pin(4, Pin.IN, value=0)

        # Instantiate a Screen
        self.screen = epaper.EPD(espi, cs, dc, rst, busy, rotation=epaper.ROTATION_90)
        