import pygame as pg
from attributes import Attributes
import pygame_widgets.constants.private as CONST
from pygame_widgets.constants.public import *


class Master_:
    """Class for methods present in Window and Widget. If instanced or subclassed, might raise AttributeError."""

    next_ID = 0

    def __init__(self):
        self.ID = Master_.next_ID
        Master_.next_ID += 1
        self.children = list()
        self.pub_arg_dict = dict()
        self.pub_arg_dict['special'] = []
        self.visible = True
        self.attributes = Attributes()
        self.surface = None
        self.my_surf = None
        self.topleft = (0, 0)
        self.master_rect = Rect(0, 0, 1, 1)
        self.grab = list()  # [event_type: [Child, ...]]
        self.handlers = dict()  # [event_type: [(func, [arg1, ...], include_event_arg, /
        #                                       call_if_handled_by_children), ...]]
        self.no_receive_events = set()
        self.no_send_events = set()

    def __str__(self):
        return f'<{str(self.__class__)[8:-2]} object, ID {self.ID}>'

    def on_screen(self, rect=None):
        """Returns True if there is its image on current window, otherwise False.
        Private."""

        if not rect:
            rect = self.get_abs_master_rect()
        try:
            b = self.master.surface is not None
        except AttributeError:
            b = True
        return pg.display.get_surface().get_rect().colliderect(rect) and b

    def add_grab(self, event_type, child):
        """Child grabs every event of specified type.
        Public."""

        if child not in self.children:
            return
        if len(self.grab) <= event_type:
            self.grab += [[]] * (1 + event_type - len(self.grab))
        self.grab[event_type].append(child)

    def remove_grab(self, event_type, child):
        """Disables grabbing events of event_type by child.
        Public."""

        try:
            while True:
                self.grab[event_type].remove(child)
        except (ValueError, IndexError):
            pass

    def add_handler(self, event_type, func, args=None, kwargs=None, self_arg=True, event_arg=True,
                    call_if_handled_by_children=False):
        """Adds handling function with settings.
        Public."""

        if args is None:
            args = list()
        if kwargs is None:
            kwargs = dict()
        if event_type not in self.handlers:
            self.handlers[event_type] = list()
        self.handlers[event_type].append((func, args, kwargs, self_arg, event_arg, call_if_handled_by_children))

    def remove_handler(self, event_type, func, args=None, kwargs=None, self_arg=True, event_arg=True):
        """Removes handling function with settings.
        Public."""

        if args is None:
            args = list()
        if kwargs is None:
            kwargs = dict()
        for handler in self.handlers[event_type]:
            if handler[:5] == (func, args, kwargs, self_arg, event_arg):
                self.handlers[event_type].remove(handler)

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
                except IndexError:
                    grab_exists = False

                if grab_exists:
                    output[index] = self.grab[e.type][-1].handle_events(e)[0]
                else:
                    for child in self.children:
                        output[index] = output[index] or child.handle_events(e)[0]

            try:
                if not self.handlers[e.type]:
                    continue
            except KeyError:
                continue

            for handler in self.handlers[e.type]:
                if handler[5] or not output[index]:
                    args = list()
                    if handler[3]:
                        args.append(self)
                    if handler[4]:
                        args.append(e)
                    args += handler[1]
                    handler[0](*args, **handler[2])
                    output[index] = True
        return output

    def post_event(self, event):
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

        if not self.visible or not self.on_screen():
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


class Window(Master_):
    """The main master. Causes problems if instanced multiple times."""

    def __init__(self, resolution=(0, 0), flags=0, depth=0, **kwargs):
        super().__init__()
        self.add_handler(VIDEORESIZE, self.resize, self_arg=False, call_if_handled_by_children=True)
        self.add_handler(QUIT, self.quit, self_arg=False, event_arg=False, call_if_handled_by_children=True)
        self.add_handler(KEYDOWN, self.AltF4, self_arg=False, call_if_handled_by_children=True)
        self.min_size = (None, None)
        self.max_size = (None, None)
        self.surf_args = (flags | SRCALPHA, depth)
        self.surface = pg.display.set_mode(resolution, *self.surf_args)
        self.my_surf = pg.Surface(self.surface.get_size())
        self.my_surf.convert_alpha()
        self.to_update = list()
        self.pub_arg_dict['Window_attr'] = ['fps']
        self.pub_arg_dict['Window_resize'] = ['min_size', 'max_size']
        self.pub_arg_dict['special'].extend(['title', 'icon_title', 'icon'])
        self.fps = CONST.DEFAULT_FPS
        self.clock = pg.time.Clock()

        self.set(**kwargs)

    @staticmethod
    def quit(code=0):
        """Default handler for pygame.QUIT event.
        Public."""

        # noinspection PyUnresolvedReferences
        pg.quit()
        exit(code)

    def AltF4(self, event):
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

    def resize(self, event):
        """Default handler for Pygame.VIDEORESIZE event.
        Private."""

        if event.size != self.surface.get_size() or self.repair_size(event.size) != self.surface.get_size():
            self.surface = pg.display.set_mode(self.repair_size(event.size), *self.surf_args)
            self.my_surf = pg.Surface(self.surface.get_size())
            for child in self.children:
                child.reconnect()
                child.generate_surf()
                if child.master_rect.size != child.my_surf.get_size():
                    child.disappear()
                    child.master_rect.size = child.my_surf.get_size()
                    child.create_subsurface()
            self.blit(self.surface.get_rect())
            self.add_update(self.surface.get_rect())

    def repair_size(self, size):
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

        if self.on_screen(rect):
            self.to_update.append(self.surface.get_rect().clip(rect))
            return True
        return False

    def get_abs_master_rect(self):
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
                    self.set_special(name, value)
                else:
                    old[name] = getattr(self, name, None)
                    setattr(self, name, value)
        self.set_update(old, **kwargs)

    def set_update(self, old=None, **kwargs):
        """Actualises its image on the screen after setting new values to attributes in most efficient way.
        Private."""

        if old is None:
            old = dict()
        if kwargs:
            res = False
            for name in kwargs.keys():
                if name in self.pub_arg_dict['Window_resize']:
                    res = True
            if res:
                res = self.surface.get_size()
                self.post_event(pg.event.Event(VIDEORESIZE, size=res, w=res[0], h=res[1]))
            self.set_event(old, **kwargs)

    # noinspection PyMethodMayBeStatic
    def set_special(self, name, value):
        """Manages settings that require some special action instead of changing attributes of self.
        Private."""

        if name == 'title':
            pg.display.set_caption(value)
        elif name == 'icontitle':
            pg.display.set_caption(pg.display.get_caption()[0], value)
        elif name == 'icon':
            pg.display.set_icon(value)

    # noinspection PyMethodMayBeStatic
    def set_event(self, old=None, **kwargs):
        """Places events on the queue based on changed attributes.
        Private."""

        if old is None:
            old = dict()
        for name, value in kwargs.items():
            self.post_event(pg.event.Event(WINDOW_ATTR, name=name, new=value, old=old[name] if name in old else None))


class Widget_(Master_):
    """Base for every other widget. Supplies comunication with children and parents, moving and displaying.
    Cannot be instanced."""

    def __init__(self, master, rect, **kwargs):
        super().__init__()
        self.pub_arg_dict["Widget_attr"] = ["auto_res"]
        self.pub_arg_dict["special"].extend(["visible"])
        self.master = master
        self.auto_res = False
        self.visible = True
        self.connected = True
        self.master_rect = rect
        self.create_subsurface()
        self.master.children.append(self)
        self.my_surf = pg.Surface(rect.size)
        self.safe_init(**kwargs)

    def get_abs_master_rect(self):
        """Returns the rectangle of used space in absolute master's surface.
        Public."""

        rect = self.master_rect.move(*self.master.get_abs_master_rect().topleft)
        print(self, rect)
        return rect

    def get_abs_master_path(self):
        """returns the list of masters sorted from top-level.
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

    def generate_surf(self):
        """Generates new surface of appearance.
        Private."""

        self.my_surf = pg.Surface(self.master_rect.size)

    def create_subsurface(self):
        """Tries to create a subsurface and actualise topleft.
        Private."""

        if self.on_screen():
            rect = self.master.surface.get_rect().clip(
                self.master_rect.move(*[self.master.topleft[i] for i in range(2)]))
            if rect.size != (0, 0):
                self.surface = self.master.surface.subsurface(rect)
                self.topleft = [self.master_rect.topleft[i] -
                                (rect.topleft[i] - self.master.topleft[i]) for i in range(2)]
                return
        self.surface = None
        self.topleft = (0, 0)

    def safe_init(self, **kwargs):
        """Searches for non-generate arg, if not found, generates surface. Useful for distinguishing the initialisation
        of user-requested instance and initialisation of the super() of it.
        Private."""

        if CONST.SUPER in kwargs:
            if kwargs[CONST.SUPER]:
                return
        self.set(**kwargs)
        self.generate_surf()
        if self.master_rect.size != self.my_surf.get_size():
            self.master_rect.size = self.my_surf.get_size()
            self.create_subsurface()
        self.appear()

    def appear(self):
        """Method used to draw widget on the screen properly.
        Public."""

        if self.connected and self.on_screen():
            self.get_abs_master_path()[0].blit(self.get_abs_master_rect())

    def disappear(self):
        """Method used to redraw widget by other widgets. It could cause problems if not used carefully.
        Private."""

        if self.connected and self.on_screen():
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
        if self.get_abs_master_rect().colliderect(rect) and self.on_screen(rect):
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
        self.create_subsurface()
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
                    self.set_special(name, value)
                else:
                    old[name] = getattr(self, name, None)
                    setattr(self, name, value)
        self.set_update(old, **kwargs)

    def set_update(self, old=None, **kwargs):
        """Actualises its image on the screen after setting new values to attributes in most efficient way.
        Private."""

        if kwargs:
            old_surf = self.my_surf.copy()
            self.generate_surf()
            if old_surf.get_size() != self.my_surf.get_size():
                self.disappear()
                self.master_rect.size = self.my_surf.get_size()
                self.create_subsurface()
            if old_surf != self.my_surf:
                self.appear()
            self.set_event(old, **kwargs)

    def set_special(self, name, value):
        """Does special actions when changing special attributes.
        Private."""

        if name == 'visible' and value != self.visible:
            self.visible = value
            if value:
                self.appear()
            else:
                self.disappear()

    # noinspection PyMethodMayBeStatic
    def set_event(self, old=None, **kwargs):
        """Places events on the queue based on changed attributes.
        Private."""

        if old is None:
            old = dict()
        for name, value in kwargs.items():
            self.post_event(pg.event.Event(WIDGET_ATTR, name=name, new=value, old=old[name] if name in old else None))

    def move_resize(self, move=(0, 0), move_level: int = 'rel', resize=(1, 1), resize_rel=True, update_surf=True):
        """Moves its subsurface inside master's surface to the given position and resizes it.
        move_level is an integer or one of strings 'abs' and 'rel'.
        Public."""

        size = self.my_surf.get_size()
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
            self.create_subsurface()
        else:
            if move_level == 'rel':
                self.master_rect.move_ip(*move)
            else:
                self.master_rect.topleft = move
            self.master_rect.size = resize
            self.surface = pg.Surface(resize)
        if update_surf:
            self.generate_surf()
            if self.master_rect.size != self.my_surf.get_size():
                self.master_rect.size = self.my_surf.get_size()
                self.create_subsurface()
        for child in self.children:
            child.reconnect()
        self.appear()
