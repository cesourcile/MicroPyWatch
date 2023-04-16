
import machine
import ui
import pyb
import time
import random

# Switches
sw1 = pyb.Switch()
sw3 = pyb.Pin('SW3', machine.Pin.IN, machine.Pin.PULL_UP)

global ball_size, ball_x, ball_y, ball_speed_x, ball_speed_y, gamer_bar_size, gamer_x, gamer_y, gamer_speed_x, gamer_speed_y, computer_bar_size, computer_x, computer_y, computer_speed_x, score

# Initialisation of the variables of Pong
ball_size = 4
ball_x = 2
ball_y = 12
ball_speed_x = 2
ball_speed_y = 2

gamer_bar_size = (6, 25)
gamer_x = 2
gamer_y = 2
gamer_speed_x = 1

computer_bar_size = (6, 25)
computer_x = 2
computer_y = 120
computer_speed_x = 1

score = 0

def pong_interface():
	"""
	Function that display an interface where we can play Pong against a computer.
	"""
	global ball_size, ball_x, ball_y, ball_speed_x, ball_speed_y, gamer_bar_size, gamer_x, gamer_y, gamer_speed_x, gamer_speed_y, computer_bar_size, computer_x, computer_y, computer_speed_x, score

	# Set the good color depending on darkmode
	darkmode = ui.darkmode
	color = not darkmode

	ui.oled.fill(color)

	# Writing the name of the game and the current score
	text1 = 'PONG'
	ui.smart_text(ui.oled, text1, (128 - len(text1) * 8) // 2, 20, not color)
	ui.smart_text(ui.oled, str(score), (128 - len(str(score)) * 8) // 2, 30, not color)

	# PONG GAME -----------------------------------------------------------------------------------

	# Gamer

	ui.oled.fill_rect(gamer_y, gamer_x, gamer_bar_size[0], gamer_bar_size[1], not color)

	# Press SW3 : go to back
	if not sw3.value():
		if (gamer_x + gamer_speed_x) < (64 - gamer_bar_size[1]):
			gamer_x += gamer_speed_x

	# Press SW1 : go to up
	if sw1():
		if (gamer_x + gamer_speed_x) > 2:
			gamer_x -= gamer_speed_x

	# Ball and ball's movement

	ui.oled.fill_rect(ball_y, ball_x, ball_size, ball_size, not color)

	if (ball_x + ball_speed_x) > 64 - ball_size or (ball_x + ball_speed_x) < 0:
		ball_speed_x = - ball_speed_x
	else:
		ball_x += ball_speed_x
		
	if (ball_y + ball_speed_y) > 128 - ball_size - (2 + computer_bar_size[0]):
		ball_speed_y = - ball_speed_y

	# Is it touching the bar or not ?
	elif (ball_y == gamer_y + gamer_bar_size[0]):
		if (ball_x <= gamer_x + gamer_bar_size[1]) and (ball_x >= gamer_x - ball_size):
			ball_speed_y = - ball_speed_y
			ball_y += ball_speed_y
			score += 1
		else:
			game_over()
			time.sleep(3)

	else:
		ball_y += ball_speed_y

	# Computer bar

	ui.oled.fill_rect(computer_y, computer_x, computer_bar_size[0], computer_bar_size[1], not color)

	if (ball_x < computer_x + computer_x / 2) and (computer_x + computer_speed_x > 2):
		computer_x -= computer_speed_x
	elif (ball_x > computer_x - computer_x / 2) and (computer_x + computer_speed_x < 64 - computer_bar_size[1]):
		computer_x += computer_speed_x

	ui.oled.show()

def game_over():
	"""
	Function that display a Game Over interface.
	"""
	global ball_x, ball_y, ball_speed_x, ball_speed_y, gamer_x, gamer_y, score

	# Set the good color depending on darkmode
	darkmode = ui.darkmode
	color = not darkmode

	ui.oled.fill(color)

	# Game Over screen
	text1 = 'GAME OVER'
	text2 = 'Your score : %i' % (score)
	ui.smart_text(ui.oled, text1, (128 - len(text1) * 8) // 2, 30, not color)
	ui.smart_text(ui.oled, text2, (128 - len(text2) * 8) // 2, 40, not color)
	ui.oled.show()

	# Init parameters of Pong
	ball_x = random.randint(2, 62)
	ball_y = 12

	ball_speed_x = 2
	ball_speed_y = 2

	gamer_x = 2
	gamer_y = 2

	score = 0
