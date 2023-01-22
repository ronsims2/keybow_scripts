# This program scroll through all the keys and ligths them with a random color
from pmk import PMK, hsv_to_rgb
from pmk.platform.keybow2040 import Keybow2040 as Hardware
from time import monotonic
from random import randint

keybow = PMK(Hardware())
keys = keybow.keys
nap = 2
ticks = 0
start = -1

colors = [(randint(0, 255), randint(0, 255), randint(0, 255)) for _ in range(16)]
colors = [(255, 255, 255) if c[0] < 50 and c[1] < 50 and c[2] < 50 else c for c in colors]

curr_index = 0
max_key = 15
while True:
    keybow.update()
    if curr_index > 15:
        curr_index = 0

    if start == -1:
        start = monotonic()

    ticks = monotonic() - start

    keys[curr_index].set_led(*colors[curr_index])

    if ticks >= nap:
        keys[curr_index].led_off()
        curr_index += 1
        start = -1
        ticks = 0

