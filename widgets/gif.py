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


import pygame as pg
import time
import pygame_widgets.widgets.image as I
import pygame_widgets.constants.private as CONST
from PIL import Image
from pygame_widgets.constants import *


__all__ = ['Gif']


class Gif(I.Image):
    """Witget used to display animated gif"""

    def __init__(self, master, topleft=(0, 0), size=(1, 1), **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, **updated)

        self.image = CONST.DEFAULT.GIF.image
        self.filename = ""
        self._current_frame = 0
        self._frames = list()
        self._ptime = 0  # in milliseconds
        self.running = CONST.DEFAULT.GIF.running
        self.breakpoint = 0
        self.startpoint = 0
        self.reversed = CONST.DEFAULT.GIF.reversed

        self.add_handler(E_LOOP_STARTED, self._animate, self_arg=False, event_arg=False)

        self.pub_arg_dict['Gif_appearance'] = ['filename']
        self.pub_arg_dict['Gif_set'] = ['startpoint', 'breakpoint', 'running', 'reversed']
        self.pub_arg_dict['Image_appearance'].remove('image')

        self._safe_init(**kwargs)

    def __len__(self):
        return len(self._frames)

    def seek(self, frame_number):
        """Set the frame to display.
        Public."""

        self._current_frame = max(min(frame_number, len(self._frames) - 1), 0)
        self.image = self._frames[self._current_frame][0]
        self.update_appearance()
        self._ptime = time.time_ns() // 1000

    def rewind(self):
        """Return to startpoint (or breakpoint if reversed).
        Public."""

        self.seek(self.breakpoint - 1 if self.reversed else self.startpoint)

    def fastforward(self):
        """Return to breakpoint (or startpoint if reversed).
        Public."""

        self.seek(self.startpoint if self.reversed else self.breakpoint - 1)

    def next_frame(self):
        if self.reversed:
            new = self._current_frame - 1
            if new < self.startpoint:
                new = self.breakpoint - 1
        else:
            new = self._current_frame + 1
            if new >= self.breakpoint:
                new = self.startpoint
        self.seek(new)

    def previous_frame(self):
        if self.reversed:
            new = self._current_frame + 1
            if new >= self.breakpoint:
                new = self.startpoint
        else:
            new = self._current_frame - 1
            if new < self.startpoint:
                new = self.breakpoint - 1
        self.seek(new)

    def reset(self):
        """Reset all playback data.
        Public."""

        self.startpoint = 0
        self.breakpoint = len(self)
        self._current_frame = 0
        self.running = CONST.DEFAULT.GIF.running
        self.reversed = CONST.DEFAULT.GIF.reversed
        self.image = self._frames[self._current_frame][0]
        self.update_appearance()
        self._ptime = time.time_ns() // 1000

    def _get_frames(self):
        image = Image.open(self.filename)

        pal = image.getpalette()
        base_palette = []
        for i in range(0, len(pal), 3):
            rgb = pal[i:i+3]
            base_palette.append(rgb)

        all_tiles = []
        try:
            while 1:
                if not image.tile:
                    image.seek(0)
                if image.tile:
                    all_tiles.append(image.tile[0][3][0])
                image.seek(image.tell()+1)
        except EOFError:
            image.seek(0)

        all_tiles = tuple(set(all_tiles))

        try:
            while 1:
                try:
                    duration = image.info["duration"]
                except:
                    duration = 100

                cons = False

                x0, y0, x1, y1 = (0, 0) + image.size
                if image.tile:
                    tile = image.tile
                else:
                    image.seek(0)
                    tile = image.tile
                if len(tile) > 0:
                    x0, y0, x1, y1 = tile[0][1]

                if all_tiles:
                    if all_tiles in ((6,), (7,)):
                        cons = True
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    elif all_tiles in ((7, 8), (8, 7)):
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    else:
                        palette = base_palette
                else:
                    palette = base_palette

                pi = pg.image.fromstring(image.tobytes(), image.size, image.mode)
                pi.set_palette(palette)
                if "transparency" in image.info:
                    pi.set_colorkey(image.info["transparency"])
                pi2 = pg.Surface(image.size, SRCALPHA)
                if cons:
                    for i in self._frames:
                        pi2.blit(i[0], (0, 0))
                pi2.blit(pi, (x0, y0), (x0, y0, x1-x0, y1-y0))

                self._frames.append([pi2, duration])
                image.seek(image.tell()+1)
        except EOFError:
            pass
        self._ptime = time.time_ns() // 1000
        self.rewind()
        self.breakpoint = len(self)

    def _animate(self):
        if not self.running:
            return
        cur_time = time.time_ns() // 1000
        change = False
        while cur_time - self._ptime >= self._frames[self._current_frame][1]:
            if self.reversed:
                self._current_frame -= 1
                if self._current_frame < self.startpoint:
                    self._current_frame = self.breakpoint - 1
            else:
                self._current_frame += 1
                if self._current_frame >= self.breakpoint:
                    self._current_frame = self.startpoint
            change = True
            self._ptime += self._frames[self._current_frame][1]
            cur_time = time.time_ns() // 1000
        if change:
            self.image = self._frames[self._current_frame][0]
            self.update_appearance()

    def _set_update(self, old=None, **kwargs):
        """Actualises its image on the screen after setting new values to attributes in most efficient way.
        Private."""

        if kwargs:
            super()._set_update(old, **kwargs)  # TODO: This calls self.update_appearance() redundantly
            update = False
            for name in kwargs.keys():
                if name in self.pub_arg_dict['Gif_appearance']:
                    self._get_frames()
                    self._correct_bounds()
                    update = True
                elif name == 'running':
                    self._ptime = time.time_ns() // 1000
                elif name in self.pub_arg_dict['Gif_set']:
                    self._correct_bounds()
            if update:
                self.update_appearance()

    def _correct_bounds(self):
        self.startpoint = max(self.startpoint, 0)
        self.breakpoint = max(self.startpoint + 1, min(self.breakpoint, len(self)))
        self._current_frame = max(self.startpoint, min(self._current_frame, self.breakpoint - 1))

    def _set_event(self, old=None, **kwargs):
        """Places events on the queue based on changed attributes.
        Private."""

        if old is None:
            old = dict()
        for name, value in kwargs.items():
            # noinspection PyArgumentList
            self._post_event(pg.event.Event(PYGAME_WIDGETS, ID=E_GIF_APPEARANCE if name in
                                            self.pub_arg_dict['Gif_appearance'] else E_GIF_ATTR, name=name, new=value,
                                            old=old[name] if name in old else None))

    def _generate_surf(self):
        """Generates new surface of appearance.
        Private."""

        if self.auto_res:
            self.my_surf = self.image.copy()
        else:
            self.my_surf = pg.transform.scale(self.image.copy(), self.my_surf.get_size())
        self.my_surf.convert_alpha()
