from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import sevensegment
import RPi.GPIO as GPIO

# IR sensor GPIO pins
IR_BEAM_PIN1 = 17
IR_BEAM_PIN2 = 27

# Reed switch pin
REED_SWITCH_PIN = 18

# Define LED components
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=2, blocks_arranged_in_reverse_order=True)
seg = sevensegment(device)


# Callbacks

def break_beam_callback(pin):
    """Detects when an IR beam connected to the given pin is broken/unbroken"""
    if GPIO.input(pin):
        print("beam unbroken", pin)
    else:
        print("broken", pin)