#!/usr/bin/env python3
"""
M4T Signal Tower Light python api
https://www.amazon.com/dp/B0DLKKFCZB
"""

from serial.tools import list_ports
from serial import Serial

class classproperty(object):
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)
    
class Modes():
    _map = { "off" : 0x01 }
    _current = None

    def __init__(self):
        self._current = self._map["off"]

    def set(self, x):
        if x not in self._map:
            raise RuntimeError(f"Value for {self.__name__} must be one of {self._map.keys()}, got {x}")
        self._current = self._map[x]
        
    def get(self):
        return self._current

    @classproperty
    def modes(cls):
        return list(cls._map.keys())

class LightModes(Modes):
    _map = {
        "off": 0x01,
        "green": 0x02,
        "blue": 0x3,
        "red": 0x4,
        "cyan": 0x5,
        "yellow": 0x6,
        "magenta": 0x07,
        "white": 0x08,
    }

class AlarmModes(Modes) :
    _map = {
        "off": 0x01,
        "on": 0x02,
    }

class BlinkModes(Modes):
    _map = {
        "off": 0x01,
        "fast": 0x02, # 0.85s/time
        "normal": 0x03, # 1.7s/time
        "slow": 0x04, # 2.5s/time
    }


class M4TTowerLight():
    _id = "1A86:7523"
    _baud_rate = 9600
    _light = LightModes()
    _alarm = AlarmModes()
    _blink = BlinkModes()
   
    def _send(self):
        self._serial.write(bytes([0xFF, self.light.get(), self.alarm.get(), self.blink.get(), 0xAA]))
        
    def __init__(self):
        d = list(list_ports.grep(self._id))
        assert len(d) == 1, f"Found more then one device with vendor:product {self._id}."
        self._serial = Serial(d[0].device, self._baud_rate, timeout=0)
    
    def set(self, light, alarm, blink):
        self.light.set(light)
        self.alarm.set(alarm)
        self.blink.set(blink)
        self._send()

    @classproperty
    def light(cls):
        return cls._light

    @classproperty
    def alarm(cls):
        return cls._alarm
    
    @classproperty
    def blink(cls):
        return cls._blink
