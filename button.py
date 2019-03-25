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
        self.add_handler(MOUSEBUTTONDOWN, self.click, self_arg=False)
        self.add_handler(MOUSEBUTTONUP, self.click, self_arg=False)
        self.safe_init(**kwargs)

    def click(self, event):
        try:
            surf_rect = self.surface.get_rect().move(self.surface.get_abs_offset())
        except AttributeError:
            pass
        else:
            if surf_rect.collidepoint(event.pos):
                if event.type == MOUSEBUTTONDOWN:
                    # noinspection PyArgumentList
                    self.post_event(pg.event.Event(BUTTON_PRESSED, button=event.button, pos=event.pos))
                    self.pressed.add(event.button)
                if event.type == MOUSEBUTTONUP:
                    # noinspection PyArgumentList
                    self.post_event(pg.event.Event(BUTTON_RELEASED, button=event.button, pos=event.pos))
                    if event.button in self.pressed:
                        # noinspection PyArgumentList
                        self.post_event(pg.event.Event(BUTTON_BUMPED, button=event.button, pos=event.pos))
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

        self.add_handler(MOUSEBUTTONDOWN, self.mouseover_check, self_arg=False, call_if_handled_by_children=True)
        self.add_handler(MOUSEBUTTONUP, self.mouseover_check, self_arg=False, call_if_handled_by_children=True)
        self.add_handler(MOUSEMOTION, self.mouseover_check, self_arg=False, call_if_handled_by_children=True)

        self.safe_init(**kwargs)

    def mouseover_check(self, event):
        if self.pressed:
            if self.appearance != 'pressed':
                self.background = self.bg_pressed
                self.appearance = 'pressed'
                self.mouseover_update()
            return
        try:
            surf_rect = self.surface.get_rect().move(self.surface.get_abs_offset())
        except AttributeError:
            surf_rect = None
        if surf_rect is None or not surf_rect.collidepoint(event.pos):
            if self.appearance != 'normal':
                self.background = self.bg_normal
                self.appearance = 'normal'
                self.mouseover_update()
            return
        if self.appearance != 'mouseover':
            self.background = self.bg_mouseover
            self.appearance = 'mouseover'
            self.mouseover_update()

    def mouseover_update(self):
        self.generate_surf()
        if self.my_surf.get_size() != self.master_rect.size:
            self.disappear()
            self.master_rect.size = self.my_surf.get_size()
        self.appear()
