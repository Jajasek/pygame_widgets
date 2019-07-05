print("pygame_widgets init")

import pygame
pygame.init()
from pygame_widgets.widgets.widget import *
from pygame_widgets.widgets.holder import *
from pygame_widgets.widgets.text import *
from pygame_widgets.widgets.button import *
from pygame_widgets.widgets.image import *
from pygame_widgets.widgets.entry import *
# from pygame_widgets.constants import *
import pygame_widgets.constants as constants

_post_events = True


def set_mode_init():
    global _post_events
    _post_events = False


def set_mode_mainloop():
    global _post_events
    _post_events = True


def get_mode():
    return _post_events


print("pygame_widgets initialised")
