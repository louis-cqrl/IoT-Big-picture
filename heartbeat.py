import machine
import ssd1306
from pyb import ADC, Pin, Timer
import framebuf
from machine import Pin
import time
import random as rd 
from time import time, sleep_ms
from pyb import ADC, Pin, Timer


i2c = machine.SoftI2C(scl=machine.Pin('A15'), sda=machine.Pin('C10'))
machine.Pin('C13', machine.Pin.OUT).low()  # mettre courant entrant
machine.Pin('A8', machine.Pin.OUT).high()  # mettre courant sortant
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

MAX_arr_value = 250
TOTAL_BEATS = 30

def compute_bpm(beats, previous_bpm):
    if beats:
        beat_time = beats[-1] - beats[0]
        if beat_time:
            n = (len(beats) / (beat_time)) * 60
            return n
    return previous_bpm

def display_heart():
    HEART = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0],
        [1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
    ]
    for y, row in enumerate(HEART):
        for x, c in enumerate(row):
            oled.pixel(x, y, c)

    oled.show()

old_y = 0

# display heartbeat
def display( bpm, value, min_value, max_value):
    global old_y

    oled.scroll(-1,0) 
    if max_value - min_value > 0:
        y = 64 - int(27 * (value - min_value) / (max_value - min_value))
        oled.line(125, old_y, 126, y, 1)
        old_y = y

    # Clear top text area
    oled.fill_rect(0,0,128,20,0)

    oled.text("%d bpm" % bpm, 12, 0)
    display_heart()
    
    oled.show()

def taker(arr_value = []):
    beats = []
    bpm = 60

    oled.fill(0)
    
    while True:
        value = ADC("C1").read()
        arr_value.append(value)
        #print(value)
        if value < MAX_arr_value:
            break
        
        arr_value = arr_value[-MAX_arr_value:]

        min_value, max_value = min(arr_value), max(arr_value)

        beats.append(time())
        beats = beats[-TOTAL_BEATS:]
        bpm = compute_bpm(beats, bpm)
        print("BPM: ", bpm)
            
        display(bpm, value, min_value, max_value)
    return arr_value