import sys
sys.path.insert(1, 'lib')
from waveshare_epd import epd2in9
from PIL import Image,ImageDraw,ImageFont

class DisplayController:
    def __init__(self):
        # Initialise epd
        self.epd = epd2in9.EPD()
        self.epd.init(self.epd.lut_full_update)
        self.epd.Clear(0XFF)

        self.midpoint = (self.epd.height // 2, self.epd.width // 2)

        self.font = ImageFont.truetype('Font.ttc', 36)


    def display_txt(self, msg, centred = True):
        h_image = Image.new('1', (self.epd.height, self.epd.width), 255)
        draw = ImageDraw.Draw(h_image)
        text_size = draw.textsize(msg, self.font)

        if centred:
            x = self.midpoint[0] - (text_size[0] // 2)
            y = self.midpoint[1] - (text_size[1] // 2)
        else:
            x = 0
            y = 0
    
        draw.text((x,y), msg, font = self.font, fill = 0)

        self.epd.display(self.epd.getbuffer(h_image))

