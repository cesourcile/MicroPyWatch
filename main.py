#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import machine
import pyb
import micropython
from machine import Pin, ADC
from pyb import LED

import ui
import clock
import sensor

micropython.alloc_emergency_exception_buf(100)

# On 0 : clock interface
# On 1 : sensor interface
# On 2 : analog clock
# On 3 : sensor plot
screen = 0
sw2 = pyb.Pin('SW2', machine.Pin.IN, machine.Pin.PULL_UP)

while True:

	# Darkmode or not
	ui.change_mode()
	#print(ui.darkmode)

	# sw2.value == 1 when not pressed and == 0 when pressed
	if not sw2.value():
		screen = (screen + 1) % 4
		#print(screen)
		sensor.old_bpm = -3
		while not sw2.value():
			pass

	# Change of screens
	if screen == 0:
		clock.clock_interface()
	elif screen == 1:
		#ui.oled.fill(1)
		#ui.draw(ui.empty_heart, 15, 21, 3)
		#ui.oled.show()
		sensor.sensor_2()
	elif screen == 2:
		clock.analog_clock_interface()
		#ui.oled.fill(1)
		#ui.oled.show()
	else:
		#ui.oled.fill(1)
		#ui.oled.show()
		sensor.sensor_interface()


	