# main.py -- put your code here!

import time
import ssd1306
import machine
from pyb import ADC

import heartbeat as hb

i2c = machine.SoftI2C(scl=machine.Pin('A15'), sda=machine.Pin('C10'))
machine.Pin('C13', machine.Pin.OUT).low()  # mettre courant entrant
machine.Pin('A8', machine.Pin.OUT).high()  # mettre courant sortant
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

rtc = machine.RTC()
h_tuple = (2023, 4, 17, 3, 20, 0, 0, 0)
rtc.datetime(h_tuple)

while(1):
    oled.fill(0)
    h_tuple = time.localtime()
    oled.text("Date: %d/%d/%d" % (h_tuple[2], h_tuple[1], h_tuple[0]), 0, 0)
    oled.text("Heure: %d:%d:%d" % (h_tuple[3], h_tuple[4], h_tuple[5]), 0, 10)
    oled.show()
    n = 0
    if n == 0:
        history = []
    history = hb.taker(history)
    print(history)
    n += 1