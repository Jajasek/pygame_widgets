import pygame_widgets.widgets.widget as W
import pygame_widgets.widgets.text as T
import pygame as pg
import pygame_widgets.constants.private as CONST
from pygame_widgets.constants import *


__all__ = ['Button']


class _Button(W._Widget):
    """Virtual base widget, which adds the button functionality. Cannot be instanced."""

    def __init__(self, master, topleft, size, **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, **updated)
        self.pressed = set()
        self.mouseover = False
        self.add_handler(MOUSEBUTTONDOWN, self._click, self_arg=False)
        self.add_handler(MOUSEBUTTONUP, self._click, self_arg=False)
        self.add_handler(MOUSEMOTION, self._movement, self_arg=False)
        self._safe_init(**kwargs)

    def _click(self, event):
        """Default handler for MOUSEBUTTON events, actually creates the behaviour of button. Posts events E_BUTTON_.
        Private."""

        if self.get_abs_surf_rect().collidepoint(event.pos):
            if event.type == MOUSEBUTTONDOWN:
                # noinspection PyArgumentList
                self._post_event(pg.event.Event(PYGAME_WIDGETS, ID=E_BUTTON_PRESSED, button=event.button, pos=event.pos))
                self.pressed.add(event.button)
            if event.type == MOUSEBUTTONUP:
                # noinspection PyArgumentList
                self._post_event(pg.event.Event(PYGAME_WIDGETS, ID=E_BUTTON_RELEASED, button=event.button, pos=event.pos))
                if event.button in self.pressed:
                    # noinspection PyArgumentList
                    self._post_event(pg.event.Event(PYGAME_WIDGETS, ID=E_BUTTON_BUMPED, button=event.button, pos=event.pos))
        if event.type == MOUSEBUTTONUP and event.button in self.pressed:
            self.pressed.remove(event.button)

    def _movement(self, event):
        """Default handler for MOUSEMOTION event, creates the behaviour of the button when mouse goes in and outside.
        Posts events E_BUTTON_.
        Private."""

        if self.get_abs_surf_rect().collidepoint(event.pos) and not self.mouseover:
            self._post_event(pg.event.Event(PYGAME_WIDGETS, ID=E_BUTTON_MOUSEOVER, pos=event.pos))
            self.mouseover = True
        elif not self.get_abs_surf_rect().collidepoint(event.pos) and self.mouseover:
            if self.pressed:
                self._post_event(pg.event.Event(PYGAME_WIDGETS, ID=E_BUTTON_SLIDED, buttons=self.pressed))
                self.pressed = set()
            else:
                self._post_event(pg.event.Event(PYGAME_WIDGETS, ID=E_BUTTON_MOUSEOUTSIDE, pos=event.pos))


class Button(_Button, T.Label):
    """Standart button. 1-line label that reacts to mouse events."""

    def __init__(self, master, topleft=(0, 0), size=(1, 1), **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, **updated)
        self.appearance = 'normal'
        self.background = self.bg_normal = CONST.DEFAULT.BUTTON.bg_normal
        self.bg_mouseover = CONST.DEFAULT.BUTTON.bg_mouseover
        self.bg_pressed = CONST.DEFAULT.BUTTON.bg_pressed
        self.cursor = self.cursor_normal = CONST.DEFAULT.BUTTON.cursor_normal
        self.cursor_mouseover = CONST.DEFAULT.BUTTON.cursor_mouseover
        self.cursor_pressed = CONST.DEFAULT.BUTTON.cursor_pressed

        self.add_handler(MOUSEBUTTONDOWN, self._mouseover_check, self_arg=False)
        self.add_handler(MOUSEBUTTONUP, self._mouseover_check, self_arg=False)
        self.add_handler(MOUSEMOTION, self._mouseover_check, self_arg=False)

        self.pub_arg_dict['Button_appearance'] = ['bg_normal', 'bg_mouseover', 'bg_pressed',
                                                  'cursor_normal', 'cursor_mouseover', 'cursor_pressed']
        self._safe_init(**kwargs)

    def _mouseover_check(self, event):
        """Default handler for mouse events, handles the dynamic appearance changing based on mouse state.
        Private."""

        if self.pressed:
            if self.appearance != 'pressed':
                self.appearance = 'pressed'
                self._mouseover_update()
            return
        surf_rect = self.get_abs_surf_rect()
        if not surf_rect.collidepoint(event.pos):
            if self.appearance != 'normal':
                self.appearance = 'normal'
                self._mouseover_update()
            return
        if self.appearance != 'mouseover':
            self.appearance = 'mouseover'
            self._mouseover_update()

    def _mouseover_update(self):
        """Updates the appearance based on mouse state.
        Private."""

        if self.appearance == 'normal':
            self.background = self.bg_normal
            self.cursor = self.cursor_normal
        if self.appearance == 'mouseover':
            self.background = self.bg_mouseover
            self.cursor = self.cursor_mouseover
        if self.appearance == 'pressed':
            self.background = self.bg_pressed
            self.cursor = self.cursor_pressed
        pg.mouse.set_cursor(*self.cursor)
        self._generate_surf()
        if self.my_surf.get_size() != self.master_rect.size:
            self.move_resize(resize=self.my_surf.get_size(), resize_rel=False)
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
            T._Text._set_update(self, old, **kwargs)

    def _set_event(self, old=None, **kwargs):
        """Places events on the queue based on changed attributes.
        Private."""

        if old is None:
            old = dict()
        for name, value in kwargs.items():
            # noinspection PyArgumentList
            self._post_event(pg.event.Event(PYGAME_WIDGETS, ID=E_BUTTON_APPEARANCE if name in
                                            self.pub_arg_dict['Button_appearance'] else E_BUTTON_ATTR, name=name,
                                            new=value, old=old[name] if name in old else None))

