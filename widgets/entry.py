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
        super().__init__(master, topleft, size, background=CONST.DEFAULT.ENTRY.Cursor.color)
        self._safe_init(**kwargs)


# TODO: alignment
class Entry(I.Image):
    """1-line text widget user can write into."""

    def __init__(self, master, topleft=(0, 0), size=(1, 1), **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, **updated)
        self.boundary_space_l = CONST.DEFAULT.ENTRY.Boundary_space.left
        self.boundary_space_r = CONST.DEFAULT.ENTRY.Boundary_space.right
        self.background = CONST.DEFAULT.ENTRY.bg

        self.intervals = list()

        self._child_init.append(self.__child_init)
        self._safe_init(**kwargs)

    def __child_init(self):
        self.w_visible_area = B.Button(self, (self.boundary_space_l, 0),
                                       (self.master_rect.size[0] - self.boundary_space_l - self.boundary_space_r, 1),
                                       visible=False)
        self.w_text = T.Label(self.w_visible_area, auto_res=True)
        self.w_highlight = T.Label(self.w_visible_area, auto_res=True)
        self.w_cursor = _Cursor(self.w_visible_area, (0, 0), (1, 1))

    def _find_intervals(self):
        # noinspection PyTypeChecker
        self.intervals = [0] + [None] * (len(self.text) - 1)
        for i in range(1, len(self.text)):
            self.intervals[i] = self.w_text.font.size(self.text[:i])[0]

    @property
    def background(self):
        return self.image

    @background.setter
    def background(self, value):
        self.image = value

    @property
    def font_name(self):
        return self.w_text.font_name

    @font_name.setter
    def font_name(self, value):
        self.w_text.set(font_name=value)
        self.w_highlight.set(font_name=value)

    @property
    def font_size(self):
        return self.w_text.font_size

    @font_size.setter
    def font_size(self, value):
        self.w_text.set(font_size=value)
        self.w_highlight.set(font_size=value)

    @property
    def bold(self):
        return self.w_text.bold

    @bold.setter
    def bold(self, value):
        self.w_text.set(bold=value)
        self.w_highlight.set(bold=value)

    @property
    def italic(self):
        return self.w_text.italic

    @italic.setter
    def italic(self, value):
        self.w_text.set(italic=value)
        self.w_highlight.set(italic=value)

    @property
    def underlined(self):
        return self.w_text.underlined

    @underlined.setter
    def underlined(self, value):
        self.w_text.set(underlined=value)
        self.w_highlight.set(underlined=value)

    @property
    def smooth(self):
        return self.w_text.smooth

    @smooth.setter
    def smooth(self, value):
        self.w_text.set(smooth=value)
        self.w_highlight.set(smooth=value)

    @property
    def font_color(self):
        return self.w_text.font_color

    @font_color.setter
    def font_color(self, value):
        self.w_text.set(font_color=value)

    @property
    def text(self):
        return self.w_text.text

    @text.setter
    def text(self, value):
        self.w_text.set(text=value)

    @property
    def highlight_font_color(self):
        return self.w_highlight.font_color

    @highlight_font_color.setter
    def highlight_font_color(self, value):
        self.w_highlight.set(font_color=value)

    @property
    def highlight_background(self):
        return self.w_highlight.background

    @highlight_background.setter
    def highlight_background(self, value):
        self.w_highlight.set(background=value)
