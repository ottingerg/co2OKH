from neopixel import NeoPixel
from machine import Pin
from time import sleep
import _thread as thread

class VIS:
  def __init__(self, getvalue, gpio=12, n=11):
    self.pin = Pin(gpio, Pin.OUT)
    self.np = NeoPixel(self.pin, n)
    self.n = n
    self.wdtlock = thread.allocate_lock()
    self.getvalue = getvalue
    self.red = (20,0,0)
    self.green = (0,20,0)
    self.yellow = (20,20,0)
    self.heartbeat = 1.0
    self.multi = 1.05
    self.runflag = False
    self.flash()
    
  def setleds(self,co2):
    if co2 < 800:
      self.np[0] = (0, int(20*self.heartbeat), 0)
    elif co2 >= 1400:
      self.np[0] = (int(20*self.heartbeat),0,0)
    else:
      self.np[0] = (int(20*self.heartbeat),int(20*self.heartbeat),0)
    


    if self.heartbeat > 2.0:
      self.multi = 0.95
    if self.heartbeat < 0.5:
      self.multi = 1.05
      
    self.heartbeat = self.heartbeat * self.multi
    
    i = 1
    col = self.green
    for co2_thres in range(500,1401,100):
      if co2_thres >= 800:
        col = self.yellow
      if co2_thres >= 1400:
        col = self.red
        
      if co2 > co2_thres:
        self.np[i] = col
      else:
        self.np[i] = (0,0,0)
        
      i = i + 1
    
    self.np.write()
    
  def run(self):
    while True:
      co2 = self.getvalue()
      self.setleds(co2)
      self.setrunflag()
      sleep(0.01)
   
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
    
  def flash(self): 
    self.np.fill((50,50,50))
    self.np.write()
    sleep(0.5)
    self.np.fill((0,0,0))
    self.np.write()



