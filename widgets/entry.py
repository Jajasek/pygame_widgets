import pygame_widgets.widgets.button as B
import pygame_widgets.widgets.image as I
import pygame_widgets.widgets.holder as H
import pygame_widgets.widgets.text as T
import pygame_widgets.constants.private as CONST
from pygame_widgets.constants import *


__all__ = ['Entry']


class _Cursor(I.Image):
    """Widget, that is displaying the cursor in Entry and similar widgets. Should not be instanced."""

    def __init__(self, master, topleft, size, **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, CONST.DEFAULT.ENTRY.Cursor.color)
        self._safe_init(**kwargs)


# TODO: create the entry widget
class Entry(B.Button):
    """1-line text widget user can write into."""

    def __init__(self, master, topleft=(0, 0), size=(1, 1), **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, **updated)
        self._child_init.append(self.__child_init)
        self.boundary_space_l = CONST.DEFAULT.ENTRY.Boundary_space.left
        self.boundary_space_r = CONST.DEFAULT.ENTRY.Boundary_space.right

        self.intervals = list()
        self._safe_init(**kwargs)

    def __child_init(self):
        self.w_visible_area = H.Holder(self, (self.boundary_space_l, 0),
                                       (self.master_rect.size[0] - self.boundary_space_l - self.boundary_space_r, 1))
        self.w_text = T.Label(self.w_visible_area, auto_res=True)
        self.w_highlight = T.Label(self.w_visible_area, auto_res=True)
        self.w_cursor = _Cursor(self.w_visible_area, (0, 0), (1, 1))

    def _find_intervals(self):
        # noinspection PyTypeChecker
        self.intervals = [0] + [None] * (len(self.text) - 1)
        for i in range(1, len(self.text)):
            self.intervals[i] = self.font.size(self.text[:i])[0]
