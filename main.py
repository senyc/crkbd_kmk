import board
import supervisor
import time

from storage import getmount

from kb import KMKKeyboard

from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.peg_oled_display import Oled, OledData, OledDisplayMode, OledReactionType
from kmk.extensions.peg_rgb_matrix import Rgb_matrix
from kmk.extensions.peg_rgb_matrix import Rgb_matrix,Rgb_matrix_data,Color
from kmk.hid import HIDModes
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide

""" Keyboard configuration """

keyboard = KMKKeyboard()
keyboard.debug_enabled = False

""" Layers configuration """

combo_layers = {
    (1, 2): 3,
}
keyboard.modules.append(Layers(combo_layers))

""" Split configuration """

split = Split(use_pio=True)

""" OLED configuration """

side = SplitSide.RIGHT if str(getmount('/').label)[-1] == 'R' else SplitSide.LEFT

if side == SplitSide.LEFT:
    # Not actually any randomness here, but good enough
    random_number1 = int((time.monotonic() * 1000) % 10000)
    random_number2 = int(((time.monotonic() * 1000) * 257) % 10000)

    oled_ext = Oled(
        OledData(
            corner_one={0:OledReactionType.LAYER,1:["qwerty", "nums", "func", "macro"]},
            corner_two={0:OledReactionType.STATIC,1:[f"  {random_number2:04d}"]},
            corner_three={0:OledReactionType.STATIC,1:["crkbd"]},
            corner_four={0:OledReactionType.STATIC,1:[f"  {random_number1:04d}"]},
        ),
        toDisplay=OledDisplayMode.TXT,flip=False
    )
else:
    oled_ext = Oled(
        OledData(
            image={0:OledReactionType.STATIC,1:["1.bmp"]}
        ),
            toDisplay=OledDisplayMode.IMG,flip=False
    )


""" LED configuration """

rgb_matrix=Rgb_matrix_data(
    keys=[
        Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE,
        Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE,
        Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE,
        Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE
          ],
    underglow=[
        Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE, Color.BLUE
    ]
)

rgb_ext = Rgb_matrix(split=True,ledDisplay=rgb_matrix, disable_auto_write=True)

""" Keymap configuration """


"""
GESC: Escape unless selected with super, then ` if shift then ~
BKDL: backspace unless selected with super, then del
"""
keyboard.keymap = [
    [
        KC.GESC, KC.Q, KC.W, KC.E, KC.R, KC.T, KC.Y, KC.U, KC.I, KC.O, KC.P, KC.BKDL,
        KC.LCTRL, KC.A, KC.S, KC.D, KC.F, KC.G, KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT,
        KC.LSFT, KC.Z, KC.X, KC.C, KC.V, KC.B, KC.N, KC.M, KC.COMMA, KC.DOT, KC.SLASH, KC.RSFT,

        KC.LGUI, KC.MO(1), KC.SPC, KC.TAB, KC.MO(2), KC.RALT
    ],
    [
        KC.TRNS, KC.EXCLAIM, KC.AT, KC.HASH, KC.DOLLAR, KC.PERCENT, KC.CIRCUMFLEX, KC.AMPERSAND, KC.ASTERISK, KC.LPRN, KC.RPRN, KC.ENT,
        KC.TRNS, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.MINS,
        KC.TRNS, KC.BSLASH, KC.UNDERSCORE, KC.PLUS, KC.EQUAL, KC.PIPE, KC.GRAVE, KC.LEFT_CURLY_BRACE, KC.RIGHT_CURLY_BRACE, KC.LBRACKET, KC.RBRACKET, KC.RALT,

        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
    ],
    [
        KC.TRNS, KC.F1, KC.F2, KC.F3, KC.F4, KC.F5, KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.ENT,
        KC.TRNS, KC.F11, KC.F12, KC.PGUP, KC.PGDN, KC.PSCR, KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT, KC.PLUS, KC.MINS,
        KC.TRNS, KC.AUDIO_VOL_DOWN, KC.AUDIO_VOL_UP, KC.MEDIA_PREV_TRACK, KC.MEDIA_PLAY_PAUSE, KC.MEDIA_NEXT_TRACK, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.RALT,

        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS
    ],
    [
        KC.TRNS, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.TRNS,
        KC.TRNS, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.TRNS,
        KC.TRNS, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.TRNS,

        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS
    ]
]

keyboard.modules.append(split)

keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(oled_ext)
keyboard.extensions.append(rgb_ext)


if __name__ == "__main__":
    keyboard.go(hid_type=HIDModes.USB)
