# SENSOR PART

import time
import ui
import pyb
from pyb import LED
from machine import Pin, ADC

global bpm, led, adc, buffer, c, limit, counter, lasts, lasts_limit, start_beat_time, last_beat_time, samples, no_samples, old_bpm, sw3, mean, sum_

# Pins, LED and others
sw2 = pyb.Pin('SW2', Pin.IN, Pin.PULL_UP)
sw3 = pyb.Pin('SW3', Pin.IN, Pin.PULL_UP)
led = LED(1)
adc = ADC(Pin('A0'))

# Variables

sum_ = 0
bpm = 0
old_bpm = -3

# Stockage of sensor's output
buffer = []
# Counter of points and limit : store 'limit' points
c = 0
limit = 50
counter = 0

# Last stockage of sensor's output with 'lasts_limits' points
lasts = []
lasts_limit = 500

# Start counting
start_beat_time = time.ticks_ms()
last_beat_time = 0

# Samples for BPM calculation
samples = []
no_samples = 10

# Intervall of 10 seconds
old_time = time.time()

# Mean
mean = 0

# Tests
# timer = pyb.Timer(1)
# timer.init(freq=10, callback=clock)

def sensor():
    global bpm, led, adc, buffer, c, limit, counter, lasts, lasts_limit, start_beat_time,  last_beat_time, samples, no_samples, sw3

    mean = 0

    # Reading value of the sensor
    buffer.append(adc.read_u16())

    c += 1
    if c >= limit:
        
        mean = sum(buffer) // limit
        c = 0
        buffer = []
        print('mean :', mean)

        for i in lasts:
            if (mean - i) > 1000 and (time.ticks_ms() - last_beat_time) > 200:

                # Calculate BPM
                total_time = time.ticks_ms() - start_beat_time
                bpm = int(60000 / total_time * counter)

                # oled.text('pulse', bpm)
                print(bpm)

                # Affichage pour le bpm
                #ui.draw(ui.empty_heart, 15, 21, 3)
                #ui.smart_text(ui.oled, str(bpm), 15, 40, not color)

                # Reset and exit loop
                last_beat_time = time.ticks_ms()
                counter += 1
                lasts = []
                break

        #ui.oled.show()

        # led.off()
        # oled.text('Pulse', 0, 0, 1)
        # oled.show()

        if len(lasts) >= lasts_limit:
            lasts.pop()
        lasts.insert(0, mean)

    return [bpm, mean]

def sensor_interface():
    global bpm, old_bpm

    darkmode = ui.darkmode
    color = not darkmode

    bpm = sensor()[0]
    if bpm != old_bpm:
        ui.oled.fill(color)
        ui.draw(ui.empty_heart, 15, 21, 3)
        ui.smart_text(ui.oled, str(bpm), 50, 25, not color)
        ui.oled.show()
    old_bpm = bpm

def sensor_plot_interface():
    global bpm, old_bpm
    
    darkmode = ui.darkmode
    color = not darkmode
    
    bpm = sensor()[0]
    mean = sensor()[1]
    
    ui.oled.pixel()

def sensor_2():
    global bpm, old_bpm, lasts, start_beat_time, counter, c, old_time, mean, last_beat_time, sum_, limit

    # Affichage
    darkmode = ui.darkmode
    color = not darkmode

    # Premier affichage
    if old_bpm == -3 :
        ui.oled.fill(color)
        ui.draw(ui.empty_heart, 15, 21, 3)
        ui.smart_text(ui.oled, "Calcul...", 50, 25, not color)
        ui.oled.show()
    


    # Period of time of 10 seconds
    while time.time() - old_time < 10:

        # Reading value of the sensor
        val = adc.read_u16()
        sum_ += val

        # Mean of the sensor's value
        c += 1
        if c >= limit:
            print(sum_, val)
            mean = sum_ // limit
            c = 0
            sum_ = 0
            #print('mean :', mean)

            for i in lasts:
                if (mean - i) > 1000 and (time.ticks_ms() - last_beat_time) > 200:
                    # Calculate BPM
                    total_time = time.ticks_ms() - start_beat_time
                    bpm = int(60000 / total_time * counter)

                    # oled.text('pulse', bpm)
                    print(bpm)

                    # Reset and exit loop
                    last_beat_time = time.ticks_ms()
                    counter += 1
                    lasts = []
                    break

                # oled.text('Pulse', 0, 0, 1)
                # oled.show()

            if len(lasts) >= lasts_limit:
                lasts.pop()
            lasts.insert(0, mean)

    # Reset toutes les variables
    samples = []
    sum_ = 0
    c = 0
    counter = 0
    last_beat_time = 0
    old_time = time.time()


    if bpm != old_bpm:
        ui.oled.fill(color)
        ui.draw(ui.empty_heart, 15, 21, 3)
        ui.smart_text(ui.oled, str(bpm), 50, 25, not color)
        ui.oled.show()
    old_bpm = bpm

