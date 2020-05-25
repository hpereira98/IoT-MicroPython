import machine

# IMPORTANT!! THIS DOES NOT WORK ON ESP32, FOR THIS BOARD CHECK THE 2nd implementation

# 1st implementation: ESP8266

# get real time clock
rtc = machine.RTC()
# add trigger to wake from deepsleep
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
# configure when the alarm goes off (one minute in this case)
rtc.alarm(rtc.ALARM0, 60 * 1000)

# 2nd implementation: ESP32
# sets the board to go into deepsleep and wake after 1 minute
machine.deepsleep(60 * 1000)