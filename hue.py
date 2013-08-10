import collections
import contextlib
import httplib
import json
import math


def FromHtml(htmlString):
  return _PALETTE.FromRGB(*_ParseRGBStr(htmlString))


def FromRGB(red, green, blue):
  return _PALETTE.FromRGB(red, green, blue)


class Color(collections.namedtuple('Color', 'bri x y')):
  __slots__ = ()

  def Replace(self, **kwargs):
    return self._replace(**kwargs)

  def Blend(self, color, ratio):
    iratio = 1.0 - ratio
    return Color(int(self.bri * iratio + color.bri * ratio + 0.5), self.x * iratio + color.x * ratio, self.y * iratio + color.y * ratio)


def NewContext(userId, ip=None):
  if not ip:
    ip = _GetIP()
  return Context(httplib.HTTPConnection(ip), userId)


class Context(object):
  
  def __init__(self, conn, userId):
    self._conn = conn
    self._userId = userId

  def On(self, id):
    self._conn.request('PUT', self._LightUrl(id), json.dumps({'on': True}))
    return self._conn.getresponse().read()

  def Off(self, id):
    self._conn.request('PUT', self._LightUrl(id), json.dumps({'on': False}))
    return self._conn.getresponse().read()

  def SetColor(self, id, color):
    self._conn.request('PUT', self._LightUrl(id), json.dumps({'bri': color.bri, 'xy': [color.x, color.y]}))
    return self._conn.getresponse().read()

  def close(self):
    self._conn.close()

  def _LightUrl(self, id):
    if id == 0:
      return self._AllUrl()
    return '/api/%s/lights/%s/state' % (self._userId, id)

  def _AllUrl(self):
    return '/api/%s/groups/0/action' % self._userId


def _ParseRGBStr(rgbStr):
  assert len(rgbStr) == 6
  r = int(rgbStr[:2], 16)
  g = int(rgbStr[2:4], 16)
  b = int(rgbStr[4:], 16)
  return r, g, b


def _GetIP():
  with contextlib.closing(httplib.HTTPConnection('www.meethue.com')) as conn:
    conn.request('GET', '/api/nupnp')
    response = json.loads(conn.getresponse().read())
    return response[0]['internalipaddress']


class _Palette(object):

  def __init__(self, red, green, blue):
    self._red = red
    self._green = green
    self._blue = blue

  def FromRGB(self, r, g, b):
    if r or g or b:
      sum = r + g + b
      sr = float(r) / sum
      sg = float(g) / sum
      sb = float(b) / sum
      x = sr * self._red[0] + sg * self._green[0] + sb * self._blue[0]
      y = sr * self._red[1] + sg * self._green[1] + sb * self._blue[1]
      return Color(max(r, g, b), x, y)
    return WHITE.Replace(bri=0)

_PALETTE = _Palette((0.675, 0.322), (0.313, 0.725), (0.167, 0.04))

BLUE = FromRGB(0, 0, 255)
RED = FromRGB(255, 0, 0)
GREEN = FromRGB(0, 255, 0)
YELLOW = FromRGB(255, 255, 0)
MAGENTA = FromRGB(255, 0, 255)
CYAN = FromRGB(0, 255, 255)
WHITE = FromRGB(255, 255, 255)
PINK = FromRGB(255, 51, 51)
ORANGE = FromRGB(255, 51, 0)
PURPLE = FromRGB(51, 0, 255)

