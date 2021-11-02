#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(
    description=
    'Retrieve data from scanning instrument. Optionally store output as .npz'
)
parser.add_argument(
    'out', action='store', nargs='?', type=str, help='Output path.'
)
args = parser.parse_args()

from cued_ia_lego import *
import time

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

# Create empty list for the light sensor readings
light_readings = []

l_r = []
A_p = []
B_p = []

# Lower scanning head
mC.turn(-130, power=20, brake=True)
mC.wait_for()

INSTRUCTIONS = [
    (mA, 300, True), (mB, 6, True), (mA, -300, False), (mB, 6, True)
] * 100

# Sometimes the brick just ... stops? This 'try' block prevents any
# lego related exceptions being raised. The machine is left in an intermediary
# state, but all data collected is still processed
try:
    for (motor, dist, read) in INSTRUCTIONS:
        if read:
            motor.turn(dist, power=24, brake=True)
        else:
            motor.turn(dist, power=24, brake=True)
            time.sleep(0.5)
        while not motor.is_ready():
            if read:
                l_r.append(sensor.get_lightness())
                A_p.append(mA.get_position())
                B_p.append(mB.get_position())

    sensor.set_illuminated(False)
    # Move the motor back to its starting position
    mA.turn_to(0, power=20, brake=True)
    mB.turn_to(0, power=30, brake=True)
    mC.turn_to(0, power=20, brake=True)

except Exception as err:
    print(err)

# Display some information about the results
num_readings = len(l_r)
print(f'The number of readings was: {num_readings}')

from matplotlib import pyplot as plt
from matplotlib import cm, mlab
import numpy as np

l_r = np.array(l_r)
A_p = np.array(A_p)
B_p = np.array(B_p) / 1.8

if args.out:
    np.savez(args.out, l_r=l_r, A_p=A_p, B_p=B_p)

plt.subplot(111)
plt.hexbin(A_p, B_p, C=l_r, gridsize=15, cmap=cm.Greys_r, bins=None)
plt.axis([A_p.min(), A_p.max(), B_p.min(), B_p.max()])
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()

cb = plt.colorbar()
cb.set_label('mean value')
plt.show()
