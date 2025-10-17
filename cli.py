#!/usr/bin/env python3
"""
M4T Signal Tower Light python api
https://www.amazon.com/dp/B0DLKKFCZB
"""

from m4t_tower_light import M4TTowerLight
import argparse
import sys

def main():
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--light", "-l", default="off", choices=M4TTowerLight.light.modes, help="The light state")
        parser.add_argument("--alarm", "-b", default="off", choices=M4TTowerLight.alarm.modes, help="The alarm state")
        parser.add_argument("--blink", "-f", default="off", choices=M4TTowerLight.blink.modes, help="The blink state")
        args = parser.parse_args()

        tower = M4TTowerLight()
        tower.set(args.light, args.alarm, args.blink)

if __name__ == "__main__":
        sys.exit(main())
