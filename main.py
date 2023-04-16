#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import machine
import pyb
import micropython
import time
from machine import Pin, ADC
from pyb import LED

import ui
import menu
import clock
import sensor
import game

micropython.alloc_emergency_exception_buf(100)


screen = 0
number_of_screens = 5
# On 0 : clock interface
# On 1 : analog clock
# On 2 : sensor plot
# On 3 : pong game

# SW2 switch to display the menu
sw2 = pyb.Pin('SW2', machine.Pin.IN, machine.Pin.PULL_UP)

#adc = ADC(Pin('A0'))

# Start of the clock application
ui.oled.fill(not ui.darkmode)
ui.smart_text(ui.oled, "MICROPY", (128 - len("MICROPY") * 8) // 2, 16, ui.darkmode)
ui.smart_text(ui.oled, "WATCH", (128 - len("WATCH") * 8) // 2, 40, ui.darkmode)
ui.oled.show()
time.sleep(2)

while True:

    # Set the good color depending on darkmode (not possible to change in game - screen 3)
    if screen != 3:
        ui.change_mode()

    # SW2.value == 1 when not pressed and == 0 when pressed
    if not sw2.value():
        while not sw2.value():
            pass

        # Change to menu
        screen = menu.menu_interface()

        # Display of the menu of plot before the plot display
        if screen == 2:
            sensor.before_sensor()
            time.sleep(4)
        # Reset of old bpm
        sensor.old_bpm = -3

        # Set the good color depending on darkmode
        darkmode = ui.darkmode
        color = not darkmode
        ui.oled.fill(color)

    if screen == 0:
        # Digital clock
        clock.clock_interface()

    elif screen == 1:
        # Analog clock
        clock.analog_clock_interface()

    elif screen == 2:
        # Sensor plot
        sensor.sensor()

    elif screen == 3:
        # Pong game
        game.pong_interface()
