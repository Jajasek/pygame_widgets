import pygame_widgets.widget as W
import pygame_widgets.text as T
import pygame as pg
import pygame_widgets.constants.private as CONST
from pygame_widgets.constants.public import *


class Button_(W.Widget_):
    def __init__(self, master, topleft, size, **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, **updated)
        self.pressed = set()
        self.add_handler(MOUSEBUTTONDOWN, self._click, self_arg=False)
        self.add_handler(MOUSEBUTTONUP, self._click, self_arg=False)
        self._safe_init(**kwargs)

    def _click(self, event):
        """Default handler for MOUSEBUTTON events, actually creates the behaviour of button: posts events E_BUTTON_.
        Private."""

        surf_rect = self.get_abs_surf_rect()
        if surf_rect.collidepoint(event.pos):
            if event.type == MOUSEBUTTONDOWN:
                # noinspection PyArgumentList
                self._post_event(pg.event.Event(E_BUTTON_PRESSED, button=event.button, pos=event.pos))
                self.pressed.add(event.button)
            if event.type == MOUSEBUTTONUP:
                # noinspection PyArgumentList
                self._post_event(pg.event.Event(E_BUTTON_RELEASED, button=event.button, pos=event.pos))
                if event.button in self.pressed:
                    # noinspection PyArgumentList
                    self._post_event(pg.event.Event(E_BUTTON_BUMPED, button=event.button, pos=event.pos))
        if event.type == MOUSEBUTTONUP and event.button in self.pressed:
            self.pressed.remove(event.button)


class Button(Button_, T.Label):
    def __init__(self, master, topleft=(0, 0), size=(1, 1), **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, **updated)
        self.appearance = 'normal'
        self.background = self.bg_normal = CONST.DEFAULT.bg_normal
        self.bg_mouseover = CONST.DEFAULT.bg_mouseover
        self.bg_pressed = CONST.DEFAULT.bg_pressed

        self.add_handler(MOUSEBUTTONDOWN, self._mouseover_check, self_arg=False, call_if_handled_by_children=True)
        self.add_handler(MOUSEBUTTONUP, self._mouseover_check, self_arg=False, call_if_handled_by_children=True)
        self.add_handler(MOUSEMOTION, self._mouseover_check, self_arg=False, call_if_handled_by_children=True)

        self.pub_arg_dict['Button_appearance'] = ['appearance', 'bg_normal', 'bg_mouseover', 'bg_pressed']
        self._safe_init(**kwargs)

    def _mouseover_check(self, event):
        """Default handler for mouse events, handles the dynamic appearance changing based on mouse state.
        Private."""

        if self.pressed:
            if self.appearance != 'pressed':
                self.background = self.bg_pressed
                self.appearance = 'pressed'
                self._mouseover_update()
            return
        surf_rect = self.get_abs_surf_rect()
        if not surf_rect.collidepoint(event.pos):
            if self.appearance != 'normal':
                self.background = self.bg_normal
                self.appearance = 'normal'
                self._mouseover_update()
            return
        if self.appearance != 'mouseover':
            self.background = self.bg_mouseover
            self.appearance = 'mouseover'
            self._mouseover_update()

    def _mouseover_update(self):
        """Updates the appearance based on mouse state.
        Private."""

        self._generate_surf()
        if self.my_surf.get_size() != self.master_rect.size:
            self.move_resize(resize=self.my_surf.get_size(), resize_rel=False)
            """self.disappear()
            self.master_rect.size = self.my_surf.get_size()
            self._create_subsurface()"""
        else:
            self.appear()

    def _set_update(self, old=None, **kwargs):
        """Actualises its image on the screen after setting new values to attributes in most efficient way.
        Private."""

        if kwargs:
            update = False
            for name in kwargs.keys():
                if name in self.pub_arg_dict['Button_appearance']:
                    update = True
            if update:
                self._mouseover_update()
            T.Text_._set_update(self, old, **kwargs)

    def _set_event(self, old=None, **kwargs):
        """Places events on the queue based on changed attributes.
        Private."""

        if old is None:
            old = dict()
        for name, value in kwargs.items():
            # noinspection PyArgumentList
            self._post_event(pg.event.Event(E_BUTTON_APPEARANCE if name in self.pub_arg_dict['Button_appearance'] else
                                           E_BUTTON_ATTR, name=name, new=value, old=old[name] if name in old else None))

