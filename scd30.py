from machine import I2C, Pin,reset
from time import sleep, sleep_ms
from struct import unpack
from math import isnan
import _thread as thread

class co2sensor:
  def __init__(self, addr = 0x61, sdaP = 15, sclP = 2):
    self.i2c = I2C(1, sda = Pin(sdaP), scl = Pin(sclP), freq = 100000)
    self.addr = addr
    self.lock = thread.allocate_lock()
    self.wdtlock = thread.allocate_lock()
    self.co2 = 10000
    self.runflag = False
    print(self.i2c.scan())
    self.i2c.writeto(self.addr, b'\x00\x10\x00\x00\x81')

    
  def read(self):
    try:
      self.i2c.writeto(self.addr, b'\x03\x00')
      sleep_ms(10)
      b = self.i2c.readfrom(self.addr,18)
      return(unpack('>f',b[0:2]+b[3:5])[0])
    except:
      return(float('nan'))

  def run(self):
    while True:
      co2 = self.read()
      if not isnan(co2):
        self.lock.acquire()
        self.co2 = co2
        self.lock.release()
      if self.wdtlock.locked():
        self.wdtlock.release()
      self.setrunflag()
      sleep(2)

  def get(self):
     self.lock.acquire()
     co2 = self.co2
     self.lock.release()
     return(co2)
     
  def setrunflag(self):
    self.wdtlock.acquire()
    self.runflag = True
    self.wdtlock.release()
    
  def getrunflag(self):
    self.wdtlock.acquire()
    runflag = self.runflag
    self.runflag = False
    self.wdtlock.release()
    return(runflag)



