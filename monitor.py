import _thread as thread
from vis import VIS
from scd30 import co2sensor
from machine import WDT
from time import sleep

wdt = WDT(timeout = 10000)
wdt.feed()


sensor = co2sensor()
visual = VIS(getvalue=sensor.get)

thread_vis = thread.start_new_thread(visual.run,())
thread_sensor = thread.start_new_thread(sensor.run,())

while True:
  while not sensor.getrunflag():
    sleep(1)
  while not visual.getrunflag():
    sleep(1)
  wdt.feed()


