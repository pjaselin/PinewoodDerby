
import RPi.GPIO as GPIO
import time

BEAM_PIN = 17 #27
BEAM_PIN2 = 27
# BEAM_PIN3 = 18


def start_gate_callback(pin):
    if GPIO.input(pin) == GPIO.HIGH:
        print("race started")
    else:
        print("race waiting")


def break_beam_callback(pin):
    if GPIO.input(pin):
        print("beam unbroken", pin)
    else:
        print("broken", pin)

GPIO.setmode(GPIO.BCM)

GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BEAM_PIN, GPIO.BOTH, callback=lambda _: break_beam_callback(BEAM_PIN))

GPIO.setup(BEAM_PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BEAM_PIN2, GPIO.BOTH,  callback=lambda _: break_beam_callback(BEAM_PIN2))


# GPIO.setup(BEAM_PIN3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.add_event_detect(BEAM_PIN3, GPIO.BOTH,  callback=lambda _: start_gate_callback(BEAM_PIN3))

# message = input("Press enter to quit\n\n")

try:
    while True:
        # print(GPIO.input(BEAM_PIN3))
        time.sleep(0.5)
    # GPIO.setup(list(pins.values()), GPIO.OUT)
    # GPIO.output(list(pins.values()), GPIO.LOW)
except:
    print("Goodbye")
    GPIO.cleanup()