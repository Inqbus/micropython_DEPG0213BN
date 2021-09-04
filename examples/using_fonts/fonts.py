from writer import Writer

from random import randint

import avantgard40

from eink import EInk

ink = EInk()
screen = ink.screen

screen.fill(1)

# screen.update_partial()

#sleep(5)

wri_big = Writer(screen, avantgard40)
Writer.set_textpos(screen, 32, 0)
temp = randint(0,300)
wri_big.printstring(u'{:.1f}C'.format(temp), invert=True)


#screen.rect(10,10,130,140,0)


screen.update_partial()

