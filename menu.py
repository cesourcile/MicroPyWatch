import machine
import ui
import pyb

# Switches
sw2 = pyb.Pin('SW2', machine.Pin.IN, machine.Pin.PULL_UP)
sw3 = pyb.Pin('SW3', machine.Pin.IN, machine.Pin.PULL_UP)

global options, chosed_option

# All of the menu's options
# On 0 : digital clock interface
# # On 1 : analog clock interface
# # On 2 : sensor plot
# # On 3 : game
options = {
    0: ["digital clock", 10, 4, 2],
    1: ["analog clock", 10, 20, 18],
    2: ["heartbeat", 10, 36, 34],
    3: ["game", 10, 52, 50]
}

chosed_option = 0 # Number of the option in dark in the menu mode

def menu_interface():
    """
    Function that display the menu's interface.
    """
    global options, chosed_option

    print ('Going into menu')

    while True:

        # Set the good color depending on darkmode
        ui.change_mode()
        darkmode = ui.darkmode
        color = not darkmode
        ui.oled.fill(color)

        # Change options by pressing SW3
        number_of_options = len(options)
        if not sw3.value():
            while not sw3.value():
                pass
            chosed_option = (chosed_option + 1) % number_of_options
            print(chosed_option)

        # Display of the menu options
        rect_x_size = 12
        rect_y_size = 112
        for key, val in options.items():
            if key == chosed_option:
                ui.oled.fill_rect(8, val[3], rect_y_size, rect_x_size, not color)
                ui.smart_text(ui.oled, val[0], val[1], val[2], color)
            else:
                ui.oled.rect(8, val[3], rect_y_size, rect_x_size, not color)
                ui.smart_text(ui.oled, val[0], val[1], val[2], not color)

        # Choose an option by pressing SW2
        if not sw2.value():
            while not sw2.value():
                pass
            
            return(chosed_option)

        ui.oled.show()
