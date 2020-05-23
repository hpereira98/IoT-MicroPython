import network

# access point interface
ap_if = network.WLAN(network.AP_IF)
# will return false, it is turned off by default. Do ap_if.active(True) to active. You will see ESP32-... appear on your available Wi-FI connections. The default password is 'micropythoN'.
ap_if.active()
# get access point infos: (IP, Subnet Mask, Gateway, DNS)
ap_if.ifconfig()
# changing its credentials
ap_if.config(essid='network name', password='password')

# station interface
sta_if = network.WLAN(network.STA_IF)
# not active as default as well, so lets activate it
sta_if.active(True)
# scan available connections: the first element in each tuple is the SSID name, the third element is the channel number, and the fourth is the RSSI or signal strength indicator.
sta_if.scan()
# connect to the intended internet
sta_if.connect('your SSID', 'your Wi-Fi password')
# verify if its connected
sta_if.isconnected()
# get connection parameters
sta_if.ifconfig()

# Setup WebREPL, a web-based REPL interface. This will open a dialog, in which you will setup the WebREPL: activate on boot, set a password and reboot.
# To use the WebREPL after that, unzip the webrepl-master.zip folder and run the html file.
import webrepl_setup

# Using config file, we can connect using:
sta_if.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

# MicroPython comes preloaded with urequests, which is a simplified version of requests.
import urequests
# contact simple web service that tells you what is your public IP address
r = urequests.get('http://icanhazip.com')
# request code
r.status_code
# request data
r.text