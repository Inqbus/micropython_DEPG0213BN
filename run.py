from machine import SPI, Pin

import DEPG0213BN as epaper

# Setup SPI bus. The pins are mandatory for the TTGO T5 V2.3
espi = SPI(2,
           baudrate=20000000,
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
screen = epaper.EPD(espi, cs, dc, rst, busy)
# Set all to white
screen.fill(1)
# Write at (0,0) the text "hello World!" in color black
screen.text('Hello World!', 0, 0, 0)
# Write to the E-Ink display
screen.update()
