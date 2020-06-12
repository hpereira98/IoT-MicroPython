import machine
import ssd1306
import framebuf

# get data pins from LED screen
# ESP32
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
# ESP8266
# i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
# scan LED to see if it is connected
i2c.scan()

# declare display variable, from the SSD1306 screen
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# clear screen: set all pixels to 0 (black)
display.fill(0)

# print text on screen:
# X: value of 0 means the left border, and a value of 127 means the right border
# Y: vertical position and it goes from 0 for the top of the screen to 63 for the bottom
display.text('Hello', 0, 0)
display.text('from', 0, 16)
display.text('MicroPython!', 0, 32)
# show the text written above
display.show()

# draw a rectangle: left, top, width, height, color
display.fill(0)
display.rect(0, 0, 128, 64, 1)
display.show()

# draw a line: point coordinates and color
display.line(64, 0, 64, 64, 1)
display.show()

# draw a single pixel: coordinates and color. if no color, the function returns the color of that pixel
display.pixel(5, 10, 1)
display.show()

# function that loads a PBM image file:
# P4 : indicates its a PBM file
# # Description : image desc
# <width> <height> : width and height of the image
# <binary image data>
def load_image(filename):
    with open(filename, 'rb') as f:
        # ignore first two lines
        f.readline()
        f.readline()
        # parse width and height
        width, height = [int(v) for v in f.readline().split()]
        # get binary image data
        data = bytearray(f.read())
        # read the image to a framebuffer in order to draw it on the screen, using the MONO_HSLB format
    return framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)

# get image
image = load_image('temperature.pbm')
# display it in the screen using blit: bit block transfer
display.blit(image, 24, 4)
