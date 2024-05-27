import adafruit_dht
from board import D17
import time

dht = adafruit_dht.DHT11(D17)
sleep_time = 10

while True:
    try:
        print("Humidity: {}%", dht.humidity)
        print("Temperature: {}%", dht.temperature)
    except RuntimeError as error:
        # Catch RuntimeError, because of https://github.com/adafruit/Adafruit_CircuitPython_DHT/issues/33
        # and because DHTs are hard to read in general
        print(error.args[0])
        time.sleep(sleep_time)
        continue
    except Exception as error:
        # If any other error occurs, exit
        dht.exit()
        raise error
    time.sleep(sleep_time)