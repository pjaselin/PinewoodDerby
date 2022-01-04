import multiprocessing as mp

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import sevensegment

from .enum import TrackEvent

# establish connection with max7219 array using luma library
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)
seg = sevensegment(device)

# initialize track timing processes and assign ir sensor to each one
# - start timer in each process when reed switch opens
# - when IR sensor closes, stop the loop and report the time back to the main event loop
# - report each time and the position to the display

def display_to_led(message_dict):
    """"function to take the dictionary of information we want to show and convert it to 
    a single string for the LED array"""
    text_to_display = ""
    for track in message_dict:
        text_to_display += text_to_display[track]["position"]
        text_to_display += text_to_display[track]["time"]
    seg.text = text_to_display

# set the defaul/min car position
car_position = 1

# set the default LED messages
display_messages = {track: dict(position="-", time="----") for track in ["track1", "track2"]}
display_to_led(display_messages)

# set the main event queue
main_queue = mp.Queue()

while True:
    # start race when reed switch opens
    while True:
        # get info from queue
        event = main_queue.get()
        if event == TrackEvent.FINISHED:
            # show time on corresponding display
            pass
        elif event == TrackEvent.ERROR:
            # show error message on display
            pass
    