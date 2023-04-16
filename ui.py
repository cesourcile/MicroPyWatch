# USER INTERFACE 

import machine
import pyb
import ssd1306

# Display I2C
i2c = machine.SoftI2C(scl=machine.Pin('D14'), sda=machine.Pin('D15'), freq=3600000)
i2c.scan()
# Display of 128*64 pixels
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# MATRIX

# Heart : empty and full

empty_heart = [
	[ 1, 0, 0, 1, 0, 0, 1],
	[ 0, 1, 1, 0, 1, 1, 0],
	[ 0, 1, 1, 1, 1, 1, 0],
	[ 0, 1, 1, 1, 1, 1, 0],
	[ 1, 0, 1, 1, 1, 0, 1],
	[ 1, 1, 0, 1, 0, 1, 1],
	[ 1, 1, 1, 0, 1, 1, 1] ]

full_heart = [
	[ 1, 0, 0, 1, 0, 0, 1],
	[ 0, 0, 0, 0, 0, 0, 0],
	[ 0, 0, 0, 0, 0, 0, 0],
	[ 0, 0, 0, 0, 0, 0, 0],
	[ 1, 0, 0, 0, 0, 0, 1],
	[ 1, 1, 0, 0, 0, 1, 1],
	[ 1, 1, 1, 0, 1, 1, 1]
]

# Numbers

zero = [
	[ 1, 1, 1, 0, 0, 1, 1, 1],
	[ 1, 1, 0, 1, 1, 0, 1, 1],
	[ 1, 1, 0, 1, 1, 0, 1, 1],
	[ 1, 1, 0, 1, 1, 0, 1, 1],
	[ 1, 1, 0, 1, 1, 0, 1, 1],
	[ 1, 1, 0, 1, 1, 0, 1, 1],
	[ 1, 1, 0, 1, 1, 0, 1, 1],
	[ 1, 1, 1, 0, 0, 1, 1, 1]
]

one = [
	[ 1, 1, 1, 1, 0, 1, 1, 1],
	[ 1, 1, 1, 0, 0, 1, 1, 1],
	[ 1, 1, 0, 1, 0, 1, 1, 1],
	[ 1, 1, 1, 1, 0, 1, 1, 1],
	[ 1, 1, 1, 1, 0, 1, 1, 1],
	[ 1, 1, 1, 1, 0, 1, 1, 1],
	[ 1, 1, 1, 1, 0, 1, 1, 1],
	[ 1, 1, 1, 0, 0, 0, 1, 1]]

two = [
	[ 1, 1, 1, 0, 0, 1, 1, 1],
	[ 1, 1, 0, 1, 1, 0, 1, 1],
	[ 1, 1, 0, 1, 1, 0, 1, 1],
	[ 1, 1, 1, 1, 1, 0, 1, 1],
	[ 1, 1, 1, 1, 0, 1, 1, 1],
	[ 1, 1, 1, 0, 1, 1, 1, 1],
	[ 1, 1, 0, 1, 1, 1, 1, 1],
	[ 1, 1, 0, 0, 0, 0, 1, 1]]

three = [
	[ 1, 1, 1, 0, 0, 1, 1, 1],
	[ 1, 1, 0, 1, 1, 0, 1, 1],
	[ 1, 1, 0, 1, 1, 0, 1, 1],
	[ 1, 1, 1, 1, 0, 1, 1, 1],
	[ 1, 1, 1, 1, 1, 0, 1, 1],
	[ 1, 1, 1, 1, 1, 0, 1, 1],
	[ 1, 1, 0, 1, 1, 0, 1, 1],
	[ 1, 1, 1, 0, 0, 1, 1, 1]
]

four = [
	[ 1, 1, 1, 1, 1, 0, 1, 1],
	[ 1, 1, 1, 1, 0, 0, 1, 1],
	[ 1, 1, 1, 0, 1, 0, 1, 1],
	[ 1, 1, 0, 1, 1, 0, 1, 1],
	[ 1, 1, 0, 0, 0, 0, 0, 1],
	[ 1, 1, 1, 1, 1, 0, 1, 1],
	[ 1, 1, 1, 1, 1, 0, 1, 1],
	[ 1, 1, 1, 1, 1, 0, 1, 1]
]

five = [
    [1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 0, 0, 1, 1, 1],
]

six = [
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
]

seven = [
    [1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1],
]

eight = [
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
]

nine = [
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
]

numbers = {
	0: zero,
	1: one,
	2: two,
	3: three,
	4: four,
	5: five,
	6: six,
	7: seven,
	8: eight,
	9: nine
}

# Pounctuation

colon = [
	[ 1, 1, 1, 1],
	[ 1, 1, 1, 1],
	[ 1, 1, 1, 1],
	[ 1, 0, 0, 1],
	[ 0, 0, 0, 0],
	[ 0, 0, 0, 0],
	[ 1, 0, 0, 1],
	[ 1, 1, 1, 1],
	[ 1, 1, 1, 1],
	[ 1, 0, 0, 1],
	[ 0, 0, 0, 0],
	[ 0, 0, 0, 0],
	[ 1, 0, 0, 1],
	[ 1, 1, 1, 1],
	[ 1, 1, 1, 1],
	[ 1, 1, 1, 1]
]

point = [
	[ 0, 0],
	[ 0, 0]
]


global darkmode

# DARKMODE

sw = pyb.Switch()
darkmode = False

def change_mode():
	"""
	Function that change the mode from light to dark when pressing SW1.
	"""
	global darkmode
	if sw():
		darkmode = not darkmode
		while sw():
			pass

# DRAW MATRIX

def draw(matrix, x, y, zoom=1, screen=oled):
	"""
	Function that draws the pixels based on a matrix.
	
	Parameters :
		matrix : matrix that we want to display
		x - x coordonnates of the matrix
		y - y coordonnates of the matrix
		zoom - zoom of the matrix (1 per default)
		screen - display we want to write on (oled by default)
	"""
	for ind_y, i in enumerate(matrix):
		for ind_x, j in enumerate(i):
			for zx in range(zoom):
				for zy in range(zoom):
					if darkmode == True:
						screen.pixel(x + zoom * ind_x + zx, y + zoom * ind_y + zy, not j)
					else:
						screen.pixel(x + zoom * ind_x + zx, y + zoom * ind_y + zy, j)

# DISPLAY TEXT PART

def smart_text(oled, new, x, y, c):
	"""
	Function that helps the writing of new text on a display.
	It compares the old display with the new and just change the color of the pixels that are going to change 
	instead of rewriting all of the pixels.
	
	Parameters :
		oled - display we want to write on
		new - text we want to write
		x - x coordonnates of the text
		y - y coordonnates of the text
		c - color of the text 
	"""
	
	global old_text
	CHAR_WIDTH = 8
	CHAR_HEIGHT = 8
	
	try:
		old_text
	except:
		old_text = {}
		
	cr = y * oled.width + x
	if cr not in old_text.keys():
		old_text[cr] = ''

	change_pos = []
	for cur, (a, b) in enumerate(zip(new, old_text[cr])):
		if a != b:
			oled.fill_rect(x + CHAR_WIDTH * cur, y, CHAR_WIDTH, CHAR_HEIGHT, not c)
			
	old_text[cr] = new
	oled.text(new, x, y, c)

