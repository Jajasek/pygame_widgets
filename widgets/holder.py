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


__all__ = ['Holder']


class _RowLayout:
    def __init__(self, master, vertical=True, size=(0, 0),
                 relative_position=((0, "left", None, "left"), (0, "top", None, "top")), identical_cells=True):
        # (x, side of self, widget or layout to compare, side of it)
        self.master = master
        self.widgets = list()
        self.vertical = vertical
        self.size = list(size)
        self.resizable = tuple([not bool(s) for s in size])
        self.position = relative_position
        self.identical_cells = identical_cells

    def add_widgets(self, *widgets):
        for w in widgets:
            if w not in self.widgets and w.master == self.master:
                self.widgets.append(w)
        self.reorganize()

    def remove_widgets(self, *widgets):
        for w in widgets:
            try:
                self.widgets.remove(w)
            except ValueError:
                pass
        self.reorganize()

    def position_in_master(self, *cycle_handling):
        """Used to determine the actual position in master accoding to the refered objects or to check the attribute
        'relative_position'.
        Public."""
        if self in cycle_handling:
            raise RecursionError(f"The layouts of {self} refer to each other.")
        output = [0, 0]
        for i in range(2):
            distance = self.position[i][0]
            # noinspection PyShadowingBuiltins
            object = self.position[i][2]
            if object is None:
                output[i] = distance if self.position[i][1] in "topleft" \
                    else distance - self.size[i]
            elif isinstance(object, _RowLayout):
                if self.master == object.master:
                    pos = object.position_in_master(*cycle_handling, self)[i]
                    pos = pos + distance if self.position[i][3] in "topleft" else pos + object.size[i] + distance
                    output[i] = pos if self.position[i][1] in "topleft" else pos - self.size[i]
                else:
                    raise AttributeError("The refered layout does not have the same Master.")
            elif isinstance(object, W._Widget):
                if self.master == object.master:
                    pos = object.surface.get_offset()[i]
                    pos = pos + distance if self.position[i][3] in "topleft" else \
                        pos + object.surface.get_size()[i] + distance
                    output[i] = pos if self.position[i][1] in "topleft" else pos - self.size[i]
                else:
                    raise AttributeError("The refered widget does not have the same Master.")
            else:
                raise ReferenceError("The refered object is not valid.")
        return output

    def reorganize(self):
        x, y = self.position_in_master()
        if self.identical_cells:
            cell_size = [0, 0]
            for widget in self.widgets:
                cell_size[0] = max(cell_size[0], widget.surface.get_size()[0])
                cell_size[1] = max(cell_size[1], widget.surface.get_size()[1])
            if self.resizable[int(self.vertical)]:
                self.size[int(self.vertical)] = len(self.widgets) * cell_size[int(self.vertical)]
            if self.resizable[int(not self.vertical)]:
                self.size[int(not self.vertical)] = cell_size[int(not self.vertical)]
            for i, w in enumerate(self.widgets):
                w.move_resize(move=(x + (i * cell_size[0] * int(self.vertical)),
                                    y + (i * cell_size[1] * int(not self.vertical))), move_level=1, update_surf=False)
        else:
            size = tuple([sum([w.surface.get_size()[int(self.vertical)] for w in self.widgets], []),
                          max([w.surface.get_size()[int(not self.vertical)] for w in self.widgets])])
            resize = 1
            if self.resizable[int(self.vertical)]:
                self.size = size[int(self.vertical)]
            else:
                resize = self.size[int(self.vertical)] / size[int(self.vertical)]
            if self.resizable[int(not self.vertical)]:
                self.size = size[int(not self.vertical)]
            next_pos = 0
            r = [1, 1]
            r[int(self.vertical)] = resize
            for w in self.widgets:
                w.move_resize(move=(x + (next_pos * int(self.vertical)), y + (next_pos * int(not self.vertical))),
                              move_level=1, resize=r)
                next_pos += w.surface.get_size()[int(self.vertical)]
        self.master.add_update()


class Holder(W._Widget):
    """Transparent widget, which can hold other widgets and organize their positions and sizes."""

    def __init__(self, master, topleft=(0, 0), size=(1, 1), **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, **updated)
        self.pub_arg_dict['Holder_attr'] = ['color']
        self.layouts = list()
        self.color = THECOLORS['transparent']
        self._safe_init(**kwargs)

    def _set_update(self, old=None, **kwargs):
        """Actualises its image on the screen after setting new values to attributes in most efficient way.
        Private."""

        if kwargs:
            super()._set_update(old, **kwargs)
            update = False
            for name in kwargs.keys():
                if name in self.pub_arg_dict['Holder_attr']:
                    update = True
            if update:
                self._generate_surf()
                self.appear()

    def _set_event(self, old=None, **kwargs):
        """Places events on the queue based on changed attributes.
        Private."""

        if old is None:
            old = dict()
        for name, value in kwargs.items():
            self._post_event(pg.event.Event(PYGAME_WIDGETS, ID=E_HOLDER_ATTR, name=name, new=value,
                                            old=old[name] if name in old else None))

    def _generate_surf(self):
        """Generates new surface of appearance.
        Private."""

        self.my_surf = pg.Surface(self.master_rect.size, SRCALPHA)
        self.my_surf.fill(self.color)
        self.my_surf.convert_alpha()

    def create_row_layout(self, *widgets, vertical=True, size=(0, 0),
                          relative_position=((0, "left", None, "left"), (0, "top", None, "top")), identical_cells=True):
        if not CONST.DEBUG:
            raise NotImplementedError("This feature is not implemented yet.")
        w = list(widgets)
        for widget in widgets:
            if (widget not in self.children) or (widget in sum([l.widgets for l in self.layouts], [])):
                w.remove(widget)
        layout = _RowLayout(self, vertical, size, relative_position, identical_cells)
        layout.add_widgets(*w)
        return layout
