import pygame as pg
from pygame_widgets.auxiliary.attributes import Attributes
from pygame_widgets.auxiliary.handler import Handler
import pygame_widgets.constants.private as CONST
from pygame_widgets.constants.public import *


class _Master:
    """Class for methods present in Window and Widget. If instanced or subclassed, might raise AttributeError."""

    next_ID = 0

    def __init__(self):
        self.ID = _Master.next_ID
        _Master.next_ID += 1
        self.children = list()
        self.pub_arg_dict = dict()
        self.pub_arg_dict['special'] = []
        self.visible = True
        self.attributes = Attributes()
        self.surface = None
        self.my_surf = None
        self.topleft = (0, 0)
        self.master_rect = Rect(0, 0, 1, 1)
        self.grab = dict()  # [event_type: [Child, ...]]
        self.handlers = dict()  # [event_type: [(func, [arg1, ...], include_event_arg, /
        #                                       call_if_handled_by_children), ...]]
        self.no_receive_events = set()
        self.no_send_events = set()

    def __str__(self):
        return f'<{str(self.__class__)[8:-2]} object, ID {self.ID}>'

    def _on_screen(self, rect=None):
        """Returns True if there is its image on current window, otherwise False.
        Private."""

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

    def add_handler(self, event_type, func, args=None, kwargs=None, self_arg=True, event_arg=True,
                    call_if_handled_by_children=False):
        """Adds handling function with settings.
        Public."""

        if event_type not in self.handlers:
            self.handlers[event_type] = list()
        self.handlers[event_type].append(Handler(func, args, kwargs, self_arg, event_arg, call_if_handled_by_children))

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
        """Returns a copy or a pointer to the list of handlers. The copy is useles, but with the pointer can user
        change the order of handlers. You should know, what you are doing. To add or remove handlers,
        it is reccomended to use the add_handler and remove_handler methods.
        Public."""
        return self.handlers.copy() if copy else self.handlers

    def add_nr_events(self, *args):
        for e in args:
            self.no_receive_events.add(e)

    def remove_nr_events(self, *args):
        for e in args:
            try:
                self.no_receive_events.remove(e)
            except ValueError:
                pass

    def add_ns_events(self, *args):
        for e in args:
            self.no_send_events.add(e)

    def remove_ns_events(self, *args):
        for e in args:
            try:
                self.no_send_events.remove(e)
            except ValueError:
                pass

    def handle_events(self, *events, filter=True):
        """Function for handling events if possible. For every event, if succesfully handled, returns True, otherwise
        False. Should be called in Window's instance for every event in event queue, especially for pygame.VIDEORESIZE
        and pygame.QUIT.
        Public."""

        output = [False] * len(events)
        for index, e in enumerate(events):
            try:
                if e.widget == self and filter:
                    continue
            except AttributeError:
                pass

            if e.type in self.no_receive_events:
                continue
            if e.type not in self.no_send_events:
                try:
                    grab_exists = bool(self.grab[e.type])
                except KeyError:
                    grab_exists = False

                if grab_exists:
                    output[index] = self.grab[e.type][-1].handle_events(e)[0]
                else:
                    for child in self.children:
                        output[index] = child.handle_events(e)[0] or output[index]

            try:
                if not self.handlers[e.type]:
                    continue
            except KeyError:
                continue

            out = False
            for handler in self.handlers[e.type]:
                if handler.if_handled or not output[index]:
                    handler(e, self)
                    out = True
            output[index] = out
        return output

    def _post_event(self, event):
        """Method that posts signed event and immediatelly handles it (when the event gets to the handling process
        by use of Window.handle_events(), it will be automatically filtered out).
        Private."""

        if event.type not in CONST.PYGAME_EVENTS:
            event.widget = self
            self.handle_events(event, filter=False)
        pg.event.post(event)

    def kwarg_list(self):
        """Returns the list of all setable attributes.
        Public."""

        return sum(self.pub_arg_dict.values(), [])

    def blit(self, rect=None):
        """Blits the surface of appearance to the master's surface's subsurface. If rect, actualises only children
        colliding with the rect.
        Can be called by master or child.
        Private."""

        if not self.visible or not self._on_screen():
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
        self.add_update(rect.move(*self.surface.get_abs_offset()))
        rect.move_ip(*[-a for a in self.topleft])
        for child in self.children:
            if child.master_rect.colliderect(rect):
                child.blit(rect.move(*[-a for a in child.master_rect.topleft]))

    def redraw_child_reccurent(self, abs_clip, path):
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
                child.redraw_child_reccurent(abs_clip, path[1:])


class Window(_Master):
    """The main master. Causes problems if instanced multiple times."""

    def __init__(self, resolution=(0, 0), flags=0, depth=0, **kwargs):
        super().__init__()
        self.add_handler(VIDEORESIZE, self._resize, self_arg=False, call_if_handled_by_children=True)
        self.add_handler(QUIT, self.quit, self_arg=False, event_arg=False, call_if_handled_by_children=True)
        self.add_handler(KEYDOWN, self._AltF4, self_arg=False, call_if_handled_by_children=True)
        self.min_size = (None, None)
        self.max_size = (None, None)
        self.bg_color = CONST.DEFAULT.WINDOW.color
        self.surf_args = (flags | SRCALPHA, depth)
        self.surface = pg.display.set_mode(resolution, *self.surf_args)
        self.my_surf = pg.Surface(self.surface.get_size(), SRCALPHA)
        self.my_surf.fill(self.bg_color)
        self.my_surf.convert_alpha()
        self.to_update = list()
        self.pub_arg_dict['Window_attr'] = ['fps', 'background']
        self.pub_arg_dict['Window_resize'] = ['min_size', 'max_size']
        self.pub_arg_dict['special'].extend(['title', 'icon_title', 'icon', 'size'])
        self.fps = CONST.DEFAULT.WINDOW.fps
        self.clock = pg.time.Clock()

        self.set(**kwargs)
        self.blit()

    @staticmethod
    def quit(code=0):
        """Default handler for pygame.QUIT event.
        Public."""

        # noinspection PyUnresolvedReferences
        pg.quit()
        exit(code)

    def _AltF4(self, event):
        """Default handler for pygame.KEYDOWN event. Quits if Alt + F4 is pressed.
        Private."""

        if event.key == K_F4 and (event.mod & KMOD_LALT):
            self.quit()

    def update_display(self):
        """Draws the recent changes of self.surface on the display.
        Some form of updating display should be called in every mainloop cycle.
        Public."""

        pg.display.update(self.to_update)
        self.to_update = list()
        self.clock.tick(self.fps)

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

    def add_update(self, rect):
        """Adds update rect to the to_update list.
        Public."""

        if self._on_screen(rect):
            self.to_update.append(self.surface.get_rect().clip(rect))
            return True
        return False

    def get_abs_master_rect(self):
        """This is here for compatibility with some methods of Master_.
        Public."""

        return self.surface.get_rect()

    def get_abs_surf_rect(self):
        """This is here for compatibility with some methods of Master_.
        Public."""

        return self.surface.get_rect()

    def change_surface(self, surf, dest=(0, 0)):
        """Used to change part of window background.
        Public."""

        surf.convert_alpha()
        self.my_surf.blit(surf, dest)
        self.blit()
        # self.surface.blit(self.my_surf, (0, 0))
        # self.to_update.append(Rect(dest, surf.get_size()))
        # for child in self.children:
        #     if child.master_rect.colliderect(Rect(dest, surf.get_size())):
        #         child.blit()

    def set(self, **kwargs):
        """Sets the keyword arguments and actualises the surface of appearance and the image on the screen.
        Public."""

        old = dict()
        for name, value in kwargs.items():
            if name in self.kwarg_list():
                if name in self.pub_arg_dict['special']:
                    self._set_special(name, value)
                else:
                    old[name] = getattr(self, name, None)
                    setattr(self, name, value)
        self._set_update(old, **kwargs)

    def _set_update(self, old=None, **kwargs):
        """Actualises its image on the screen after setting new values to attributes in most efficient way.
        Private."""

        if old is None:
            old = dict()
        if kwargs:
            res = False
            for name in kwargs.keys():
                if name in self.pub_arg_dict['Window_resize']:
                    res = True
                elif name == 'background':
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
            self._post_event(pg.event.Event(E_WINDOW_ATTR, name=name, new=value, old=old[name] if name in old else None))


class _Widget(_Master):
    """Base for every other widget. Supplies comunication with children and parents, moving and displaying.
    Cannot be instanced."""

    def __init__(self, master, topleft, size, **kwargs):
        super().__init__()
        self.pub_arg_dict["Widget_attr"] = ["auto_res"]
        self.pub_arg_dict["special"].extend(["visible"])
        self.master = master
        self.auto_res = False
        self.visible = True
        self.connected = True
        self.master_rect = Rect(topleft, size)
        self._create_subsurface()
        self.master.children.append(self)
        self.my_surf = pg.Surface(size, SRCALPHA)
        self._safe_init(**kwargs)

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

    def _generate_surf(self):
        """Generates new surface of appearance.
        Private."""

        self.my_surf = pg.Surface(self.master_rect.size, SRCALPHA)

    def _create_subsurface(self):
        """Tries to create a subsurface and actualise topleft.
        Private."""

        if self._on_screen():
            rect = self.master.surface.get_rect().clip(
                self.master_rect.move(*[self.master.topleft[i] for i in range(2)]))
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
        self.set(**kwargs)
        self._generate_surf()
        if self.master_rect.size != self.my_surf.get_size():
            self.master_rect.size = self.my_surf.get_size()
            self._create_subsurface()
        self.appear()

    def appear(self):
        """Method used to draw widget on the screen properly.
        Public."""

        if self.connected and self._on_screen() and self.visible:
            self.get_abs_master_path()[0].blit(self.get_abs_master_rect())

    def disappear(self):
        """Method used to redraw widget by other widgets. It could cause problems if not used carefully.
        Private."""

        if self.connected and self._on_screen():
            path = self.get_abs_master_path()
            path[0].redraw_child_reccurent(self.get_abs_master_rect().clip(pg.display.get_surface().get_rect()),
                                           path[1:] + [self])
            self.add_update()

    def add_update(self, rect=None):
        """Used to add a child's rectrangle into 'to_update' list of the window.
        Returns True if succesful, otherwise False.
        Can be called by a child.
        Private."""

        if not rect:
            rect = self.get_abs_master_rect()
        if self.get_abs_master_rect().colliderect(rect) and self._on_screen(rect):
            return self.master.add_update(self.get_abs_master_rect().clip(rect))
        return False

    def reconnect(self, rect=None, abs_rect=False):
        """Used to actualise the connections of subsurfaces
        (makes self.surface to be a subsurface of self.master.surface if possible).
        Can be called by master.
        Public."""

        if not rect:
            rect = self.master_rect
        if abs_rect:
            rect.move_ip(*[-i for i in self.master.get_abs_master_rect().topleft])
        self.master_rect = rect
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

    def set(self, **kwargs):
        """Sets the keyword arguments and actualises the surface of appearance and the image on the screen.
        Public."""

        old = dict()
        for name, value in kwargs.items():
            if name in self.kwarg_list():
                if name in self.pub_arg_dict['special']:
                    self._set_special(name, value)
                else:
                    old[name] = getattr(self, name, None)
                    setattr(self, name, value)
        self._set_update(old, **kwargs)

    def _set_update(self, old=None, **kwargs):
        """Actualises its image on the screen after setting new values to attributes in most efficient way.
        Private."""

        if kwargs:
            old_surf = self.my_surf.copy()
            self._generate_surf()
            if old_surf.get_size() != self.my_surf.get_size():
                self.move_resize(resize=self.my_surf.get_size(), resize_rel=False, update_surf=False)
            elif old_surf != self.my_surf:
                self.appear()
            self._set_event(old, **kwargs)

    def _set_special(self, name, value):
        """Does special actions when changing special attributes.
        Private."""

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
            self._post_event(pg.event.Event(E_WIDGET_ATTR, name=name, new=value, old=old[name] if name in old else None))

    def move_resize(self, move=(0, 0), move_level: int = 'rel', resize=(1, 1), resize_rel=True, update_surf=True):
        """Moves its subsurface inside master's surface to the given position and resizes it.
        move_level is an integer or one of strings 'abs' and 'rel'.
        Public."""

        size = self.master_rect.size
        if resize_rel:
            resize = [resize[i] * size[i] for i in range(2)]

        if self.connected:
            if move_level == 'rel':
                move = [move[i] + self.master_rect.topleft[i] for i in range(2)]
            elif move_level == 'abs':
                move = [move[i] - self.master.get_abs_master_rect().topleft[i] for i in range(2)]
            else:
                master = self.master
                for _ in range(move_level):
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
