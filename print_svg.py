#!/usr/bin/env python3

import argparse
from html.parser import HTMLParser
import time

parser = argparse.ArgumentParser(
    description='Print prepared SVG image to lego printer'
)
parser.add_argument('input_path', action='store', type=str, help='Input path')
args = parser.parse_args()

X_COORDS = []
Y_COORDS = []


class Parse(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()

    def handle_starttag(self, tag, attrs):
        for a in attrs:
            if a[0] == "points":
                global X_COORDS
                global Y_COORDS
                coords = list(map(float, a[1].split(",")))
                X_COORDS.append(coords[0::2])
                Y_COORDS.append(coords[1::2])


parser = Parse()
parser.feed(open(args.input_path, "r").read())

max_x = max(map(max, X_COORDS))
min_x = min(map(min, X_COORDS))
delta_x = max_x - min_x

max_y = max(map(max, Y_COORDS))
min_y = min(map(min, Y_COORDS))
delta_y = max_y - min_y

print(min_x, min_y, max_x, max_y)


def motor_x(x):
    return int(305 - 300 * ((max_x - x) / delta_x))


def motor_y(y):
    return int(545 - 540 * ((max_y - y) / delta_y))


from cued_ia_lego import *
# Try to find connected brick
try:
    brick = NXTBrick()
except Exception:
    exit()

sensor = Light(brick, PORT_1, illuminated=True)
mA = Motor(brick, PORT_A)
mA.reset_position()
mB = Motor(brick, PORT_B)
mB.reset_position()
mC = Motor(brick, PORT_C)
mC.reset_position()
mA.wait_for()
mB.wait_for()
mC.wait_for()

# PENUP
mC.turn(80, power=40, brake=True)
mC.wait_for()

for x_series, y_series in zip(X_COORDS, Y_COORDS):
    # GOTO x_series[0], y_series[0]
    mA.turn_to(motor_x(x_series[0]), power=30, brake=False)
    mA.wait_for()
    mB.turn_to(motor_y(y_series[0]), power=30, brake=False)
    mB.wait_for()

    # PENDOWN
    mC.turn(-80, power=40, brake=True)
    mC.wait_for()
    while not mC.is_ready():
        time.sleep(0.1)

    for x, y in zip(x_series[1:], y_series[1:]):
        # GOTO x, y
        print(f"moving from ({x}, {y}) to ({motor_x(x)}, {motor_y(y)})", )
        mA.turn_to(motor_x(x), power=30, brake=True)
        mB.turn_to(motor_y(y), power=30, brake=True)
        time.sleep(0.4)
        while not mA.is_ready():
            time.sleep(0.15)
        time.sleep(0.4)
        while not mB.is_ready():
            time.sleep(0.15)
    # PENUP
    mC.idle()
    mC.turn(80, power=40, brake=True)
    mC.wait_for()

# GOTO ZERO
mA.turn_to(0, power=20, brake=True)
mB.turn_to(0, power=30, brake=True)
mC.turn_to(0, power=20, brake=True)
