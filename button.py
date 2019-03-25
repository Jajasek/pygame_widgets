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
        self.add_handler(MOUSEBUTTONDOWN, self.click, self_arg=False)
        self.add_handler(MOUSEBUTTONUP, self.click, self_arg=False)
        self.safe_init(**kwargs)

    def click(self, event):
        try:
            surf_rect = self.surface.get_rect().move(self.surface.get_abs_offset())
        except AttributeError:
            return
        if surf_rect.collidepoint(event.pos):
            self.post_event(pg.event.Event(BUTTON_PRESSED if event.type == MOUSEBUTTONDOWN else BUTTON_RELEASED,
                                           button=event.button, pos=event.pos))


class Button(Button_, T.Label):
    def __init__(self, master, topleft=(0, 0), size=(1, 1), **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, **updated)
        self.safe_init(**kwargs)
