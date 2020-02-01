import sys
sys.path.insert(1, 'lib')
from waveshare_epd import epd2in9

epd = epd2in9.EPD()
epd.init(epd.lut_full_update)
epd.Clear(0XFF)


