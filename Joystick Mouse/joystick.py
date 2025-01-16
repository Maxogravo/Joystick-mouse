import time
import board
import analogio
import digitalio
import usb_hid
from adafruit_hid.mouse import Mouse


mouse = Mouse(usb_hid.devices)


x_axis = analogio.AnalogIn(board.A0)
y_axis = analogio.AnalogIn(board.A1)


button = digitalio.DigitalInOut(board.GP22)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

DEAD_ZONE = 2000  
SCALE_FACTOR = 6553.6  

def get_scaled_value(analog_in):
    raw_value = analog_in.value
    if abs(raw_value - 32768) < DEAD_ZONE:  
        return 0
    return int((raw_value - 32768) / SCALE_FACTOR) 

while True:
   
    x_movement = get_scaled_value(x_axis)
    y_movement = get_scaled_value(y_axis)

    
    mouse.move(x=x_movement, y=y_movement)


    if not button.value:
        mouse.click(Mouse.LEFT_BUTTON)
        time.sleep(0.2)  

    time.sleep(0.01)  
