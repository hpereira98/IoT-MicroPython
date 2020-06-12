# Using https://github.com/peterhinch/micropython-font-to-py:
# import the font and the writer code
import freesans20
import writer

# create a writer instance
font_writer = writer.Writer(display, freesans20)

# set writing position
font_writer.set_textpos(0, 0)

# write some text!
font_writer.printstring("hello")

# calculate how many pixels wide a text is
len = font_writer.stringlen("hello")