import time

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import sevensegment
from luma.led_matrix.device import max7219

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial) # cascaded=2
seg = sevensegment(device)

seg.text = "12.34"

time.sleep(10)