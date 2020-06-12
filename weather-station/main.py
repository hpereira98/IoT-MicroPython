import dht
import ssd1306
import machine
import config
import urequests
import sys
import time
import network
import framebuf
import writer
import freesans20

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

def load_image(filename):
    with open(filename, 'rb') as f:
        f.readline()
        f.readline()
        width, height = [int(v) for v in f.readline().split()]
        data = bytearray(f.read())
    return framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)

def display_temperature_and_humidity(temperature, humidity):
    i2c = machine.I2C(scl=machine.Pin(config.DISPLAY_SCL_PIN), sda=machine.Pin(config.DISPLAY_SDA_PIN))
    if 60 not in i2c.scan():
        raise RuntimeError('Cannot find display.')

    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    font_writer = writer.Writer(display, freesans20)

    temperature_pbm = load_image('temperature.pbm')
    units_pbm = load_image('fahrenheit.pbm') if config.FAHRENHEIT \
        else load_image('celsius.pbm')
    humidity_pbm = load_image('humidity.pbm')
    percent_pbm = load_image('percent.pbm')

    display.fill(0)
    display.rect(0, 0, 128, 64, 1)
    display.line(64, 0, 64, 64, 1)
    display.blit(temperature_pbm, 24, 4)
    display.blit(humidity_pbm, 88, 4)
    display.blit(units_pbm, 28, 52)
    display.blit(percent_pbm, 92, 52)

    text = '{:.1f}'.format(temperature)
    textlen = font_writer.stringlen(text)
    font_writer.set_textpos((64 - textlen) // 2, 30)
    font_writer.printstring(text)

    text = '{:.1f}'.format(humidity)
    textlen = font_writer.stringlen(text)
    font_writer.set_textpos(64 + (64 - textlen) // 2, 30)
    font_writer.printstring(text)

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