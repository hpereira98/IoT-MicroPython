import dht
import ssd1306
import machine
import config
import urequests
import sys
import time
import network

def get_temperature_and_humidity():
    # assign sensor to respective pin
    dht11 = dht.DHT11(machine.Pin(config.DHT11_PIN))
    # measure the environment
    dht11.measure()
    # get the temperature and convert it to fahrenheit if needed
    temperature = dht11.temperature()
    if config.FAHRENHEIT:
        temperature = temperature * 9 / 5 + 32
    # return both the temperature and the humidity
    return temperature, dht11.humidity()

# send data to ThingSpeak channel
def log_data(temperature, humidity):
    print('Invoking log webhook')
    # set config variable values
    url = config.WEBHOOK_URL.format(temperature=temperature,
                                    humidity=humidity)
    # send request (ThingSpeak works with GET requests)
    response = urequests.get(url)
    if response.status_code < 400:
        print('Webhook invoked')
    else:
        print('Webhook failed')
        raise RuntimeError('Webhook failed')

# connect to wifi
def connect_wifi():
    # deactivate access point interface if active
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.isconnected():
        ap_if.active(False)
    # activate station interface if not active and connect to the wifi
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to WiFi...')
        sta_if.active(True)
        sta_if.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        # while not connected, wait
        while not sta_if.isconnected():
            time.sleep(1)
    print('Network config:', sta_if.ifconfig())

# blink LED 3 times when an error occurs
def show_error():
    led = machine.Pin(config.BLUE_LED_PIN, machine.Pin.OUT)
    # blink three times
    for i in range(3):
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
    # in the end stays on
    led.off()

def is_debug():
    debug = machine.Pin(config.DEBUG_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    if debug.value() == 0:
        print('Debug mode detected.')
        return True
    return False

def deepsleep():
    print('Going into deepsleep for {seconds} seconds...'.format(
        seconds=config.LOG_INTERVAL))
    machine.deepsleep(config.LOG_INTERVAL * 1000)

def display_temperature_and_humidity(temperature, humidity):
    i2c = machine.I2C(-1, scl=machine.Pin(config.DISPLAY_SCL_PIN),
                      sda=machine.Pin(config.DISPLAY_SDA_PIN), freq=40000)
    if 60 not in i2c.scan():
        raise RuntimeError('Cannot find display.')

    display = ssd1306.SSD1306_I2C(config.OLED_WIDTH, config.OLED_HEIGHT, i2c)
    display.fill(0)

    # '{:^16s}': centered in a field of 16 chars
    display.text('{:^16s}'.format('Temperature:'), 0, 0)
    display.text('{:^16s}'.format(str(temperature) + \
        ('F' if config.FAHRENHEIT else 'C')), 0, 16)

    display.text('{:^16s}'.format('Humidity:'), 0, 32)
    display.text('{:^16s}'.format(str(humidity) + '%'), 0, 48)

    # show for 10secs and then turn off
    display.show()
    # time.sleep(10)
    # display.poweroff()

def run():
    try:
        connect_wifi()
        temperature, humidity = get_temperature_and_humidity()
        log_data(temperature, humidity)
        display_temperature_and_humidity(temperature, humidity)
    except Exception as exc:
        sys.print_exception(exc)
        show_error()

    if not is_debug():
        deepsleep()

run()