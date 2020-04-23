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


_post_events = True


def set_mode_init():
    """Stop widgets posting large number of events when initializating, thus setting lots of attributes."""

    global _post_events
    _post_events = False


def set_mode_mainloop():
    """Continue posting events when setting widgets' attributes."""

    global _post_events
    _post_events = True


def get_mode():
    """Returns True, if are widgets allowed to post events, otherwise False."""

    return _post_events
