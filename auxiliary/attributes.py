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


class Attributes:
    """Object for assigning attributes to widgets without worrying about name collision with builtin attributes."""

    def __str__(self):
        """Displays all attributes as dict."""
        return str(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

    def __get__(self, instance, owner):
        """Returns all attributes as a dict."""

        return self

    def __set__(self, instance, value):
        """Clear all saved attributes. Then, if value is a dict, save it to self.__dict__. Any non-iterable object
        will be saved to self.attr0, iterable object will be unpacked and its content saved to
        self.attr0, self.attr1, ..."""

        if isinstance(value, Attributes):
            value = dict(value.__dict__)
        if isinstance(value, dict):
            self.__dict__ = value
            return
        try:
            new = dict()
            for index, item in enumerate(value):
                new[f'attr{index}'] = item
        except TypeError:
            self.__dict__ = {'attr0': value}
        else:
            self.__dict__ = new

    def __delete__(self, instance):
        """Clear all saved attributes."""

        self.clear()

    def __getitem__(self, item):
        """Returns the value of the attribute when given a string name. Integer names are converted to f'attr{item}'
        unless there is the integer as a key in self.__dict__."""

        if isinstance(item, int) and item not in self.__dict__.keys():
            item = f'attr{item}'
        return self.__dict__[item]

    def __setitem__(self, key, value):
        """Sets the attribute by the given name. Names do not have to be strings."""

        self.__dict__[key] = value

    def __delitem__(self, key):
        """Deletes an attribute given by its name. Names do not have to be strings."""

        del self.__dict__[key]

    def __add__(self, other):
        """Adds the name-attribute pairs from other to self.__dict__. Other must be a dict, an instance of Attributes
        or iterable."""

        if isinstance(other, Attributes):
            other = dict(other.__dict__)
        elif not isinstance(other, dict):
            new = dict()
            try:
                for index, value in enumerate(other):
                    new[f'attr{index}'] = value
            except TypeError:
                raise TypeError("'other' must be instance of Attributes, dict or iterable object")
            else:
                other = new
        self.__dict__.update(other)

    def __sub__(self, other):
        """Other can be a dict, iterable or a name of an attribute. This method deletes the attributes given by the
        sequence of names in iterable, or by the sequence of dict keys."""

        if isinstance(other, dict):
            other = other.keys()
        try:
            for key in other:
                if isinstance(key, int):
                    key = f'attr{key}'
                del self.__dict__[key]
        except KeyError:
            pass
        except TypeError:
            try:
                del self.__dict__[other]
            except KeyError:
                pass

    def clear(self):
        """Clear all saved attributes."""

        self.__dict__.clear()

    def toDict(self):
        """Returns all saved attributes as a dict."""

        return dict(self.__dict__)
