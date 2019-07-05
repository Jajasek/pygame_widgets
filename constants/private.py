from pygame_widgets.constants.public import THECOLORS, SRCALPHA
from pygame_widgets.auxiliary import cursors
from pygame import Surface


def button_bg(fill, edge):
    background = frame(fill, edge)

    def func(self, text):
        surf = background(self.master_rect.size)
        dest = (self.alignment_x * (self.master_rect.w - text.get_width()) / 2,
                self.alignment_y * (self.master_rect.h - text.get_height()) / 2)
        surf.blit(text, dest)
        surf.convert_alpha()
        return surf
    return func


def frame(fill, edge):
    def func(size):
        surf = Surface(size, SRCALPHA)
        surf.fill(edge)
        if size[0] > 2 and size[1] > 2:
            surf1 = Surface([a - 2 for a in size], SRCALPHA)
            surf1.fill(fill)
            surf.blit(surf1, (1, 1))
        return surf
    return func


class DEFAULT:
    cursor = cursors.arrow

    class WINDOW:
        fps = 25
        color = THECOLORS['gray90']

    class TEXT:
        bg_color = THECOLORS['transparent']
        font_color = THECOLORS['black']
        font = 'calibri'
        font_size = 16
        text = ""

        class Alignment:
            x = 1
            y = 1

    class IMAGE:
        bg = THECOLORS['white']

    class BUTTON:
        bg_normal = button_bg(THECOLORS['gray80'], THECOLORS['gray65'])
        bg_mouseover = button_bg(THECOLORS['lightblue1'], THECOLORS['blue'])
        bg_pressed = button_bg(THECOLORS['lightblue3'], THECOLORS['blue'])
        cursor_mouseover = cursors.tri_right
        cursor_pressed = cursors.tri_left

    class ENTRY:
        bg = frame(THECOLORS['white'], THECOLORS['blue'])

        class Boundary_space:
            left = 6
            right = 6

        class Cursor:
            color = THECOLORS['black']


SUPER = 's'  # kwarg used to detect if the class is initialising as super() or not
PYGAME_EVENTS = range(1, 18)
