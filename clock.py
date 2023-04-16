# CLOCK 

import machine
import ui
from ds3231 import DS3231
import math

# Initialisation of the real-time clock
rtc = machine.RTC()
rtc.datetime((2022, 02, 28, 2, 15, 17, 0, 0))

# Preparing DS3231 RTC module
rtc_vcc_pin = machine.Pin('D0', machine.Pin.OUT) # Turning on DS3231 RTC (since it's not plugged on 5v or VCC)
rtc_vcc_pin.value(1)
rtc_i2c = machine.SoftI2C(sda=machine.Pin('D6'), scl=machine.Pin('D7'))
ds = DS3231(rtc_i2c)
try:
	rtc.datetime(ds.datetime())
except OSError: # RTC module unplugged
	print ('RTC module not detected')

# Dictionnary of each days
days_name = {0: 'dimanche',
			 1: 'lundi',
			 2: 'mardi',
			 3: 'mercredi',
			 4: 'jeudi',
			 5: 'vendredi',
			 6: 'samedi'}

# Global variables
global x_deb, y, z
x_deb = 12
z = 2
y = 24

def traductor_str_matrix(hour, minute, second):
	"""
	Function that collects all the necessaries matrices to display the hour.
	
	Parameters :
		hour - hour number
		minute - minute number
		second - second number
	"""
	matrix = []
	d = hour // 10, hour % 10, minute // 10, minute % 10, second // 10, second % 10

	for i in d:
		matrix.append(ui.numbers[i])
	return matrix

def rotation(x_center, y_center, angle, clock_x=64, clock_y=32):
	"""
	Function that calculates the rotation of the hands of the clock.
	
	Parameters :
		x_center - Center of the hand of the clock
		y_center - Represents the radius of the hand of the clock
		angle - Degree of the hand of the clock
		clock_x - Center of the clock (64 per default)
		clock_y - Radius of the clock (32 per default)
	"""

	rad = math.radians(angle)
	x_center -= clock_x
	y_center -= clock_y

	xCos = x_center * math.cos(rad)
	yCos = y_center * math.cos(rad)

	xSin = x_center * math.sin(rad)
	ySin = y_center * math.sin(rad)

	x_direction = xCos - ySin + clock_x
	y_direction = xSin + yCos + clock_y

	return [int(x_direction), int(y_direction)]

def clock_interface():
	"""
	Function that display an interface of digital clock.
	"""
	global x_deb, y, z

	# Set the good color depending on darkmode
	darkmode = ui.darkmode
	color = not darkmode

	ui.oled.fill(color)

	# Recuperation of the date
	date = rtc.datetime()
	(year, month, day, weekday, hour, minute, second, subseconds) = date
	weekday %= 7

	# Preparation of text
	text1 = '%02d/%02d/%02d' % (day, month, year)
	text2 = '%02d : %02d : %02d' % (hour, minute, second)
	text3 = 'On est ' + days_name[weekday]

	# Display of the text
	ui.smart_text(ui.oled, text1, (128 - len(text1) * 8) // 2, 44, not color)
	ui.smart_text(ui.oled, days_name[weekday], 5, 5, not color)

	# Display of the hour
	mat = traductor_str_matrix(hour, minute, second)

	ui.draw(mat[0], x_deb, y, z)
	ui.draw(mat[1], x_deb + 8 * z, y, z)
	ui.draw(ui.colon, x_deb + 8 * z * 2, y)
	ui.draw(mat[2], x_deb + 8 * z * 2 + 4, y, z)
	ui.draw(mat[3], x_deb + 8 * z * 3 + 4, y, z)
	ui.draw(ui.colon, x_deb + 8 * z * 4 + 4, y)
	ui.draw(mat[4], x_deb + 8 * z * 4 + 8, y, z)
	ui.draw(mat[5], x_deb + 8 * z * 5 + 8, y, z)

	ui.oled.show()

def analog_clock_interface():
	"""
	Function that display an interface of analog clock.
	"""

	# Set the good color depending on darkmode
	darkmode = ui.darkmode
	color = not darkmode

	ui.oled.fill(color)
	
	# recuperation of the date
	date = rtc.datetime()
	(year, month, day, weekday, hour, minute, second, subseconds) = date
	weekday %= 7

	# Calculus of the different degrees of the hands of the clocks
	hour_degree = (hour + minute / 60) * 30
	minute_degree = minute * 6
	second_degree = second * 6

	# Parameteres to determinate where is the clock
	clock_center_x = 35
	clock_center_y = 32

	# Drawing of the circle of the analog clock
	for degree in range(0, 12):
		ui.draw(ui.point, rotation(clock_center_x, 4, 30 * degree, clock_x=clock_center_x)[0],
				rotation(clock_center_x, 4, 30 * degree, clock_x=clock_center_x)[1])

	# Drawing of the center of the clock
	clock_center = ui.oled.pixel(clock_center_x, clock_center_y, not color)
	
	# Drawing of the second hand 
	second_line = ui.oled.line(clock_center_x, clock_center_y,
							   rotation(clock_center_x, 4, second_degree, clock_x=clock_center_x)[0],
							   rotation(clock_center_x, 4, second_degree, clock_x=clock_center_x)[1], not color)
	
	# Drawing of the minute hand
	minute_line = ui.oled.line(clock_center_x, clock_center_y,
							   rotation(clock_center_x, 8, minute_degree, clock_x=clock_center_x)[0],
							   rotation(clock_center_x, 8, minute_degree, clock_x=clock_center_x)[1], not color)
	
	# Drawing of the hour hand
	hour_line = ui.oled.line(clock_center_x, clock_center_y,
							 rotation(clock_center_x, 16, hour_degree, clock_x=clock_center_x)[0],
							 rotation(clock_center_x, 16, hour_degree, clock_x=clock_center_x)[1], not color)
	
	# Preparation of text
	text1 = '%02d/%02d' % (day, month)
	text2 = '%02d' % (year)

	# Display of the text
	ui.smart_text(ui.oled, days_name[weekday], 64 + (64 - 8*len(days_name[weekday])) // 2, 13, not color)
	ui.smart_text(ui.oled, text1, 64 + (64 - 8*len(text1)) // 2, 28, not color)
	ui.smart_text(ui.oled, text2, 64 + (64 - 8*len(text2)) // 2, 43, not color)

	ui.oled.show()
