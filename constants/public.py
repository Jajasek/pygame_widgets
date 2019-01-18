from pygame.colordict import THECOLORS
from pygame.locals import *


def Args(*args, **kwargs):
    return args, kwargs


# mouse events
MOTION_LEFT = 0
MOTION_MIDDLE = 1
MOTION_RIGHT = 2
BUTTON_LEFT = 1
BUTTON_MIDDLE = 2
BUTTON_RIGHT = 3
BUTTON_THUMB_FRONT = 6
BUTTON_THUMB_BACK = 7

# widget event types
LABEL__ATTR_CHANGE = 100
HOLDER__ATTR_CHANGE = 101
