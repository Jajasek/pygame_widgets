# noinspection PyUnresolvedReferences
from pygame.colordict import THECOLORS
from pygame import Surface
# noinspection PyUnresolvedReferences
from pygame.locals import *


# useful constants of pygame.locals which PyCharm doesn't know
# display flags
FULLSCREEN = FULLSCREEN
DOUBLEBUF = DOUBLEBUF
HWSURFACE = HWSURFACE
OPENGL = OPENGL
RESIZABLE = RESIZABLE
NOFRAME = NOFRAME
# event types
QUIT = QUIT
ACTIVEEVENT = ACTIVEEVENT
KEYDOWN = KEYDOWN
KEYUP = KEYUP
MOUSEMOTION = MOUSEMOTION
MOUSEBUTTONUP = MOUSEBUTTONUP
MOUSEBUTTONDOWN = MOUSEBUTTONDOWN
JOYAXISMOTION = JOYAXISMOTION
JOYBALLMOTION = JOYBALLMOTION
JOYHATMOTION = JOYHATMOTION
JOYBUTTONUP = JOYBUTTONUP
JOYBUTTONDOWN = JOYBUTTONDOWN
VIDEORESIZE = VIDEORESIZE
VIDEOEXPOSE = VIDEOEXPOSE
USEREVENT = USEREVENT
# keys
K_BACKSPACE = K_BACKSPACE
K_TAB = K_TAB
K_CLEAR = K_CLEAR
K_RETURN = K_RETURN
K_PAUSE = K_PAUSE
K_ESCAPE = K_ESCAPE
K_SPACE = K_SPACE
K_EXCLAIM = K_EXCLAIM
K_QUOTEDBL = K_QUOTEDBL
K_HASH = K_HASH
K_DOLLAR = K_DOLLAR
K_AMPERSAND = K_AMPERSAND
K_QUOTE = K_QUOTE
K_LEFTPAREN = K_LEFTPAREN
K_RIGHTPAREN = K_RIGHTPAREN
K_ASTERISK = K_ASTERISK
K_PLUS = K_PLUS
K_COMMA = K_COMMA
K_MINUS = K_MINUS
K_PERIOD = K_PERIOD
K_SLASH = K_SLASH
K_0 = K_0
K_1 = K_1
K_2 = K_2
K_3 = K_3
K_4 = K_4
K_5 = K_5
K_6 = K_6
K_7 = K_7
K_8 = K_8
K_9 = K_9
K_COLON = K_COLON
K_SEMICOLON = K_SEMICOLON
K_LESS = K_LESS
K_EQUALS = K_EQUALS
K_GREATER = K_GREATER
K_QUESTION = K_QUESTION
K_AT = K_AT
K_LEFTBRACKET = K_LEFTBRACKET
K_BACKSLASH = K_BACKSLASH
K_RIGHTBRACKET = K_RIGHTBRACKET
K_CARET = K_CARET
K_UNDERSCORE = K_UNDERSCORE
K_BACKQUOTE = K_BACKQUOTE
K_a = K_a
K_b = K_b
K_c = K_c
K_d = K_d
K_e = K_e
K_f = K_f
K_g = K_g
K_h = K_h
K_i = K_i
K_j = K_j
K_k = K_k
K_l = K_l
K_m = K_m
K_n = K_n
K_o = K_o
K_p = K_p
K_q = K_q
K_r = K_r
K_s = K_s
K_t = K_t
K_u = K_u
K_v = K_v
K_w = K_w
K_x = K_x
K_y = K_y
K_z = K_z
K_DELETE = K_DELETE
K_KP0 = K_KP0
K_KP1 = K_KP1
K_KP2 = K_KP2
K_KP3 = K_KP3
K_KP4 = K_KP4
K_KP5 = K_KP5
K_KP6 = K_KP6
K_KP7 = K_KP7
K_KP8 = K_KP8
K_KP9 = K_KP9
K_KP_PERIOD = K_KP_PERIOD
K_KP_DIVIDE = K_KP_DIVIDE
K_KP_MULTIPLY = K_KP_MULTIPLY
K_KP_MINUS = K_KP_MINUS
K_KP_PLUS = K_KP_PLUS
K_KP_ENTER = K_KP_ENTER
K_KP_EQUALS = K_KP_EQUALS
K_UP = K_UP
K_DOWN = K_DOWN
K_RIGHT = K_RIGHT
K_LEFT = K_LEFT
K_INSERT = K_INSERT
K_HOME = K_HOME
K_END = K_END
K_PAGEUP = K_PAGEUP
K_PAGEDOWN = K_PAGEDOWN
K_F1 = K_F1
K_F2 = K_F2
K_F3 = K_F3
K_F4 = K_F4
K_F5 = K_F5
K_F6 = K_F6
K_F7 = K_F7
K_F8 = K_F8
K_F9 = K_F9
K_F10 = K_F10
K_F11 = K_F11
K_F12 = K_F12
K_F13 = K_F13
K_F14 = K_F14
K_F15 = K_F15
K_NUMLOCK = K_NUMLOCK
K_CAPSLOCK = K_CAPSLOCK
K_SCROLLOCK = K_SCROLLOCK
K_RSHIFT = K_RSHIFT
K_LSHIFT = K_LSHIFT
K_RCTRL = K_RCTRL
K_LCTRL = K_LCTRL
K_RALT = K_RALT
K_LALT = K_LALT
K_RMETA = K_RMETA
K_LMETA = K_LMETA
K_LSUPER = K_LSUPER
K_RSUPER = K_RSUPER
K_MODE = K_MODE
K_HELP = K_HELP
K_PRINT = K_PRINT
K_SYSREQ = K_SYSREQ
K_BREAK = K_BREAK
K_MENU = K_MENU
K_POWER = K_POWER
K_EURO = K_EURO
# key mods
KMOD_NONE = KMOD_NONE
KMOD_LSHIFT = KMOD_LSHIFT
KMOD_RSHIFT = KMOD_RSHIFT
KMOD_SHIFT = KMOD_SHIFT
KMOD_CAPS = KMOD_CAPS
KMOD_LCTRL = KMOD_LCTRL
KMOD_RCTRL = KMOD_RCTRL
KMOD_CTRL = KMOD_CTRL
KMOD_LALT = KMOD_LALT
KMOD_RALT = KMOD_RALT
KMOD_ALT = KMOD_ALT
KMOD_LMETA = KMOD_LMETA
KMOD_RMETA = KMOD_RMETA
KMOD_META = KMOD_META
KMOD_NUM = KMOD_NUM
KMOD_MODE = KMOD_MODE
# surface flag
SRCALPHA = SRCALPHA
# other references
Rect = Rect
color = color

# mouse event values
MOTION_LEFT = 0
MOTION_MIDDLE = 1
MOTION_RIGHT = 2
BUTTON_LEFT = 1
BUTTON_MIDDLE = 2
BUTTON_RIGHT = 3
BUTTON_THUMB_FRONT = 6
BUTTON_THUMB_BACK = 7

# widget event types
PYGAME_WIDGETS = 18

E_WINDOW_ATTR = 100
E_WIDGET_ATTR = 101
E_HOLDER_ATTR = 102
E_LABEL_ATTR = 103
E_LABEL_TEXT = 104
E_BUTTON_PRESSED = 105
E_BUTTON_RELEASED = 106
E_BUTTON_BUMPED = 107
E_BUTTON_SLIDED = 108
E_BUTTON_MOUSEOVER = 109
E_BUTTON_MOUSEOUTSIDE = 110
E_BUTTON_ATTR = 111
E_BUTTON_APPEARANCE = 112
E_IMAGE_APPEARANCE = 113
E_LOOP_STARTED = 114

# text alignment
A_TOPLEFT = 0
A_CENTER = 1
A_BOTTOMRIGHT = 2


def Args(*args, **kwargs):
    """This is useful when adding event handler with args or kwargs. You don't have to pass it like list and dict, but
    you can type *Args(arg1, ..., key1=kwarg1, ...) to fill the arguments of Master.add_handler() method."""

    return args, kwargs


def button_wrapper(func, buttons=(BUTTON_LEFT,), self_arg=False, event_arg=False):
    """When adding handler for button click event, this wrapper calls the handling function only for specified mouse
    buttons. Pass button_wrapper(handling_func, (button1, ...)) to the func argument in Button_.add_handler().
    self_arg and event_arg must be True."""

    def handler(self, event, *args, **kwargs):
        if event.button in buttons and event.widget == self:
            if self_arg:
                args = [self] + list(args)
            if event_arg:
                args = [event] + list(args)
            func(*args, **kwargs)
    return handler


def button_bg(fill, edge, frame_thickness=1):
    """Returns a function, that can be used to create background surface for button."""

    background = frame(fill, edge, frame_thickness)

    def func(self, text):
        surf = background(self.master_rect.size)
        dest = (self.alignment_x * (self.master_rect.w - text.get_width()) / 2,
                self.alignment_y * (self.master_rect.h - text.get_height()) / 2)
        surf.blit(text, dest)
        surf.convert_alpha()
        return surf
    return func


def frame(fill, edge, thickness=1):
    """Returns a function, that creates surface of given size, which is filled with fill color and has a frame of
    given thickness and different color."""

    def func(size):
        if size == func.last_size:
            return func.last_surf.copy()
        surf = Surface(size, SRCALPHA)
        surf.fill(edge)
        if size[0] > 2 * thickness and size[1] > 2 * thickness:
            if fill[3] == 255:
                surf1 = Surface([a - (2 * thickness) for a in size], SRCALPHA)
                surf1.fill(fill)
                surf.blit(surf1, (thickness, thickness))
            else:
                for y in range(thickness, size[1] - thickness):
                    for x in range(thickness, size[0] - thickness):
                        surf.set_at((x, y), fill)
        func.last_size = size
        func.last_surf = surf.copy()
        return surf
    func.last_size = None
    func.last_surf = None
    return func
