import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def reed_switch_cb(pin):
    if GPIO.input(pin):
        print("Open")
        # start the internal timer

GPIO.add_event_detect(18, GPIO.BOTH, callback=lambda _: reed_switch_cb(18))

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
    # GPIO.setup(list(pins.values()), GPIO.OUT)
    # GPIO.output(list(pins.values()), GPIO.LOW)
except:
    print("Goodbye")
    GPIO.cleanup()