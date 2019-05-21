import pygame_widgets.widgets.button as B
import pygame_widgets.widgets.image as I
import pygame_widgets.constants.private as CONST
from pygame_widgets.constants.public import *


class _Cursor(I.Image):
    """Widget, that is displaying the cursor in Entry and similar widgets. Should not be instanced."""

    def __init__(self, master, topleft, size, **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, THECOLORS['black'])
        self._safe_init(**kwargs)


# TODO: create the entry widget
class Entry(B.Button):
    """1-line text widget you can write into."""

    def __init__(self, master, topleft=(0, 0), size=(1, 1), **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, **updated)
        self.w_text = None
        self.w_highlight = None
        self.w_cursor = None
        self.intervals = list()

    def _find_intervals(self):
        # noinspection PyTypeChecker
        self.intervals = [1] + [None] * (len(self.text) - 1)
        for i in range(1, len(self.text)):
            self.intervals[i] = self.font.size(self.text[:i])[0]
