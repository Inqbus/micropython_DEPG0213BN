# micropython_DEPG0213BN

Pure Micropython driver for the DEPG0213BN E-Ink display found on the TTGO T5 V2.3 ESP32 boards

Overview
---------

The TTGO T5 V2.3 ESP32 boards with E-Ink displays are a really cool platform for DIY and also for 
scientific applications. 

[If you just want to use these boards for your home automatisation, please have a look at esphome/homeassistant. 
They have a quite complete integration of these devices.]

My data aquisition is based on amqtt_db and therefore I like to have more Python control over my sensors and the display.

So I shamelessly translated the CPP code of esphome to Micropython. I also stole some code from 
https://github.com/Xinyuan-LilyGO/LilyGo-eink-v2.3-micropython/blob/master/README.MD

Installation
------------

Just copy DEPG0213BN.py to your ESP32 Micropython device.


Usage
-----

run.py gives you a "Hello World!" example which shows the usage of the driver.

Examples
--------

In the examples folder there is code to display arbitrary fonts.  


Limitations
-----------

  * Partial updates are implemented, but only for the whole display.
  * This code is just a prove of concept. So please do not rely on any bit of it.
