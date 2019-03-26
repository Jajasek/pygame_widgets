import pygame as pg
import pygame_widgets.widget as W
from pygame_widgets.constants.private import *
from pygame_widgets.constants.public import *


class Image(W.Widget_):
    def __init__(self, master, image, topleft=(0, 0), **kwargs):
        updated = kwargs.copy()
        updated[SUPER] = True
        super().__init__(master, Rect(topleft, image.get_size()), **updated)
        self.pub_arg_dict['Image_set'] = ['image']
        self.image = image
        self._safe_init(**kwargs)

    def _generate_surf(self):
        self.my_surf = self.image.copy()
