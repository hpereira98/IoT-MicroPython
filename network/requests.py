import config
# MicroPython comes preloaded with urequests, which is a simplified version of requests.
import urequests
# contact simple web service that tells you what is your public IP address
r = urequests.get('http://icanhazip.com')
# request code
r.status_code
# request data
r.text

# using a IFTTT WebHook
r = urequests.post(config.REQUEST_URL, json={'value1': 'micropython1'})
# check if request was successful
r.status_code