import machine
import ssd1306

# get data pins from LED screen
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
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
