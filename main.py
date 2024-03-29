"""
Main script for Pinewood Derby Timer

Initialization:
- Set all digits to show "8" at start to check fit

Procedure:
- On reed switch open:
    - Store current time
    - Set position counter to 0
- On IR beam break:
    - Get time difference and show
- On reed switch closed:
    - Reset text to all "-"

"""
from time import perf_counter, sleep
from collections import OrderedDict

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import sevensegment
import RPi.GPIO as GPIO
from loguru import logger
import socketio

# IR sensor GPIO pins
IR_BEAM_PIN1 = 17
IR_BEAM_PIN2 = 27

# Reed switch pin
REED_SWITCH_PIN = 18

# Define LED components
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=2, blocks_arranged_in_reverse_order=True)
display = sevensegment(device)

# clear display at initialization
display.text = "8"*16

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(REED_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(REED_SWITCH_PIN, GPIO.BOTH, callback=lambda _: reed_switch_cb(REED_SWITCH_PIN))

# create a Socket.IO server
sio = socketio.AsyncServer()

# wrap with ASGI application
app = socketio.ASGIApp(sio)

class Lane:
    def __init__(self, pin=None, lane=None) -> None:
        self.pin = pin
        self.lane = lane
        self.time = "----"
        self.position = "-"
        self.is_active = False

    def start(self, start_time):
        self._start_time = start_time
        self.time = "----"
        self.position = "-"
        self.is_active = True
    
    def finish(self, start_time, position):
        if not self.is_active:
            return
        abs_time = perf_counter() - start_time
        print(abs_time)
        # If the timer exceeds 9999 seconds, show 9999, otherwise store
        # the time rounded to 4 digits
        # if abs_time >= 9999:
            # self._finish_time = "9999"
        # else:
        self._finish_time = perf_counter() #'{:g}'.format(float('{:.4g}'.format(abs_time))).zfill(4)
        # Store the given position
        self.position = str(position)
        self.is_active = False
        # send completion to web app
        sio.emit('my event', {'data': 'foobar'})
        return
    
    def time(self):
        abs_time = 
        return '{:g}'.format(float('{:.4g}'.format(abs_time))).zfill(4)
        
    def status(self):
        return f"{self.time}{self.position}"


class RaceMonitor:
    def __init__(self):
        self.num_lanes = 0
        self._register = OrderedDict()
        self._start_time = None
        self._position = 1
        self._race_active = False

    def register_lane(self, pin):
        if self.num_lanes not in self._register:
            self._register[pin] = Lane(pin, self.num_lanes)
            self.num_lanes += 1
            # Set up the GPIO for the IR sensors for this lane
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=lambda _: break_beam_cb(pin))
    
    def display_status(self):
        display_times = ""
        display_positions = ""
        for lane in self._register.values():
            display_times += lane.time
            display_positions += lane.position
        print(display_times + display_positions)
        display.text = display_times + display_positions
        return
    
    def start_race(self):
        # Record the start time start time
        self._start_time = perf_counter()
        self._race_active = True
        for lane in self._register.values():
            lane.start()
        logger.info("Start race")
    
    def reset_race(self):
        # Reset the position counter
        self._position = 1
        logger.info("Reset race")
    
    def finish(self, pin):
        # Log the finish time and position for the given lane/pin
        self._register[pin].finish(self._start_time, self._position)
        logger.info(f"Pin {pin} finished with {self._register[pin].__dict__}")
        # Increment position counter
        self._position += 1


monitor = RaceMonitor()
monitor.register_lane(IR_BEAM_PIN1)
monitor.register_lane(IR_BEAM_PIN2)


# GPIO callbacks
def reed_switch_cb(pin):
    """Detects when the reed switch is open/closed and responds accordingly"""
    global monitor
    if GPIO.input(pin):
        # Start the race
        monitor.start_race()
    else:
        monitor.reset_race()

def break_beam_cb(pin):
    """Detects when an IR beam connected to the given pin is broken
    i.e. the car has crossed the finish line"""
    global monitor
    if not GPIO.input(pin):
        # Store race finish information for this lane/pin
        monitor.finish(pin)

try:
    while True:
        monitor.display_status()
        sleep(0.5)
except Exception as e:
    print(e)
    print("Goodbye")
    GPIO.cleanup()