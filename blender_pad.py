import os

from pmk import PMK, hsv_to_rgb
from pmk.platform.keybow2040 import Keybow2040 as Hardware
from time import monotonic
from random import randint
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

pmk = PMK(Hardware())
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)
keys = pmk.keys

# state of the app set my the func key (15)
mode = 0
# apple = 0, linux = 1, windows = 2
comp_os = 0
# select pad layout
screen = 0
arrow_keys = [6, 5, 1, 9]  # up, down, left right

# X color
red = (245, 66, 66)
# Y color
green = (102, 245, 66)

# Z color
blue = (66, 135, 245)

# indicator yellow
yellow = (245, 233, 66)
white = (255, 255, 255)

def lights_on():
    # Turn on lights (grab)
    keys[3].set_led(*red)
    keys[7].set_led(*green)
    keys[11].set_led(*blue)
    # Turn on lights (rotate)
    keys[2].set_led(*red)
    keys[6].set_led(*green)
    keys[10].set_led(*blue)
    # Turn on lights (scale)
    keys[1].set_led(*red)
    keys[5].set_led(*green)
    keys[9].set_led(*blue)


lights_on()

def arrow_keys_toggle(on=False):
    for x in arrow_keys:
        if on:
            keys[x].set_led(*blue)
        else:
            keys[x].led_off()

def safe_sleep(s):
    clock = 0
    start = monotonic()
    press_time = s
    while clock < press_time:
        clock = monotonic() - start


def get_alt(flag):
    return Keycode.OPTION if flag == 0 else Keycode.ALT

def manip(k, _ax, _act):
    ax = {
        'x': Keycode.X,
        'y': Keycode.Y,
        'z': Keycode.Z
    }

    act = {
        'g': Keycode.G,
        'r': Keycode.R,
        's': Keycode.S
    }


    cmd = [ax[_ax.lower()]]
    if mode == 1:
        cmd.insert(0, Keycode.SHIFT)

    k.set_led(*white)
    keyboard.send(Keycode.ESCAPE)
    keyboard.send(act[_act.lower()])
    keyboard.send(*cmd)


def grab(k, _ax):
    manip(k, _ax, 'g')


def rotate(k, _ax):
    manip(k, _ax, 'r', )


def scale(k, _ax):
    manip(k, _ax, 's')


# Func key
@pmk.on_press(keys[0])
def func_key(key):
    global mode
    mode += 1
    if mode >= 3:
        mode = 0


# comp os button
@pmk.on_press(keys[4])
def comp_set(key):
    global comp_os
    comp_os += 1
    if comp_os >= 3:
        comp_os = 0


# pad layout button
@pmk.on_press(keys[12])
def screen_set(key):
    global screen
    screen += 1
    if screen > 0:
        for x in range(16):
            if x % 4 != 0:
                keys[x].led_off()
                arrow_keys_toggle(True)
    if screen >= 2:
        arrow_keys_toggle()
        lights_on()
        screen = 0

# grab
@pmk.on_press(keys[3])
def grab_x(key):
    if screen == 0:
        grab(key, 'x')
        safe_sleep(0.3)
        key.set_led(*red)
    if screen == 1:
        pass


@pmk.on_press(keys[7])
def grab_y(key):
    if screen == 0:
        grab(key, 'y')
        safe_sleep(0.3)
        key.set_led(*green)
    if screen == 1:
        pass


@pmk.on_press(keys[11])
def grab_y(key):
    if screen == 0:
        grab(key, 'z')
        safe_sleep(0.3)
        key.set_led(*blue)
    if screen == 1:
        pass


# rotate
@pmk.on_press(keys[2])
def rotate_y(key):
    if screen == 0:
        rotate(key, 'x')
        safe_sleep(0.3)
        key.set_led(*red)
    if screen == 1:
        pass


@pmk.on_press(keys[6])
def rotate_y(key):
    if screen == 0:
        rotate(key, 'y')
        safe_sleep(0.3)
        key.set_led(*green)
    if screen == 1:
        pass


@pmk.on_press(keys[10])
def rotate_y(key):
    if screen == 0:
        rotate(key, 'z')
        safe_sleep(0.3)
        key.set_led(*blue)
    if screen == 1:
        pass


# scale
@pmk.on_press(keys[1])
def scale_x(key):
    if screen == 0:
        scale(key, 'x')
        safe_sleep(0.3)
        key.set_led(*red)
    if screen == 1:
        pass


@pmk.on_press(keys[5])
def scale_y(key):
    if screen == 0:
        scale(key, 'y')
        safe_sleep(0.3)
        key.set_led(*green)
    if screen == 1:
        pass


@pmk.on_press(keys[9])
def scale_z(key):
    if screen == 0:
        scale(key, 'z')
        safe_sleep(0.3)
        key.set_led(*blue)
    if screen == 1:
        pass


# reset
@pmk.on_press(keys[15])
def reset_grab(key):
    if screen == 0:
        key.set_led(*white)
        keyboard.send(Keycode.ESCAPE, get_alt(comp_os), Keycode.G)
        safe_sleep(0.3)
        key.led_off()
    if screen == 1:
        pass


@pmk.on_press(keys[14])
def reset_rotate(key):
    if screen == 0:
        key.set_led(*white)
        keyboard.send(Keycode.ESCAPE, get_alt(comp_os), Keycode.R)
        safe_sleep(0.3)
        key.led_off()
    if screen == 1:
        pass


@pmk.on_press(keys[13])
def reset_scale(key):
    if screen == 0:
        key.set_led(*white)
        keyboard.send(Keycode.ESCAPE, get_alt(comp_os), Keycode.S)
        safe_sleep(0.3)
        key.led_off()
    if screen == 1:
        pass


@pmk.on_press(keys[3])
def send_tilde(key):
    if screen == 1:
        layout.write('~')


@pmk.on_press(keys[7])
def send_backtick(key):
    if screen == 1:
        layout.write('`')


def arrow(key, d):
    dir = {
        'u': Keycode.UP_ARROW,
        'd': Keycode.DOWN_ARROW,
        'l': Keycode.LEFT_ARROW,
        'r': Keycode.RIGHT_ARROW
    }

    if screen == 1:
        key.set_led(*white)
        keyboard.send(dir[d.lower()])
        safe_sleep(0.1)
        key.set_led(*blue)


@pmk.on_press(keys[6])
def send_up(key):
    arrow(key, 'u')


@pmk.on_press(keys[5])
def send_down(key):
    arrow(key, 'd')


@pmk.on_press(keys[1])
def send_left(key):
    arrow(key, 'l')



@pmk.on_press(keys[9])
def send_right(key):
    arrow(key, 'r')


indicator = keys[0]
comp_indicator = keys[4]
scr_indicator = keys[12]

while True:
    pmk.update()
    # mode led
    if mode == 0:
        indicator.led_off()
    if mode == 1:
        indicator.set_led(*white)
    if mode == 2:
        indicator.set_led(*yellow)
    # comp led
    if comp_os == 0:
        comp_indicator.led_off()
    if comp_os == 1:
        comp_indicator.set_led(*white)
    if comp_os == 2:
        comp_indicator.set_led(*yellow)
    # screen
    if screen == 0:
        scr_indicator.led_off()
    if screen == 1:
        scr_indicator.set_led(*white)