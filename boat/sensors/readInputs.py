import Adafruit_BBIO
# spi = Adafruit_BBIO.SPI(bus, device) #/dev/spidev<bus>.<device>

# /dev/spidev0.0
spi = Adafruit_BBIO.SPI(0, 0)
print(spi.xfer2([32, 11, 110, 22, 220]))
spi.close()