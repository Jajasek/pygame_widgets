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


from pygame_widgets.constants.public import THECOLORS, SRCALPHA, button_bg, frame, A_TOPLEFT, A_CENTER, A_BOTTOMRIGHT
from pygame_widgets.auxiliary import cursors


class DEFAULT:
    cursor = cursors.arrow

    class WINDOW:
        fps = 25
        color = THECOLORS['gray90']

    class TEXT:
        font_color = THECOLORS['black']
        font = 'calibri'
        font_size = 16
        text = ""
        bold = False
        italic = False
        underlined = False
        smooth = True

        class Alignment:
            x = A_CENTER
            y = A_CENTER

    class LABEL:
        bg = THECOLORS['transparent']

    class IMAGE:
        bg = THECOLORS['white']

    class BUTTON:
        bg_normal = button_bg(THECOLORS['gray80'], THECOLORS['gray65'])
        bg_mouseover = button_bg(THECOLORS['lightblue1'], THECOLORS['blue'])
        bg_pressed = button_bg(THECOLORS['lightblue3'], THECOLORS['blue'])
        cursor_mouseover = cursor_pressed = cursors.arrow

    class ENTRY:
        bg = frame(THECOLORS['white'], THECOLORS['blue'])
        cursor = cursors.textmarker

        class Alignment:
            x = A_TOPLEFT
            y = A_CENTER

        class Boundary_space:
            top = 3
            left = 6
            bottom = 3
            right = 6

        class Text:
            font_color = THECOLORS['black']
            highlight_font_color = THECOLORS['white']
            highlight_bg = THECOLORS['blue']
            font = 'calibri'
            font_size = 16
            bold = False
            italic = False
            underlined = False
            smooth = True
            text = "Hello World"

        class Cursor:
            color = THECOLORS['black']


SUPER = '_SUPER'  # kwarg used to detect if the class is initialising as super() or not
PYGAME_EVENTS = range(1, 18)
DEBUG = False
