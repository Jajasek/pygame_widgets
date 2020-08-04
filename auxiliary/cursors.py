# pygame_widgets - Python GUI library built on pygame
# Copyright (C) 2018  Jáchym Mierva
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Jáchym Mierva
# jachym.mierva@gmail.com


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


_invisible_strings = [' ' * 8] * 8


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
invisible = compile(_invisible_strings)
hidden = (None, None, None, None)
