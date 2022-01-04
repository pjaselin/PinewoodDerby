import time

import max7219.led as led

device = led.sevensegment()
device.write_text(deviceId=0, text="....")
time.sleep(10)
