import RPi.GPIO as GPIO
import time
from random import randint

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

global_val = 0

def reed_switch_cb(pin, test_val):
    if GPIO.input(pin):
        global_val = randint(0,100)
        print("Open")
        # start the internal timer
    else:
        print("Closed")
        # reset the timer maybe, need to see what gets shared across callbacks

GPIO.add_event_detect(18, GPIO.BOTH, callback=lambda _: reed_switch_cb(18, global_val))

# while True:
#     input_value = GPIO.input(18)
#     if input_value:
#         print("Open")
#     else:
#         print("Closed")
#     time.sleep(.1)
try:
    while True:
        # print(GPIO.input(BEAM_PIN3))
        time.sleep(0.5)
        # global_val = randint(0,100)
        print(global_val)
    # GPIO.setup(list(pins.values()), GPIO.OUT)
    # GPIO.output(list(pins.values()), GPIO.LOW)
except:
    print("Goodbye")
    GPIO.cleanup()