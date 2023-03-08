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

def clock_interface():

	darkmode = ui.darkmode
	color = not darkmode

	ui.oled.fill(color)
	
	date = rtc.datetime()
	(year, month, day, weekday, hour, minute, second, subseconds) = date

	mat = traductor_str_matrix(hour, minute, second)

	text1 = '%02d/%02d/%02d' % (day, month, year)
	text2 = '%02d : %02d : %02d' % (hour, minute, second)
	text3 = 'On est ' + days_name[weekday]

	# str(hour).zpad(2) + " : " + str(minute).zpad(2) + " : " + str(second).zpad(2)

	#ui.smart_text(ui.oled, text1, 27, 10, 0)
	#ui.smart_text(ui.oled, text2, 19, 25, 0)
	ui.smart_text(ui.oled, text1, ( 128 - len(text1) *8 ) // 2, 44, not color)
	ui.smart_text(ui.oled, days_name[weekday], 5, 5, not color)

	#def draw(matrix, x, y, zoom=1)
	x_deb = 12
	z = 2
	y = 24

	# Affichage (le bon)
	ui.draw(mat[0], x_deb, y, z)
	ui.draw(mat[1], x_deb + 8*z, y, z)
	ui.draw(ui.colon, x_deb + 8*z*2, y)
	ui.draw(mat[2], x_deb + 8*z*2 + 4, y, z)
	ui.draw(mat[3], x_deb + 8*z*3 + 4, y, z)
	ui.draw(ui.colon, x_deb + 8*z*4 + 4, y)
	ui.draw(mat[4], x_deb + 8*z*4 + 8, y, z)
	ui.draw(mat[5], x_deb + 8*z*5 + 8, y, z)

	#ui.oled.rect(0, 0, 128, 64, 0)
	#ui.oled.rect(5, 5, 118, 54, 1)
	#ui.oled.rect(10, 20, 108, 24, 1)

	ui.oled.show()
	
def traductor_str_matrix(hour, minute, second):
	matrix = []
	d = hour // 10, hour % 10, minute // 10, minute % 10, second // 10, second % 10

	for i in d:
		matrix.append(ui.numbers[i])

	return matrix

def rotation(x_center, y_center, angle, clock_x=64, clock_y=32):

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

def analog_clock_interface():

	darkmode = ui.darkmode
	color = not darkmode

	ui.oled.fill(color)

	date = rtc.datetime()
	(year, month, day, weekday, hour, minute, second, subseconds) = date

	hour_degree = (hour + minute / 60) * 30
	minute_degree = minute * 6
	second_degree = second * 6

	clock_center_x = 35
	clock_center_y = 32

	for degree in range(0, 12):
		ui.draw(ui.point, rotation(clock_center_x, 4, 30 * degree, clock_x=clock_center_x)[0],
				rotation(clock_center_x, 4, 30 * degree, clock_x=clock_center_x)[1])


	clock_center = ui.oled.pixel(clock_center_x, clock_center_y, not color)
	second_line = ui.oled.line(clock_center_x, clock_center_y,
							   rotation(clock_center_x, 4, second_degree, clock_x=clock_center_x)[0],
							   rotation(clock_center_x, 4, second_degree, clock_x=clock_center_x)[1], not color)
	minute_line = ui.oled.line(clock_center_x, clock_center_y,
							   rotation(clock_center_x, 8, minute_degree, clock_x=clock_center_x)[0],
							   rotation(clock_center_x, 8, minute_degree, clock_x=clock_center_x)[1], not color)
	hour_line = ui.oled.line(clock_center_x, clock_center_y,
							 rotation(clock_center_x, 16, hour_degree, clock_x=clock_center_x)[0],
							 rotation(clock_center_x, 16, hour_degree, clock_x=clock_center_x)[1], not color)

	text1 = '%02d/%02d' % (day, month)
	text2 = '%02d' % (year)


	ui.smart_text(ui.oled, days_name[weekday], 64 + (64 - 8*len(days_name[weekday])) // 2, 13, not color)
	ui.smart_text(ui.oled, text1, 64 + (64 - 8*len(text1)) // 2, 28, not color)
	ui.smart_text(ui.oled, text2, 64 + (64 - 8*len(text2)) // 2, 43, not color)

	ui.oled.show()
