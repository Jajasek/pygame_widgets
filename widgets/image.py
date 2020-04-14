import pygame as pg
import pygame_widgets.widgets.widget as W
import pygame_widgets.constants.private as CONST
from pygame_widgets.constants import *


__all__ = ['Image']


class Image(W._Widget):
    """Widget that constantly displays given surface or color."""

    def __init__(self, master, topleft=(0, 0), size=(1, 1), **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, topleft, size, **updated)
        self.pub_arg_dict['Image_set'] = ['image']
        self.image = CONST.DEFAULT.IMAGE.bg
        self._safe_init(**kwargs)

    def _set_update(self, old=None, **kwargs):
        """Actualises its image on the screen after setting new values to attributes in most efficient way.
        Private."""

        if kwargs:
            super()._set_update(old, **kwargs)
            update = False
            for name in kwargs.keys():
                if name in self.pub_arg_dict['Image_set']:
                    update = True
            if update:
                self.update_appearance()

    def _set_event(self, old=None, **kwargs):
        """Places events on the queue based on changed attributes.
        Private."""

        if old is None:
            old = dict()
        for name, value in kwargs.items():
            self._post_event(pg.event.Event(PYGAME_WIDGETS, ID=E_IMAGE_APPEARANCE, name=name, new=value,
                                            old=old[name] if name in old else None))

    def _generate_surf(self):
        """Generates new surface of appearance.
        Private."""

        if callable(self.image):
            self.my_surf = self.image(self)
        elif isinstance(self.image, pg.Surface):
            if self.auto_res:
                self.my_surf = self.image.copy()
            else:
                self.my_surf = pg.transform.scale(self.image.copy(), self.my_surf.get_size())
        else:
            self.my_surf = pg.Surface(self.master_rect.size, SRCALPHA)
            self.my_surf.fill(self.image)
        self.my_surf.convert_alpha()
