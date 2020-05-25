import machine
import dht

# my temperature sensor is DHT11 and I connected it to the pin GPIO5
d = dht.DHT11(machine.Pin(5))
# tell the sensor to get the values
d.measure()
# print the temperature
d.temperature()
# print the humidity
d.humidity()