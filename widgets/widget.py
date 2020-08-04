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


import sys
import pygame as pg
from pygame_widgets.auxiliary.attributes import Attributes
from pygame_widgets.auxiliary.handler import Handler
from pygame_widgets.auxiliary.cursors import set as set_cursor
import pygame_widgets.constants.private as CONST
from pygame_widgets.constants import *
from pygame_widgets.auxiliary.event_mode import get_mode


__all__ = ['Window']


class _Caller(list):
    """A list of functions that can call all of them  in order.
    Used to initialise child widgets of a compound widget."""

    def __call__(self):
        for func in self:
            if callable(func):
                func()


class _Master:
    """Class for methods present in Window and Widget. If instanced or subclassed, might raise AttributeError."""

    next_ID = 0

    def __init__(self, **kwargs):
        if CONST.SUPER not in kwargs or not kwargs[CONST.SUPER]:
            raise TypeError("Hidden widget _Master instanced")
        self.ID = _Master.next_ID
        _Master.next_ID += 1
        self.children = list()
        self.pub_arg_dict = dict()
        self.pub_arg_dict['special'] = []
        self.visible = True
        self.attr = Attributes()
        self.surface = None
        self.my_surf = None
        self.topleft = (0, 0)
        self.master_rect = Rect(0, 0, 1, 1)
        self.cursor = CONST.DEFAULT.cursor
        self.grab = dict()
        self.handlers = dict()
        self.handler_queue = list()
        self.dont_receive_events = set()
        self.dont_send_events = set()

        self.add_handler(MOUSEMOTION, self._change_cursor, self_arg=False)
        self.add_handler(E_LOOP_STARTED, self._move_queue, self_arg=False, event_arg=False)
        self.pub_arg_dict['Master'] = ['cursor']

    def __str__(self):
        return f'<{str(self.__class__)[8:-2]} object, ID {self.ID}>'

    def __repr__(self):
        return str(self)

    def __del__(self):
        self.delete()

    def delete(self):
        for child in self.children:
            child.delete()

    def _change_cursor(self, event):
        """Default handler for MOUSEMOTION events. It calls cursor updater with correct argument.
        Private."""

        self._update_cursor(event.pos)

    def _move_queue(self):
        """Default handler for E_LOOP_STARTED events. It calls delayed handlers.
        Private."""

        try:
            del self.handler_queue[0]
            for handler, event in self.handler_queue[0]:
                handler(self, event)
        except IndexError:
            pass

    def _update_cursor(self, mousepos):
        """This method is called when mouse moves or widget cursor is changed. It checks whether the mouse is above
        the widget and actualises cursor image.
        Private."""

        if self.get_abs_master_rect().collidepoint(mousepos):
            for child in self.children:
                if child.get_abs_master_rect().collidepoint(mousepos):
                    return
            if isinstance(self, _Widget):
                siblings = self.master.children
                for sibling in siblings[siblings.index(self) + 1:]:
                    if sibling.get_abs_master_rect().collidepoint(mousepos):
                        return
            set_cursor(*self.cursor)

    def get_abs_master_rect(self):
        """This method is overridden in both _Widget and Window. It is here only because PyCharm highlithes its usages
        in _Master."""

        pass

    def add_update(self, rect):
        """This method is overridden in both _Widget and Window. It is here only because PyCharm highlithes its usages
        in _Master."""

        pass

    def get_visibility(self):
        """This method is overridden in both _Widget and Window. It is here only because PyCharm highlithes its usages
        in _Master."""

        pass

    def on_screen(self, rect=None):
        """Returns True if there is its image on current window, otherwise False.
        Public."""
        # TODO: This returns True even if the rect is outside self.master.surface

        if not rect:
            rect = self.get_abs_master_rect()
        if hasattr(self, 'master'):
            b = self.master.surface is not None
        else:
            b = True
        return pg.display.get_surface().get_rect().colliderect(rect) and b

    def add_grab(self, event_type, child, level=0):
        """Child grabs every event of specified type.
        Public."""

        if child not in self.children:
            return
        if event_type not in self.grab.keys():
            self.grab[event_type] = list()
        self.grab[event_type].append(child)
        if level:
            if hasattr(self, 'master'):
                self.master.add_grab(event_type, self, level - 1)

    def remove_grab(self, event_type, child, level=0):
        """Disables grabbing events of event_type by child.
        Public."""

        if child in self.grab[event_type]:
            self.grab[event_type].reverse()
            self.grab[event_type].remove(child)
            self.grab[event_type].reverse()
        if hasattr(self, 'master') and level:
            self.master.remove_grab(event_type, self, level - 1)

    def add_handler(self, event_type, func, args=None, kwargs=None, self_arg=True, event_arg=True, delay=0, index=None):
        """Adds handling function with settings.
        Public."""

        if event_type not in self.handlers:
            self.handlers[event_type] = list()
        if index is None:
            self.handlers[event_type].append(Handler(func, args, kwargs, self_arg, event_arg, delay))
        else:
            self.handlers[event_type].insert(index, Handler(func, args, kwargs, self_arg, event_arg, delay))

    def remove_handler(self, event_type, func, args=None, kwargs=None, self_arg=True, event_arg=True):
        """Removes handling function with settings.
        Public."""

        if args is None:
            args = list()
        if kwargs is None:
            kwargs = dict()
        for handler in self.handlers[event_type].copy():
            if handler.func == func and handler.args == args and handler.kwargs == kwargs and \
               handler.self_arg == self_arg and handler.event_arg == event_arg:
                self.handlers[event_type].remove(handler)

    def get_handlers(self, copy=True):
        """Returns a copy or a reference to the list of handlers. The copy is useles, but with the reference user can
        change the order of handlers. You should know, what you are doing. To add or remove handlers,
        it is recommended to use the add_handler and remove_handler methods.
        Public."""

        if not copy:
            return self.handlers
        copied = dict()
        for event_type, list in self.handlers.items():
            copied[event_type] = [h.copy() for h in list]
        return copied

    def add_nr_events(self, *args):
        for e in args:
            self.dont_receive_events.add(e)

    def remove_nr_events(self, *args):
        for e in args:
            try:
                self.dont_receive_events.remove(e)
            except ValueError:
                pass

    def add_ns_events(self, *args):
        for e in args:
            self.dont_send_events.add(e)

    def remove_ns_events(self, *args):
        for e in args:
            try:
                self.dont_send_events.remove(e)
            except ValueError:
                pass

    """def handle_events(self, *events, _filter=True):
        Function for handling events if possible. For every event, if succesfully handled, returns True, otherwise
        False. Should be called in Window's instance for every event in event queue, especially for pygame.VIDEORESIZE
        and pygame.QUIT.
        Public.

        output = [False] * len(events)
        for index, e in enumerate(events):
            if hasattr(e, 'widget') and e.widget == self and _filter:
                continue

            if not hasattr(e, 'ID'):
                e.ID = e.type
            if e.ID in self.dont_receive_events:
                continue
            if e.ID not in self.dont_send_events:
                if e.ID in self.grab:
                    grab_exists = self.grab[e.ID]
                else:
                    grab_exists = False

                if grab_exists:
                    output[index] = self.grab[e.type][-1].handle_events(e)[0]
                else:
                    for child in self.children:
                        output[index] = child.handle_events(e)[0] or output[index]

            if e.ID in self.handlers:
                if not self.handlers[e.ID]:
                    continue
            else:
                continue

            out = False
            for handler in self.handlers[e.ID]:
                if handler.if_handled or not output[index]:
                    handler(e, self)
                    out = True
            output[index] = out
        return output"""

    def handle_event(self, event, _filter=True):
        if not hasattr(event, 'ID'):
            event.ID = event.type
        if (hasattr(event, 'widget') and event.widget == self and _filter) or event.ID in self.dont_receive_events:
            return
        if event.ID in self.handlers:
            for handler in self.handlers[event.ID]:
                if handler.delay:
                    if len(self.handler_queue) <= handler.delay:
                        self.handler_queue += [list() for _ in range(handler.delay - len(self.handler_queue) + 1)]
                    self.handler_queue[handler.delay].append((handler, event))
                else:
                    handler(self, event)
        if event.ID not in self.dont_send_events:
            if event.ID in self.grab:
                grab_exists = self.grab[event.ID]
            else:
                grab_exists = False

            if grab_exists:
                self.grab[event.ID][-1].handle_event(event)
            else:
                for child in self.children:
                    child.handle_event(event)

    def handle_events(self, *events, _filter=True):
        for event in events:
            self.handle_event(event, _filter)

    def _post_event(self, event):
        """Method that posts signed event and immediatelly handles it (when the event gets to the handling process
        by use of Window.handle_events(), it will be automatically filtered out).
        Private."""

        if not get_mode():
            return
        if event.type == PYGAME_WIDGETS:
            event.widget = self
            self.handle_event(event, _filter=False)
        pg.event.post(event)

    def kwarg_list(self):
        """Returns the list of all setable attributes.
        Public."""

        return sum(self.pub_arg_dict.values(), [])

    def blit(self, rect=None, _update=True):
        """Blits the surface of appearance to the master's surface's subsurface. If rect, actualises only children
        colliding with the rect.
        Can be called by master or child.
        Private."""

        # TODO: in special cases can be self.surface == None while not returning in first condition. In that case the method falls.
        if not self.get_visibility() or not self.on_screen():
            return
        if rect is None:
            rect = self.surface.get_rect()
        else:
            rect = rect.move(self.topleft).clip(self.surface.get_rect())
            if not rect:
                return
        old_clip = self.surface.get_clip()
        self.surface.set_clip(rect)
        self.surface.blit(self.my_surf, self.topleft)
        self.surface.set_clip(old_clip)
        if _update:
            self.add_update(rect.move(*self.surface.get_abs_offset()))
        rect.move_ip(*[-a for a in self.topleft])
        for child in self.children:
            if child.master_rect.colliderect(rect):
                child.blit(rect.move(*[-a for a in child.master_rect.topleft]), _update=False)

    def _redraw_child_reccurent(self, abs_clip, path):
        """Reccurent function used to disappear widget.
        Is called by child or master.
        Private."""

        clip = abs_clip.move(*[-a for a in self.get_abs_master_rect().topleft])
        old_clip = self.surface.get_clip()
        self.surface.set_clip(clip.move(*self.topleft))
        self.surface.blit(self.my_surf, self.topleft)
        self.surface.set_clip(old_clip)
        for child in self.children:
            if child.master_rect.colliderect(clip) and child != path[0]:
                child.blit(clip.move(*[-a for a in child.master_rect.topleft]))
            elif child == path[0] and len(path) > 1:
                # noinspection PyProtectedMember
                child._redraw_child_reccurent(abs_clip, path[1:])

    def set(self, **kwargs):
        """Sets the keyword arguments and actualises the surface of appearance and the image on the screen.
        Public."""

        old = dict()
        for name, value in kwargs.items():
            if name in self.kwarg_list():
                if name in self.pub_arg_dict['special']:  # TODO: special attributes could be implemented using property
                    self._set_special(name, value)
                else:
                    old[name] = getattr(self, name, None)
                    setattr(self, name, value)
        self._set_update(old, **kwargs)

    def _set_update(self, old=None, **kwargs):
        """Actualises its image on the screen after setting new values to attributes in most efficient way.
        Private."""

        for name in kwargs.keys():
            if name == 'cursor':
                self._update_cursor(pg.mouse.get_pos())

    def _set_special(self, name, value):
        """Manages settings that require some special action instead of changing attributes of self.
        Private."""

        pass


class Window(_Master):
    """The main master. Causes problems if instanced multiple times."""

    def __init__(self, resolution=(0, 0), flags=0, depth=0, **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(**updated)
        self.add_handler(VIDEORESIZE, self._resize, self_arg=False)
        self.add_handler(QUIT, self.quit, self_arg=False, event_arg=False)
        self.add_handler(KEYDOWN, self._AltF4, self_arg=False)
        self.min_size = (None, None)
        self.max_size = (None, None)
        self.bg_color = CONST.DEFAULT.WINDOW.color
        self.surf_args = (flags | SRCALPHA, depth)
        self.surface = pg.display.set_mode(resolution, *self.surf_args)
        self.my_surf = pg.Surface(self.surface.get_size(), SRCALPHA)
        self.my_surf.fill(self.bg_color)
        self.my_surf.convert_alpha()
        self.to_update = list()
        self.pub_arg_dict['Window_attr'] = ['fps', 'bg_color']
        self.pub_arg_dict['Window_resize'] = ['min_size', 'max_size']
        self.pub_arg_dict['special'].extend(['title', 'icon_title', 'icon', 'size'])
        self.fps = CONST.DEFAULT.WINDOW.fps
        self.clock = pg.time.Clock()

        self.set(**kwargs)
        self.blit()

    def quit(self, code=0):
        """Default handler for pygame.QUIT event.
        Public."""

        self.delete()
        pg.quit()
        sys.exit(code)

    def _AltF4(self, event):
        """Default handler for pygame.KEYDOWN event. Quits if Alt + F4 is pressed.
        Private."""

        if event.key == K_F4 and (event.mod & KMOD_LALT):
            self.quit()

    def update_display(self):
        """Draws the recent changes of self.surface on the display.
        Some form of updating display should be called in every mainloop cycle.
        Public."""

        if self.to_update:
            pg.display.update(self.to_update)
            self.to_update = list()
        self.clock.tick(self.fps)

    def get_fps(self):
        return self.clock.get_fps()

    def _resize(self, event):
        """Default handler for Pygame.VIDEORESIZE event.
        Private."""

        if event.size != self.surface.get_size() or self._repair_size(event.size) != self.surface.get_size():
            self.surface = pg.display.set_mode(self._repair_size(event.size), *self.surf_args)
            self.my_surf = pg.Surface(self.surface.get_size(), SRCALPHA)
            self.my_surf.fill(self.bg_color)
            for child in self.children:
                child.reconnect()
                child._generate_surf()
                if child.master_rect.size != child.my_surf.get_size():
                    """child.disappear()
                    child.master_rect.size = child.my_surf.get_size()
                    child._create_subsurface()"""
                    child.move_resize(resize=child.my_surf.get_size(), resize_rel=False)
            self.blit(self.surface.get_rect())
            self.add_update(self.surface.get_rect())

    def _repair_size(self, size):
        """Change the size so that it is in defined limits.
        Private."""

        size = list(size)
        for i in range(2):
            if self.min_size[i] is not None:
                size[i] = max(size[i], self.min_size[i])
            if self.max_size[i] is not None:
                size[i] = min(size[i], self.max_size[i])
        return tuple(size)

    def get_visibility(self):
        """Screen is always visible, so this method returns True. This may change in the future.
        Public."""

        return True

    def add_update(self, rect=None):
        """Adds update rect to the to_update list.
        Public."""

        if not rect:
            rect = self.get_abs_master_rect()
        if self.on_screen(rect):
            self.to_update.append(self.surface.get_rect().clip(rect))

    def get_abs_master_rect(self):
        """This is here for compatibility with some methods of Master_.
        Public."""

        return self.surface.get_rect()

    def get_abs_surf_rect(self):
        """This is here for compatibility with some methods of Master_.
        Public."""

        return self.surface.get_rect()

    def change_surface(self, surf, dest=(0, 0), area=None, special_flags=0):
        """Used to change part of window background.
        Public."""

        surf.convert_alpha()
        self.my_surf.blit(surf, dest, area, special_flags)
        self.blit()
        # self.surface.blit(self.my_surf, (0, 0))
        # self.to_update.append(Rect(dest, surf.get_size()))
        # for child in self.children:
        #     if child.master_rect.colliderect(Rect(dest, surf.get_size())):
        #         child.blit()

    """def set(self, **kwargs):
        Sets the keyword arguments and actualises the surface of appearance and the image on the screen.
        Public.

        old = dict()
        for name, value in kwargs.items():
            if name in self.kwarg_list():
                if name in self.pub_arg_dict['special']:
                    self._set_special(name, value)
                else:
                    old[name] = getattr(self, name, None)
                    setattr(self, name, value)
        self._set_update(old, **kwargs)"""

    def _set_update(self, old=None, **kwargs):
        """Actualises its image on the screen after setting new values to attributes in most efficient way.
        Private."""

        if old is None:
            old = dict()
        if kwargs:
            super()._set_update(old, **kwargs)
            res = False
            for name in kwargs.keys():
                if name in self.pub_arg_dict['Window_resize']:
                    res = True
                elif name == 'bg_color':
                    self.my_surf.fill(self.bg_color)
                    self.blit()
            if res:
                res = self.surface.get_size()
                self._post_event(pg.event.Event(VIDEORESIZE, size=res, w=res[0], h=res[1]))
            self._set_event(old, **kwargs)

    # noinspection PyMethodMayBeStatic
    def _set_special(self, name, value):
        """Manages settings that require some special action instead of changing attributes of self.
        Private."""

        super()._set_special(name, value)
        if name == 'size':
            pg.event.post(pg.event.Event(VIDEORESIZE, size=value, w=value[0], h=value[1]))
        elif name == 'title':
            pg.display.set_caption(value)
        elif name == 'icontitle':
            pg.display.set_caption(pg.display.get_caption()[0], value)
        elif name == 'icon':
            pg.display.set_icon(value)

    # noinspection PyMethodMayBeStatic
    def _set_event(self, old=None, **kwargs):
        """Places events on the queue based on changed attributes.
        Private."""

        if old is None:
            old = dict()
        for name, value in kwargs.items():
            self._post_event(pg.event.Event(PYGAME_WIDGETS, ID=E_WINDOW_ATTR, name=name, new=value,
                                            old=old[name] if name in old else None))


class _Widget(_Master):
    """Base for every other widget. Supplies comunication with children and parents, moving and displaying.
    Cannot be instanced."""

    def __init__(self, master, topleft, size, **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(**updated)
        self.pub_arg_dict["Widget_attr"] = ["auto_res"]
        self.pub_arg_dict["special"].extend(["visible"])
        self.master = master
        self.auto_res = False
        self.visible = True
        self.connected = True
        self._child_init = _Caller()
        self.master_rect = Rect(topleft, size)  # TODO: implement getter of master_rect, surface, mysurf etc.
        self._create_subsurface()
        self.master.children.append(self)
        self.my_surf = pg.Surface(size, SRCALPHA)
        self._safe_init(**kwargs)

    def delete(self):
        for child in self.children:
            child.delete()
        self.children.clear()
        try:
            self.disconnect()
        except Exception:
            pass
        self.master = None

    def get_abs_master_rect(self):
        """Returns the rectangle of used space in absolute master's surface.
        Public."""

        rect = self.master_rect.move(*self.master.get_abs_master_rect().topleft)
        return rect

    def get_abs_surf_rect(self):
        """Returns the rectangle of actual used space in the window. If it is not inside the window surface,
        returns 0-sized rectangle.
        Public."""

        try:
            surf_rect = self.surface.get_rect().move(self.surface.get_abs_offset())
        except AttributeError:
            surf_rect = Rect(0, 0, 0, 0)
        return surf_rect

    def get_abs_master_path(self):
        """Returns the list of masters sorted from top-level.
        Public."""

        master = self.master
        path = list()
        try:
            while True:
                path.append(master)
                master = master.master
        except AttributeError:
            pass
        path.reverse()
        return path

    def get_visibility(self):
        """Returns True if all master widgets and self are visible, otherwise False.
        Public"""

        return self.visible and self.master.get_visibility()

    def _generate_surf(self):
        """Generates new surface of appearance.
        Private."""

        self.my_surf = pg.Surface(self.master_rect.size, SRCALPHA)

    def update_appearance(self):
        old_surf = self.my_surf.copy()
        self._generate_surf()
        if old_surf.get_size() != self.my_surf.get_size():
            self.move_resize(resize=self.my_surf.get_size(), resize_rel=False)
        elif old_surf != self.my_surf:
            self.appear()

    def _create_subsurface(self):
        """Tries to create a subsurface and actualise topleft.
        Private."""

        if self.on_screen():
            rect = self.master.surface.get_rect().clip(
                self.master_rect.move(*[self.master.topleft[i] for i in range(2)]))  # TODO: This should be *self.master.topleft
            if rect.size != (0, 0):
                self.surface = self.master.surface.subsurface(rect)
                self.topleft = [self.master_rect.topleft[i] -
                                (rect.topleft[i] - self.master.topleft[i]) for i in range(2)]
                return
        self.surface = None
        self.topleft = (0, 0)

    def _safe_init(self, **kwargs):
        """Searches for non-generate arg, if not found, generates surface. Useful for distinguishing the initialisation
        of user-requested instance and initialisation of the super() of it.
        Private."""

        if CONST.SUPER in kwargs:
            if kwargs[CONST.SUPER]:
                return
        self._child_init()
        self.set(**kwargs)
        self._generate_surf()
        if self.master_rect.size != self.my_surf.get_size():
            self.master_rect.size = self.my_surf.get_size()
            self._create_subsurface()
        self.appear()

    def appear(self):
        """Method used to draw widget on the screen properly.
        Public."""

        if self.connected and self.on_screen() and self.get_visibility():
            self.get_abs_master_path()[0].blit(self.get_abs_master_rect())
            self._update_cursor(pg.mouse.get_pos())

    def disappear(self):
        """Method used to redraw widget by other widgets. It could cause problems if not used carefully.
        Private."""

        if self.connected and self.on_screen():
            path = self.get_abs_master_path()
            # noinspection PyProtectedMember
            path[0]._redraw_child_reccurent(self.get_abs_master_rect().clip(pg.display.get_surface().get_rect()),
                                            path[1:] + [self])
            self.add_update()

    def add_update(self, rect=None):
        """Used to add a child's rectrangle into the 'to_update' list of the window.
        Can be called by a child.
        Private."""

        if not rect:
            rect = self.get_abs_master_rect()
        if self.get_abs_master_rect().colliderect(rect) and self.on_screen(rect):
            self.master.add_update(self.get_abs_master_rect().clip(rect))

    def reconnect(self):
        """Used to actualise the connections of subsurfaces
        (makes self.surface to be a subsurface of self.master.surface if possible).
        Can be called by master.
        Public."""

        self.connected = True
        self._create_subsurface()
        if self not in self.master.children:
            self.master.children.append(self)
        for child in self.children:
            child.reconnect()
        self.appear()

    def disconnect(self):
        """Disconnets its surface from master's surface and redraws itself. It will no longer receive events.
        Public."""

        if not self.connected:
            return
        self.disappear()
        self.master.children.remove(self)
        self.surface = self.my_surf.copy()
        self.topleft = (0, 0)
        self.connected = False
        for child in self.children:
            child.reconnect()

    """def set(self, **kwargs):
        Sets the keyword arguments and actualises the surface of appearance and the image on the screen.
        Public.

        old = dict()
        for name, value in kwargs.items():
            if name in self.kwarg_list():
                if name in self.pub_arg_dict['special']:
                    self._set_special(name, value)
                else:
                    old[name] = getattr(self, name, None)
                    setattr(self, name, value)
        self._set_update(old, **kwargs)"""

    def _set_update(self, old=None, **kwargs):
        """Actualises its image on the screen after setting new values to attributes in most efficient way.
        Private."""

        super()._set_update(old, **kwargs)

        """if kwargs:
            old_surf = self.my_surf.copy()
            self._generate_surf()
            if old_surf.get_size() != self.my_surf.get_size():
                self.move_resize(resize=self.my_surf.get_size(), resize_rel=False, update_surf=False)
            elif old_surf != self.my_surf:
                self.appear()
            self._set_event(old, **kwargs)"""

    def _set_special(self, name, value):
        """Does special actions when changing special attributes.
        Private."""

        super()._set_special(name, value)
        if name == 'visible' and value != self.visible:
            self.visible = value
            if value:
                self.appear()
            else:
                self.disappear()

    def _set_event(self, old=None, **kwargs):
        """Places events on the queue based on changed attributes.
        Private."""

        if old is None:
            old = dict()
        for name, value in kwargs.items():
            self._post_event(pg.event.Event(PYGAME_WIDGETS, ID=E_WIDGET_ATTR, name=name, new=value,
                                            old=old[name] if name in old else None))

    def move_resize(self, move=(0, 0), move_level=0, resize=(1, 1), resize_rel=True, update_surf=True):
        """Moves its subsurface inside master's surface to the given position and resizes it.
        Negative move_level means absolute coordinates, 0 means relative.
        Public."""

        size = self.master_rect.size
        if resize_rel:
            resize = [resize[i] * size[i] for i in range(2)]

        if self.connected:
            if move_level == 0:
                move = [move[i] + self.master_rect.topleft[i] for i in range(2)]
            elif move_level < 0:
                move = [move[i] - self.master.get_abs_master_rect().topleft[i] for i in range(2)]
            else:
                master = self.master
                for _ in range(move_level - 1):
                    move = [move[i] - master.master_rect.topleft[i] for i in range(2)]
                    try:
                        master = master.master
                    except AttributeError:
                        break
            rect = Rect(move, resize)
            self.disappear()
            self.master_rect = rect
            self._create_subsurface()
        else:
            if move_level == 'rel':
                self.master_rect.move_ip(*move)
            else:
                self.master_rect.topleft = move
            self.master_rect.size = resize
            self.surface = pg.Surface(resize, SRCALPHA)
        if update_surf:
            self._generate_surf()
            if self.master_rect.size != self.my_surf.get_size():
                self.master_rect.size = self.my_surf.get_size()
                self._create_subsurface()
        for child in self.children:
            child.reconnect()
        self.appear()
