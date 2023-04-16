import time
import ui
import framebuf

from machine import ADC, Pin

global buffer, count_points, limit_points, mean, last_mean, last_mean_limit, last_heart_beat, draw_cursor, points_counter

adc = ADC(Pin('A0'))

# List of all the values of the sensor
buffer = []

# Counter of points and limit : we want to store a number of 'limit_points' points
count_points = 0
limit_points = 50

# Calculated mean of the points
mean = 0

# List of the lasts means of the value
last_mean = []
# We want to store a number of 'last_mean_limit' means in the last_mean
last_mean_limit = 50

# The last time the heart beat
last_heart_beat = 0

ssd_buffer = ui.ssd1306.SSD1306(10, 64, None)  # Init a "fake" SSD1306  only 10 pixels wide (1 for plot, 9 for "blank-ahead")
ssd_buffer_text = ui.ssd1306.SSD1306(32, 64, None)

draw_cursor = 0
points_counter = 0

def sensor():
    """
    Function that displays the plot of the sensor, calculate the BPM of the person and display it.
    """
    global buffer, count_points, limit_points, mean, last_mean, last_mean_limit, last_heart_beat, draw_cursor, points_counter

    # Set the good color depending on darkmode
    darkmode = ui.darkmode
    color = not darkmode

    val = adc.read_u16()

    # Reading value of the sensor
    buffer.append(val)
    # We add one value to the list so we add a point
    count_points += 1

    if count_points >= limit_points:
        # We calculate the mean of the points
        mean = sum(buffer) // limit_points
        # print("mean:", mean)
        # We pop the first value we know
        buffer.pop(0)
        # We have a point to count down
        count_points -= 1

        points_counter += 1
        if points_counter > 10:
            plt = int((mean % 6000) / 6000 * 60)  # This line still needs a bit of workout
            ssd_buffer.pixel(0, 62 - plt, not color)

            #### SMART SHOW ####
            # Draw the buffer of the fake screen on the real screen.
            ui.oled.write_cmd(ui.ssd1306.SET_COL_ADDR)  # "Here is the width of the buffer I'm gonna send you"
            ui.oled.write_cmd(draw_cursor)  # "You are going to draw the buffer from this column..."
            ui.oled.write_cmd(draw_cursor + 9)  # "... and it's gonna end at this column " (+ 9 because the fake buffer is 10 pixels wide)
            ui.oled.write_cmd(ui.ssd1306.SET_PAGE_ADDR)  # Same but for rows (not really rows, but "pages" = groups of 8 rows)
            ui.oled.write_cmd(0)
            ui.oled.write_cmd(7)
            ui.oled.write_data(ssd_buffer.buffer)  # "And here is the buffer:" but it's actually the buffer of the fake screen

            ssd_buffer.fill(color)  # Clear the fake screen buffer

            draw_cursor = (draw_cursor + 1) % 87
            points_counter = 0

    if len(last_mean) > last_mean_limit:
        last_mean.pop(0)
    last_mean.append(mean)

    ind_m = -1
    for m in last_mean:
        ind_m += 1

        if (time.ticks_ms() - last_heart_beat) > 200 and (mean - m) > 100:
            # Exchange new beats time
            start_heart_beat = last_heart_beat
            last_heart_beat = time.ticks_ms()
            # Calculus of the period between two heartbeats
            period_one_beat = last_heart_beat - start_heart_beat
            bpm = 60000 // period_one_beat
            if bpm < 150:
                print('bpm: ', bpm, 'mean:', mean, 'm:', m)

                # Writing the bpm
                ssd_buffer_text.fill(color)
                ssd_buffer_text.text("BPM", 0, 10, not color)
                ssd_buffer_text.text(str(bpm), 0, 25, not color)
                ui.draw(ui.empty_heart, 7, 40, zoom=2, screen=ssd_buffer_text)

                ui.oled.write_cmd(ui.ssd1306.SET_COL_ADDR)
                ui.oled.write_cmd(96)
                ui.oled.write_cmd(127)
                ui.oled.write_cmd(ui.ssd1306.SET_PAGE_ADDR)
                ui.oled.write_cmd(0)
                ui.oled.write_cmd(7)

                ui.oled.write_data(ssd_buffer_text.buffer)

def before_sensor():
    """
    Function to display a menu before the plot to explain operating instructions.
    """
    ui.oled.fill(not ui.darkmode)
    ui.oled.text("Veuillez placer", 0, 4, ui.darkmode)
    ui.oled.text("votre doigt sur", 0, 16, ui.darkmode)
    ui.oled.text("le capteur afin", 0, 28, ui.darkmode)
    ui.oled.text("de calculer", 0, 40, ui.darkmode)
    ui.oled.text("votre BPM.", 0, 52, ui.darkmode)
    ui.oled.show()
    
    