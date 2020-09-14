

# This file is executed on every boot (including wake-boot from deepsleep)

#import esp

#esp.osdebug(None)

#import webrepl

#webrepl.start()

from machine import reset
from time import sleep
from struct import pack,unpack

try: 
  f = open('bootcount.dat')
  bootcount = int(f.read())
  f.close()
except:
  bootcount = 0
  
bootcount = bootcount + 1

f = open('bootcount.dat','w')
f.write(str(bootcount))
f.close()


print("press CTRL+C to interrupt autoboot.")
for i in range(1,4):
  print(".")
  sleep(1)

import monitor


