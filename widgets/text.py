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


import pygame_widgets.widgets.widget as W
import pygame as pg
import pygame_widgets.constants.private as CONST
from pygame_widgets.constants import *
pg.font.init()


__all__ = ['Label']


class _Text(W._Widget):
    """Virtual base widget tor text widgets. Supplies text updating. Cannot be instaned."""

    def __init__(self, master, topleft, size, **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, **updated)
        self._font = None
        self.font_name = CONST.DEFAULT.TEXT.font
        self.font_size = CONST.DEFAULT.TEXT.font_size

        self.bold = CONST.DEFAULT.TEXT.bold
        self.italic = CONST.DEFAULT.TEXT.italic
        self.underlined = CONST.DEFAULT.TEXT.underlined

        self.font_color = CONST.DEFAULT.TEXT.font_color
        self.smooth = CONST.DEFAULT.TEXT.smooth
        self.text = CONST.DEFAULT.TEXT.text
        self.alignment_x = CONST.DEFAULT.TEXT.Alignment.x
        self.alignment_y = CONST.DEFAULT.TEXT.Alignment.y

        self.pub_arg_dict["Text_new_font"] = ["font_name", "font_size"]
        self.pub_arg_dict["Text_set_font"] = ["bold", "italic", "underlined"]
        self.pub_arg_dict["Text_render"] = ["font_color", "smooth", "text", "alignment_x", "alignment_y"]

        self._safe_init(**kwargs)

    def _new_font(self):
        """Creates new pygame._font.Font object according to actual settings.
        Private."""

        self._font = pg.font.SysFont(self.font_name, self.font_size, self.bold, self.italic)
        self._font.set_underline(self.underlined)

    def _set_font(self):
        """Adjusts the current pygame._font.Font object according to actual settings.
        Private."""

        self._font.set_bold(self.bold)
        self._font.set_italic(self.italic)
        self._font.set_underline(self.underlined)

    def _set_update(self, old=None, **kwargs):
        """Actualises its image on the screen after setting new values to attributes in most efficient way.
        Private."""

        if kwargs:
            super()._set_update(old, **kwargs)
            new = False
            set = False
            render = False
            for name in kwargs.keys():
                if name in self.pub_arg_dict["Text_render"]:
                    render = True
                elif name in self.pub_arg_dict["Text_set_font"]:
                    set = True
                elif name in self.pub_arg_dict["Text_new_font"]:
                    new = True
                    break
            if new:
                self._new_font()
            elif set:
                self._set_font()
            if new or set or render:
                self.update_appearance()
            self._set_event(old, **kwargs)


class Label(_Text):
    """Widget with 1-line unchangable text on a solid, transparent or custom background."""

    def __init__(self, master, topleft=(0, 0), size=(1, 1), **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, **updated)
        self.background = CONST.DEFAULT.LABEL.bg

        self.pub_arg_dict["Text_render"].append("background")
        self._new_font()
        self._safe_init(**kwargs)

    def _generate_surf(self):
        """Generates new surface of appearance.
        Private."""

        text = self._font.render(self.text, self.smooth, self.font_color, self.background if not
                                isinstance(self.background, pg.Surface) and not callable(self.background) and
                                                                                             self.background[3] else None)
        if callable(self.background):  # TODO: this option skips self.auto_res, which is problem in Button
            self.my_surf = self.background(self, text)
            return
        if self.auto_res:
            size = text.get_size()
        else:
            size = self.master_rect.size
        if isinstance(self.background, pg.Surface):
            self.my_surf = pg.transform.scale(self.background, size)
        else:
            self.my_surf = pg.Surface(size, SRCALPHA)
            self.my_surf.fill(self.background)
        if self.auto_res:
            self.my_surf.blit(text, (0, 0))
            return
        dest = (self.alignment_x * (self.my_surf.get_width() - text.get_width()) / 2,
                self.alignment_y * (self.my_surf.get_height() - text.get_height()) / 2)
        self.my_surf.blit(text, dest)
        self.my_surf.convert_alpha()

    def _set_event(self, old=None, **kwargs):
        """Places events on the queue based on changed attributes.
        Private."""

        if old is None:
            old = dict()
        for name, value in kwargs.items():
            # noinspection PyArgumentList
            self._post_event(pg.event.Event(PYGAME_WIDGETS, ID=E_LABEL_TEXT if name == 'text' else E_LABEL_ATTR,
                                            name=name, new=value, old=old[name] if name in old else None))
