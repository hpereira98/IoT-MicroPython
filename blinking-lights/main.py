import machine
import time

LED_PIN = 2 # In-Built LED
BUTTON_PIN = 19  # D19

def blink():
    # define 'led' as the pin number 2 and as an Output pin
    led = machine.Pin(LED_PIN, machine.Pin.OUT)
    # define 'button' as the pin number 19 and as an Input pin. Also, we will activate the Pull-Up resistor inside the pin.
    button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    # while the button is not pressed, the light will be on and off each 0.5 seconds
    while button.value():
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
    # when the button is pressed, the led stays on
    led.on()

blink()