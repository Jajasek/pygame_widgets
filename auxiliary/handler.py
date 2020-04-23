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


class Handler:
    def __init__(self, func, args=None, kwargs=None, self_arg=True, event_arg=True, delay=0):
        self.func = func
        self.args = list(args) if args is not None else list()
        self.kwargs = dict() if kwargs is None else kwargs
        self.self_arg = self_arg
        self.event_arg = event_arg
        self.delay = delay

    def __call__(self, widget, event):
        args = list()
        if self.self_arg:
            args.append(widget)
        if self.event_arg:
            args.append(event)
        args += self.args
        self.func(*args, **self.kwargs)

    def copy(self):
        return Handler(self.func, self.args, self.kwargs, self.self_arg, self.event_arg, self.delay)
