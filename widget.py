import pygame as pg
from constants.private import *
from constants.public import *


class Master:
    """Class for methods present in Window and Widget. If instanced or subclassed, might raise AttributeError."""

    def __init__(self):
        self.children = list()
        self.pub_arg_dict = dict()
        self.visible = True
        self.user_attr = dict()
        self.surface = None
        self.my_surf = None
        self.grab = list()  # [event_type: [Child, ...]]
        self.handlers = list()  # [event_type: [(func, [arg1, ...], include_event_arg, /
        #                                       call_if_handled_by_children), ...]]
        self.non_receive_events = set()
        self.non_send_events = set()

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

    def add_handler(self, event_type, func, arglist=None, self_arg=True, event_arg=True, call_if_handled_by_children=False):
        """Adds handling function"""

        if arglist is None:
            arglist = list()
        if len(self.handlers) <= event_type:
            self.handlers += [list() for _ in range(1 + event_type - len(self.handlers))]
        self.handlers[event_type].append((func, arglist, self_arg, event_arg, call_if_handled_by_children))

    def remove_handler(self, event_type, func, arglist=None, include_event_arg=True):
        if arglist is None:
            arglist = list()
        to_del = []
        for handler in self.handlers[event_type]:
            if handler[:3] == (func, arglist, include_event_arg):
                to_del.append(handler)
        for d in to_del:
            self.handlers.remove(d)

    def add_nr_events(self, *args):
        for e in args:
            self.non_receive_events.add(e)

    def remove_nr_events(self, *args):
        for e in args:
            try:
                self.non_receive_events.remove(e)
            except ValueError:
                pass

    def add_ns_events(self, *args):
        for e in args:
            self.non_send_events.add(e)

    def remove_ns_events(self, *args):
        for e in args:
            try:
                self.non_send_events.remove(e)
            except ValueError:
                pass

    def handle_events(self, *events):
        """Function for handling events if possible. For every event, if succesfully handled, returns list of tuples
        (widget, handler), otherwise empty list. Should be called in Window's instance for every event in event queue,
        especially for pygame.VIDEORESIZE.
        Public."""

        output = [False] * len(events)
        for index, e in enumerate(events):
            if e.type in self.non_receive_events:
                continue
            if e.type not in self.non_send_events:
                try:
                    grab_exists = bool(self.grab[e.type])
                except IndexError:
                    grab_exists = False

                if grab_exists:
                    output[index] = True in self.grab[e.type][-1].handle_events(e)[0]
                else:
                    for child in self.children:
                        output[index] += child.handle_events(e)[0]

            try:
                handler_exists = bool(self.handlers[e.type])
            except IndexError:
                handler_exists = False

            if handler_exists:
                for handler in self.handlers[e.type]:
                    if handler[3] or not output[index]:
                        args = list()
                        if handler[2]:
                            args.append(self)
                        if handler[3]:
                            args.append(e)
                        args += handler[1]
                        handler[0](*args)
        return output

    def kwarg_list(self):
        """Returns the list of all setable attributes.
        Public."""

        return sum(self.pub_arg_dict.values(), [])

    def set_u(self, **kwargs):
        """Sets user defined attributes.
        Public."""

        self.user_attr.update(kwargs)

    def get_u(self, *args):
        """Returns values of requested user defined attributes. If not defined, returns None.
        Public."""

        Values = [None] * len(args)
        for index, attr in enumerate(args):
            try:
                Values[index] = self.user_attr[attr]
            except KeyError:
                pass
        return Values

    def del_u(self, *args):
        """Deletes some of user defined attributes.
        Public."""

        for attr in args:
            try:
                del self.user_attr[attr]
            except KeyError:
                pass

    def blit(self, rect=None):
        """Blits the surface of appearance to the master's surface subsurface. If rect, actualises only children
        colliding with the rect.
        Can be called by master or child.
        Private."""

        if not self.visible:
            return
        if rect is None:
            rect = self.surface.get_rect()
        else:
            rect = rect.clip(self.surface.get_rect())
        OldClip = self.surface.get_clip()
        self.surface.set_clip(rect)
        self.surface.blit(self.my_surf, (0, 0))
        self.surface.set_clip(OldClip)
        self.add_update(rect.move(*self.surface.get_abs_offset()))
        for child in self.children:
            if child.master_rect.colliderect(rect):
                child.blit(rect.move(*[-a for a in child.surface.get_offset()]))

    def redraw_child_reccurent(self, abs_clip, path):
        """Reccurent function used to disappear widget.
        Is called by child.
        Private."""

        clip = abs_clip.move(*[-a for a in self.surface.get_offset()]) if isinstance(self, Widget) else abs_clip
        self.surface.set_clip(clip)
        self.surface.blit(self.my_surf, (0, 0))
        for child in self.children:
            if child.master_rect.colliderect(clip) and child != path[0]:
                child.blit(clip.move(*[-a for a in child.surface.get_offset()]))
            elif child == path[0] and len(path) > 1:
                child.redraw_child_reccurent(abs_clip, path[1:])


class Window(Master):
    """The main master. Causes problems if instanced multiple times."""

    def __init__(self, resolution=(0, 0), flags=0, depth=0, min_size=(None, None), max_size=(None, None), **kwargs):
        super().__init__()
        self.add_handler(VIDEORESIZE, self.resize, self_arg=False, call_if_handled_by_children=True)
        self.add_handler(QUIT, self.quit, self_arg=False, event_arg=False)
        self.add_handler(KEYDOWN, self.AltF4, self_arg=False, call_if_handled_by_children=True)
        self.min_size = min_size
        self.max_size = max_size
        resolution = self.repair_size(resolution)
        self.surf_args = (flags | SRCALPHA, depth)
        self.surface = pg.display.set_mode(resolution, *self.surf_args)
        self.my_surf = pg.Surface(resolution)
        self.my_surf.convert_alpha()
        self.to_update = list()
        self.pub_arg_dict['Window_'] = ['fps']
        self.fps = DEFAULT_FPS
        self.clock = pg.time.Clock()

        self.set()

    @staticmethod
    def quit(code=0):
        pg.quit()
        exit(code)

    def AltF4(self, event):
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

        size = self.repair_size(event.size)
        self.surface = pg.display.set_mode(size, *self.surf_args)
        self.my_surf = pg.Surface(size)
        for child in self.children:
            child.reconnect()
            child.generate_surf()
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

        if self.surface.get_rect().colliderect(rect):
            self.to_update.append(self.surface.get_rect().clip(rect))
            return True
        return False

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

        for name, value in kwargs.items():
            if name in self.kwarg_list():
                setattr(self, name, value)
        self.actualise_settings(**kwargs)

    def actualise_settings(self, **kwargs):
        """Actualises its image on the screen after setting new values to attributes in most efficient way.
        Private."""

        pass


class Widget(Master):
    """Base for every other widget. Supplies comunication with children and parents, moving and displaying.
    Cannot be instanced."""

    def __init__(self, master, rect, **kwargs):
        super().__init__()
        self.pub_arg_dict["Widget_"] = ["auto_res"]
        self.pub_arg_dict["special"] = ["visible"]
        self.master = master
        self.auto_res = False
        self.visible = True

        try:
            self.surface = master.surface.subsurface(rect)
        except ValueError:
            self.surface = pg.Surface(rect.size)
            self.connected = False
        else:
            self.connected = True
            self.master.children.append(self)
        self.master_rect = rect
        self.my_surf = pg.Surface(rect.size)
        self.safe_init(**kwargs)

    def get_abs_master_rect(self):
        """Returns the rectangle of used space in absolute master's surface.
        Public."""

        return Rect(self.surface.get_abs_offset(), self.surface.get_size())

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

        self.my_surf = pg.Surface(self.surface.get_size())

    def safe_init(self, **kwargs):
        """Searches for non-generate arg, if not found, generates surface. Useful for distinguishing the initialisation
        of user-requested instance and initialisation of the super() of it.
        Private."""

        if SUPER in kwargs.keys():
            if kwargs[SUPER]:
                return
        self.set(**kwargs)
        self.generate_surf()
        self.appear()

    def appear(self):
        """Method used to draw widget properly."""

        if self.connected:
            self.get_abs_master_path()[0].blit(self.get_abs_master_rect())

    def disappear(self):
        """Method used to redraw widget by other widgets.
        Public."""

        if self.connected:
            path = self.get_abs_master_path()
            path[0].redraw_child_reccurent(self.get_abs_master_rect(), path[1:] + [self])
            self.add_update()

    def add_update(self, rect=None):
        """Used to add a child's rectrangle into 'to_update' list of the window.
        Returns True if succesful, otherwise False.
        Can be called by a child.
        Private."""

        if not rect:
            rect = self.get_abs_master_rect()
        if self.get_abs_master_rect().colliderect(rect):
            return self.master.add_update(self.get_abs_master_rect().clip(rect))
        return False

    def reconnect(self, rect=None, abs_rect=False):
        """Used to actualise the connections of subsurfaces
        (makes self.surface to be a subsurface of self.master.surface).
        Can be called by master.
        Public."""

        if not rect:
            rect = self.master_rect
        if abs_rect:
            rect.move_ip(*[-i for i in self.master.surface.get_abs_offset()])
        try:
            self.surface = self.master.surface.subsurface(rect)
        except ValueError:
            self.connected = False
            return False
        self.connected = True
        self.master_rect = rect
        if self not in self.master.children:
            self.master.children.append(self)
        self.appear()
        output = [True] + ([None] * len(self.children))
        for index, child in enumerate(self.children):
            output[index + 1] = child.reconnect()
        return output

    def disconnect(self):
        """Disconnets its surface from master's surface and redraws itself."""

        if not self.connected:
            return
        self.disappear()
        self.master.children.remove(self)
        self.surface = self.my_surf.copy()
        self.connected = False
        for child in self.children:
            child.reconnect()

    def set(self, **kwargs):
        """Sets the keyword arguments and actualises the surface of appearance and the image on the screen.
        Public."""

        for name, value in kwargs.items():
            if name in self.kwarg_list():
                if name in self.pub_arg_dict['special']:
                    self.set_special(name, value)
                else:
                    setattr(self, name, value)
                visible = self.visible
                setattr(self, name, value)
                if name == "visible" and value != visible:
                    if value:
                        self.master.blit(self.master_rect)
                    else:
                        self.disappear()
        self.set_update(**kwargs)

    def set_update(self, **kwargs):
        """Actualises its image on the screen after setting new values to attributes in most efficient way.
        Private."""

        if kwargs:
            OldSurf = self.my_surf.copy()
            self.generate_surf()
            if OldSurf != self.my_surf:
                self.appear()

    def set_special(self, name, value):
        """Does special actions when changing special attributes.
        Private."""

        if name == 'visible' and value != self.visible:
            self.visible = value
            if value:
                self.appear()
            else:
                self.disappear()

    def move_resize(self, move=(0, 0), move_level='rel', resize=(1, 1), resize_rel=True, update_surf=True):
        """Moves its subsurface inside master's surface to the given position and resizes it.
        move_level is an integer or one of strings 'abs' and 'rel'.
        Public."""

        if resize_rel:
            resize = [resize[i] * self.surface.get_size()[i] for i in range(2)]

        size = self.surface.get_size()

        if self.connected:
            if move_level == 'rel':
                move = [move[i] + self.surface.get_offset()[i] for i in range(2)]
            elif move_level == 'abs':
                move = [self.surface.get_offset()[i] + (move[i] - self.surface.get_abs_offset()[i]) for i in range(2)]
            else:
                master = self.master
                for _ in range(move_level):
                    move = [move[i] - master.surface.get_offset()[i] for i in range(2)]
                    try:
                        master = master.master
                    except AttributeError:
                        break
            rect = Rect(move, resize)
            if not self.master.surface.get_rect().contains(rect):
                return False
            self.disappear()
            self.surface = self.master.surface.subsurface(rect)
            self.master_rect = rect
        else:
            if move_level == 'rel':
                self.master_rect.move_ip(*move)
            else:
                self.master_rect.topleft = move
            self.master_rect.size = resize
            self.surface = pg.Surface(resize)
        if update_surf:
            self.generate_surf()
        output = [True] + ([None] * len(self.children))
        for index, child in enumerate(self.children):
            output[index + 1] = child.reconnect()
            if size != resize:
                child.generate_surf()
        self.appear()
        return output
