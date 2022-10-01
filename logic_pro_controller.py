# https://github.com/pimoroni/pmk-circuitpython
# https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware
from pmk import PMK
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode


pmk = PMK(Hardware())
keys = pmk.keys

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

keymap = [
    (Keycode.LEFT_SHIFT, Keycode.COMMA),  # Row 1 (top, C = fast rewind, 8 = rewind , 4 = forward, 0 = fast forward)
    Keycode.COMMA,
    Keycode.PERIOD,
    (Keycode.LEFT_SHIFT, Keycode.PERIOD),
    Keycode.K,  # Row 2 (D = metronome click, 9 = count-in, 5 = solo mode, 1 = cycle mode)
    (Keycode.LEFT_SHIFT, Keycode.K),
    (Keycode.LEFT_CONTROL, Keycode.S),
    Keycode.C,
    (Keycode.COMMAND, Keycode.TWO),  # Row 3 (E = open mixer, A = open piano roll, 6 = open smart controls, 2 = toggle library)
    (Keycode.COMMAND, Keycode.FOUR),
    (Keycode.COMMAND, Keycode.THREE),
    Keycode.Y,
    Keycode.R,  # Row 4 (bottom, F = record, B = stop, 7 = pause, 3 = play)
    Keycode.KEYPAD_ZERO,
    Keycode.KEYPAD_PERIOD,
    Keycode.KEYPAD_ENTER
]

key_colors = [
    (0, 0, 96),  # Row 1 (top, C, 8, 4, 0)
    (0, 0, 32),
    (32, 0, 32),
    (32, 0, 96),
    (32, 0, 32),  # Row 2 (D, 9, 5, 1)
    (32, 0, 32),
    (32, 32, 0),
    (32, 32, 0),
    (0, 32, 32),  # Row 3 (E, A, 6, 2)
    (0, 32, 32),
    (0, 32, 32),
    (0, 32, 32),
    (32, 0, 0),  # Row 4 (bottom, F = red, B = yellow, 7 = orange, 3 = green)
    (32, 32, 0),
    (64, 32, 0),
    (0, 64, 0)
]

for key in keys:
    @pmk.on_press(key)
    def press_handler(key):
        binding = keymap[key.number]
        if type(binding) is tuple:
            first, second = binding
            keyboard.send(first, second)
        else:
            keyboard.send(binding)


for i in range(len(keys)):
    r, g, b = key_colors[i]
    keys[i].set_led(r, g, b)


while True:
    pmk.update()
