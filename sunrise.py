#!/usr/bin/python

import contextlib
import hue
import os
import time

ON_FILE_PATH = '/Users/pegerita/morning_alarm.txt'
DURATION = 300
REFRESH = 5


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
  blue = hue.BLUE.Replace(bri=0)
  red = hue.RED.Replace(bri=85)
  orange = hue.ORANGE.Replace(bri=170)
  white = hue.WHITE
  with contextlib.closing(hue.NewContext('newdeveloper')) as cx:
    cx.On(0)
    Transition(cx, 0, blue, red, DURATION, REFRESH)
    Transition(cx, 0, red, orange, DURATION, REFRESH)
    Transition(cx, 0, orange, white, DURATION, REFRESH)


if __name__ == '__main__':
  Sunrise()
