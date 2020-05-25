# IoT-MicroPython
A small project for a ESP32 microcontroller using MicroPython to check temperature and humidity.

I developed this project following the Miguel Grinberg's **MicroPython and the Internet of Things** tutorial (https://blog.miguelgrinberg.com/post/micropython-and-the-internet-of-things-part-i-welcome), and adapting it to the ESP32 board as the tutorial was written using an ESP8266.

## Getting Started:

- Mount ESP32 on the Breadboard
- Erase ESP32 previous data: 
```bash
esptool.py erase_flash
```
- Flash the MicroPython firmware to the board at address O
```
esptool.py --chip esp32 --port <your_serial_port> --baud 460800 write_flash -z 0x1000 esp32-idf3-20191220-v1.12.bin
```
- Connect to your board using RShell:
```bash
rshell --port <your_serial_port>
```
And then to interact with it in real time:
```bash
repl
```
- My ESP32 board only has one programmable LED (blue) on GPIO2.

## Working with files:

- List files and dirs on board, inside RShell:
```bash
ls /pyboard
```
- Copy file to board:
```bash
rshell --port <board serial port name> cp <py_file> /pyboard
```
