import pygame as pg
import pygame_widgets.widgets.widget as W
import pygame_widgets.constants.private as CONST
from pygame_widgets.constants import *


__all__ = ['Image']


class Image(W._Widget):
    """Widget that constantly displays given surface or color. When resized, the image will be sticked in topleft
    corner."""

    def __init__(self, master, topleft=(0, 0), size=(1, 1), **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, **updated)
        self.pub_arg_dict['Image_set'] = ['image']
        self.image = CONST.DEFAULT.IMAGE.img
        self._safe_init(**kwargs)

    def _set_event(self, old=None, **kwargs):
        """Places events on the queue based on changed attributes.
        Private."""

        if old is None:
            old = dict()
        for name, value in kwargs.items():
            self._post_event(pg.event.Event(PYGAME_WIDGETS, ID=E_IMAGE_APPEARANCE, name=name, new=value,
                                            old=old[name] if name in old else None))

    def _generate_surf(self):
        if callable(self.image):
            self.my_surf = self.image(self.master_rect.size)
        elif isinstance(self.image, pg.Surface):
            self.my_surf = self.image.copy()
        else:
            self.my_surf = pg.Surface(self.master_rect.size, SRCALPHA)
            self.my_surf.fill(self.image)
        self.my_surf.convert()
