#!/usr/bin/env python3
"""
M4T Signal Tower Light python api
https://www.amazon.com/dp/B0DLKKFCZB
"""

from serial.tools import list_ports
from serial import Serial
import argparse
import sys


class Modes():
    _map = {}
    _current = None

    def __init__(self):
        self._current = self._map["off"]

    @classmethod
    def modes(cls):
        return list(cls._map.keys())

    def set(self, x):
        if x not in self._map:
            raise RuntimeException(f"Value for {self.__name__} must be one of {cls._map.keys()}, got {x}")
        self._current = self._map[x]
        
    def get(self):
        return self._current


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


class M4TTower():
    _id = "1A86:7523"
    _baud_rate = 9600
    _light = LightModes()
    _alarm = AlarmModes()
    _blink = BlinkModes()
   
    def _send(self):
        self._serial.write(bytes([0xFF, self._light.get(), self._alarm.get(), self._blink.get(), 0xAA]))
        
    def __init__(self):
        d = list(list_ports.grep(self._id))
        assert len(d) == 1, f"Found more then one device with vendor:product {VID_PID}."
        self._serial = Serial(d[0].device, self._baud_rate, timeout=0)

    def set(self, light, alarm, blink):
        self._light.set(light)
        self._alarm.set(alarm)
        self._blink.set(blink)
        self._send()

def main():
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--light", "-l", default="off", choices=LightModes.modes(), help="The light state")
        parser.add_argument("--alarm", "-b", default="off", choices=AlarmModes.modes(), help="The alarm state")
        parser.add_argument("--blink", "-f", default="off", choices=BlinkModes.modes(), help="The blink state")
        args = parser.parse_args()
        tower = M4TTower()
        tower.set(args.light, args.alarm, args.blink)

if __name__ == "__main__":
        sys.exit(main())

