import hue
import time

def Transition(cx, light, first, second, duration, refresh):
  startTime = time.time()
  ctime = time.time()
  while ctime < startTime + duration:
    cx.SetColor(light, first.Blend(second, (ctime - startTime) / duration))
    time.sleep(refresh)
    ctime = time.time()

if __name__ == '__main__':
  blue = hue.BLUE.Replace(bri=0)
  red = hue.RED.Replace(bri=85)
  orange = hue.ORANGE.Replace(bri=170)
  white = hue.WHITE
  cx = hue.NewContext('newdeveloper')
  cx.On(0)
  Transition(cx, 0, blue, red, 300, 5)
  Transition(cx, 0, red, orange, 300, 5)
  Transition(cx, 0, orange, white, 300, 5)
