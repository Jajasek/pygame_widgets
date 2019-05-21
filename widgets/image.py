import pygame as pg
import pygame_widgets.widgets.widget as W
import pygame_widgets.constants.private as CONST
from pygame_widgets.constants.public import *


class Image(W._Widget):
    """Widget that constantly displays given surface or color. When resized, the image will be sticked in topleft
    corner."""

    def __init__(self, master, topleft=(0, 0), size=(1, 1) , image_or_color = THECOLORS['white'], **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        if isinstance(image_or_color, pg.Surface):
            size = image_or_color.get_size()
            image = image_or_color
            image.convert()
        else:
            image = pg.Surface(size, SRCALPHA)
            image.fill(image_or_color)
        super().__init__(master, Rect(topleft, size), **updated)
        self.pub_arg_dict['Image_set'] = ['image']
        self.image = image
        self._safe_init(**kwargs)

    def _set_event(self, old=None, **kwargs):
        """Places events on the queue based on changed attributes.
        Private."""

        if old is None:
            old = dict()
        for name, value in kwargs.items():
            self._post_event(pg.event.Event(E_IMAGE_APPEARANCE, name=name, new=value,
                                            old=old[name] if name in old else None))

    def _generate_surf(self):
        self.my_surf = self.image.copy()
