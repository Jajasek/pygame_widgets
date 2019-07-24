# TODO: fix the cursor displaying
import pygame.cursors as _cursors
import pygame.mouse as _mouse
# from pygame.cursors import *


_hand_strings = ['     XX                 ',
                 '    X..X                ',
                 '    X..X                ',
                 '    X..X                ',
                 '    X..X                ',
                 '    X..XXX              ',
                 '    X..X..XXX           ',
                 '    X..X..X..XX         ',
                 '    X..X..X..X.X        ',
                 'XXX X..X..X..X..X       ',
                 'X..XX........X..X       ',
                 'X...X...........X       ',
                 ' X..............X       ',
                 '  X.............X       ',
                 '  X.............X       ',
                 '   X............X       ',
                 '   X...........X        ',
                 '    X..........X        ',
                 '    X..........X        ',
                 '     X........X         ',
                 '     X........X         ',
                 '     XXXXXXXXXX         ',
                 '                        ',
                 '                        ']


def compile(strings, hotspot=(1, 1), black='X', white='.', xor='o'):
    """Creates cursor data needed by cursors.set() from a sequence of same-lenght strings.
    Public."""

    return ((len(strings[0]), len(strings)), hotspot, *_cursors.compile(strings, black, white, xor))


def set(size, hotspot, xormasks, andmasks):
    """Sets new cursor image. Predefined cursors are tuples containing the 4 needed arguments, so you can type
    cursors.set(*cursors.arrow). Custom cursors must be first compiled by cursors.compile() to create the needed args.
    Public."""

    if size is None:
        _mouse.set_visible(False)
    else:
        _mouse.set_visible(True)
        _mouse.set_cursor(size, hotspot, xormasks, andmasks)


def get():
    """Gets the current cursor settings.
    Public."""

    return _mouse.get_cursor()


load_xbm = _cursors.load_xbm
arrow = _cursors.arrow
ball = _cursors.ball
diamond = _cursors.diamond
broken_x = _cursors.broken_x
tri_left = _cursors.tri_left
tri_right = _cursors.tri_right
textmarker = compile(_cursors.textmarker_strings, (3, 7))
thickarrow = compile(_cursors.thickarrow_strings, (1, 1))
sizer_x = compile(_cursors.sizer_x_strings, (11, 7))
sizer_y = compile(_cursors.sizer_y_strings, (7, 11))
sizer_xy = compile(_cursors.sizer_xy_strings, (11, 7))
hand = compile(_hand_strings, (5, 1))
invisible = (None, None, None, None)
