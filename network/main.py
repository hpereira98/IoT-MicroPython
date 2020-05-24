import network
import config
import urequests
import time
import sys
import machine

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

# call the IFTTT WebHook
def call_webhook():
    print('Invoking webhook')
    # post request
    response = urequests.post(config.REQUEST_URL, json={'value1': config.BUTTON_ID})
    # print success if the response code is not an error code or empty
    if response is not None and response.status_code < 400:
        print('Webhook invoked with success')
    # else print that it failed
    else:
        print('Webhook failed')
        # throw/raise and exception
        raise RuntimeError('Webhook failed')

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
    led.on()

# run both functions above
# def run():
#     try:
#         connect_wifi()
#         call_webhook()
#     # catch exception and blink lights
#     except Exception as exc:
#         sys.print_exception(exc)
#         show_error()


# set the board to the deep sleep state. press the reset button to wake it
# machine.deepsleep()
# get reset info:
# PWRON_RESET: powered for the first time
# HARD_RESET: pressing the reset button
# WDT_RESET: watchdog timer reset, if the system crashes or fails
# DEEPSLEEP_RESET: reset after deep sleep state
# SOFT_RESET: ctrl-D reset in REPL
# machine.reset_cause()

# new version of run that only calls the webhook if reset from deep sleep state
# def run():
#     try:
#         if machine.reset_cause() == machine.DEEPSLEEP_RESET:
#             connect_wifi()
#             call_webhook()
#     except Exception as exc:
#         sys.print_exception(exc)
#         show_error()
#     machine.deepsleep()

# if debug pin is off (0), it activates debug mode
def is_debug():
    debug = machine.Pin(config.DEBUG_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    if debug.value() == 0:
        print('Debug mode detected.')
        return True
    return False

# only enters in deep sleep state if debug mode is off. will loop and call the webhook every 20secs
def run():
    try:
        # calls web hook only when waking up from deepsleep state
        if machine.reset_cause() == machine.DEEPSLEEP_RESET:
            connect_wifi()
            call_webhook()
    except Exception as exc:
        sys.print_exception(exc)
        show_error()

    if not is_debug():
        # goes into deepsleep for 20secs
        machine.deepsleep(20000)

run()