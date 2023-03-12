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
# On 1 : analog clock
# On 2 : sensor menu
# On 3 : sensor plot
screen = 0
sw2 = pyb.Pin('SW2', machine.Pin.IN, machine.Pin.PULL_UP)

adc = ADC(Pin('A0'))

while True:

	# Darkmode or not
	ui.change_mode()

	# sw2.value == 1 when not pressed and == 0 when pressed
	if not sw2.value():
		screen = (screen + 1) % 4
		sensor.old_bpm = -3
		darkmode = ui.darkmode
		color = not darkmode
		ui.oled.fill(color)

		while not sw2.value():
			pass

	# Change of screens
	if screen == 0:
		clock.clock_interface()
	elif screen == 1:
		clock.analog_clock_interface()
	elif screen == 2:
		ui.oled.fill(not ui.darkmode)
		ui.oled.text("Veuillez placer", 0, 4, ui.darkmode)
		ui.oled.text("votre doigt sur", 0, 16, ui.darkmode)
		ui.oled.text("le capteur afin", 0, 28, ui.darkmode)
		ui.oled.text("de calculer", 0, 40, ui.darkmode)
		ui.oled.text("votre BPM.", 0, 52, ui.darkmode)
		ui.oled.show()
		pass
	else:
		sensor.sensor()
	
