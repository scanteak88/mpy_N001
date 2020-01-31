import machine
from machine import I2C, Pin

#i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
'''
while True:
	sensor.measure()
	print(sensor.temperature())
	print(sensor.humidity())
	time.sleep_ms(4000)
'''

class DHTBaseI2C:
    def __init__(self, i2c, addr=0x5c):
        self.i2c = i2c
        self.addr = addr
        self.buf = bytearray(5)
    def measure(self):
        buf = self.buf
        self.i2c.readfrom_mem_into(self.addr, 0, buf)
        if (buf[0] + buf[1] + buf[2] + buf[3]) & 0xff != buf[4]:
            raise Exception("checksum error")

class DHT12(DHTBaseI2C):
    def humidity(self):
        return self.buf[0] + self.buf[1] * 0.1

    def temperature(self):
        t = self.buf[2] + (self.buf[3] & 0x7f) * 0.1
        if self.buf[3] & 0x80:
            t = -t
        return t

def setdht12():
    global sensor
    sensor.measure()
    print("tm:",sensor.temperature())
    print("rh:",sensor.humidity())

def getdht12():
    global sensor
    sensor.measure()
    return sensor.temperature(),sensor.humidity()




i2c = I2C(scl=Pin(5), sda=Pin(4))
sensor = DHT12(i2c)


