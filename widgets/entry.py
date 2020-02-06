import pygame_widgets.widgets.button as B
import pygame_widgets.widgets.image as I
import pygame_widgets.widgets.text as T
import pygame_widgets.constants.private as CONST
from pygame_widgets.auxiliary import cursors
from pygame_widgets.constants import *


__all__ = ['Entry']


class _Cursor(I.Image):
    """Widget, that is displaying the cursor in Entry and similar widgets. Should not be instanced."""

    def __init__(self, master, topleft, size, **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size)
        self._safe_init(**kwargs)
        self.position = None


# TODO: alignment
class Entry(I.Image):
    """1-line text widget user can write into."""

    def __init__(self, master, topleft=(0, 0), size=(1, 1), **kwargs):
        if not CONST.DEBUG:
            raise NotImplementedError("The development of this widget has not finished yet.")
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, **updated)
        self.boundary_space_t = CONST.DEFAULT.ENTRY.Boundary_space.top
        self.boundary_space_l = CONST.DEFAULT.ENTRY.Boundary_space.left
        self.boundary_space_b = CONST.DEFAULT.ENTRY.Boundary_space.bottom
        self.boundary_space_r = CONST.DEFAULT.ENTRY.Boundary_space.right
        self.background = CONST.DEFAULT.ENTRY.bg
        self.alignment_x = CONST.DEFAULT.ENTRY.Alignment.x
        self.alignment_y = CONST.DEFAULT.ENTRY.Alignment.y

        self.intervals = list()
        self._text_offset = 0
        self._active = False

        # TODO: pub_arg_dict
        self._child_init.append(self.__child_init)
        self._safe_init(**kwargs)

    def __child_init(self):
        self.w_visible_area = B.Button(self, (self.boundary_space_l, self.boundary_space_t),
                                       (self.master_rect.size[0] - self.boundary_space_l - self.boundary_space_r,
                                        self.master_rect.size[1] - self.boundary_space_t - self.boundary_space_b),
                                       bg_normal=THECOLORS['transparent'], bg_mouseover=THECOLORS['transparent'],
                                       bg_pressed=THECOLORS['transparent'])
        self.w_text = T.Label(self.w_visible_area, auto_res=True, font_name=CONST.DEFAULT.ENTRY.Text.font,
                              font_size=CONST.DEFAULT.ENTRY.Text.font_size, bold=CONST.DEFAULT.ENTRY.Text.bold,
                              italic=CONST.DEFAULT.ENTRY.Text.italic, underlined=CONST.DEFAULT.ENTRY.Text.underlined,
                              smooth=CONST.DEFAULT.ENTRY.Text.smooth, font_color=CONST.DEFAULT.ENTRY.Text.font_color,
                              background=THECOLORS['transparent'], text=CONST.DEFAULT.ENTRY.Text.text)
        self.w_highlight = T.Label(self.w_visible_area, auto_res=True, font_name=CONST.DEFAULT.ENTRY.Text.font,
                                   visible=False, font_size=CONST.DEFAULT.ENTRY.Text.font_size,
                                   bold=CONST.DEFAULT.ENTRY.Text.bold, italic=CONST.DEFAULT.ENTRY.Text.italic,
                                   underlined=CONST.DEFAULT.ENTRY.Text.underlined,
                                   smooth=CONST.DEFAULT.ENTRY.Text.smooth,
                                   font_color=CONST.DEFAULT.ENTRY.Text.highlight_font_color,
                                   background=CONST.DEFAULT.ENTRY.Text.highlight_bg, text="")
        self.w_cursor = _Cursor(self.w_visible_area, (0, 0), (1, CONST.DEFAULT.ENTRY.Text.font_size),
                                image=CONST.DEFAULT.ENTRY.Cursor.color)
        self.set(cursor_mouseover=CONST.DEFAULT.ENTRY.cursor)

    def _generate_surf(self):
        """Generates new surface of appearance.
        Private."""

        I.Image._generate_surf(self)
        # TODO: reorganize

    def _find_intervals(self):
        # noinspection PyTypeChecker
        self.intervals = [0] + [None] * (len(self.text) - 1)
        for i in range(1, len(self.text)):
            self.intervals[i] = self.w_text._font.size(self.text[:i])[0]

    # aliases bound to the attributes of child widgets to support their setting using Entry.set(**kwargs)
    # self
    @property
    def background(self):
        return self.image

    @background.setter
    def background(self, value):
        self.image = value

    # visible_area
    @property
    def cursor_mouseover(self):
        return self.w_visible_area.cursor_mouseover

    @cursor_mouseover.setter
    def cursor_mouseover(self, value):
        self.w_visible_area.set(cursor_mouseover=value, cursor_pressed=value)
        self.w_text.set(cursor=value)
        self.w_highlight.set(cursor=value)
        self.w_cursor.set(cursor=value)

    # cursor
    @property
    def cursor_background(self):
        return self.w_cursor.image

    @cursor_background.setter
    def cursor_background(self, value):
        self.w_cursor.set(image=value)

    # text and highlight
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

    # text
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

    # highlight
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
