#!/usr/bin/python

import contextlib
import hue
import os
import time

ON_FILE_PATH = '/Users/pegerita/morning_alarm.txt'
SPEED = 1.0
REFRESH = 5

# We hard-code our bridge internal IP address as the IP address discovery
# through the portal service can sometimes fail.
HUE_BRIDGE_IP = '10.0.1.15'


def IsAlarmOn():
  if not os.path.isfile(ON_FILE_PATH):
    return False
  with open(ON_FILE_PATH) as f:
    for line in f:
      return line.strip().lower() == 'on'
  return False


def Transition(cx, light, first, second, duration, refresh):
  startTime = time.time()
  ctime = time.time()
  while ctime < startTime + duration:
    if not IsAlarmOn():
      return
    cx.SetColor(light, first.Blend(second, (ctime - startTime) / duration))
    time.sleep(refresh)
    ctime = time.time()


def Sunrise():
  if not IsAlarmOn():
    return
  dimredblue = hue.Color(bri=0, x=0.5762, y=0.268)
  redblue = dimredblue.Replace(bri=51)
  dimyellow = hue.Color(bri=51, x=0.509, y=0.4149)
  white = dimyellow.Replace(bri=102)
  with contextlib.closing(hue.NewContext('newdeveloper', ip=HUE_BRIDGE_IP)) as cx:
    cx.On(0)
    cx.SetColor(0, dimredblue)
    time.sleep(720.0 / SPEED)
    Transition(cx, 0, dimredblue, redblue, 180.0 / SPEED, REFRESH)
    Transition(cx, 0, redblue, dimyellow, 180.0 / SPEED, REFRESH)
    Transition(cx, 0, dimyellow, white, 720.0 / SPEED, REFRESH)


if __name__ == '__main__':
  Sunrise()
