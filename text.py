import pygame_widgets.widget as W
import pygame as pg
import pygame_widgets.constants.private as CONST
from pygame_widgets.constants.public import *
pg.font.init()


class Text_(W.Widget_):
    """Base widget tor text widgets. Supplies text updating. Cannot be instaned."""

    def __init__(self, master, rect, **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, rect, **updated)
        self.font = None
        self.font_name = "calibri"
        self.font_size = 16

        self.bold = False
        self.italic = False
        self.underlined = False

        self.font_color = THECOLORS['black']
        self.bg_color = None
        self.smooth = True
        self.text = ""
        self.alignment_x = 1
        self.alignment_y = 1

        self.pub_arg_dict["Text_new_font"] = ["font_name", "font_size"]
        self.pub_arg_dict["Text_set_font"] = ["bold", "italic", "underlined"]
        self.pub_arg_dict["Text_render"] = ["font_color", "bg_color", "smooth", "text", "alignment_x", "alignment_y"]

        self.safe_init(**kwargs)

    def new_font(self):
        """Creates new pygame.font.Font object according to actual settings.
        Private."""

        self.font = pg.font.SysFont(self.font_name, self.font_size, self.bold, self.italic)
        self.font.set_underline(self.underlined)

    def set_font(self):
        """Adjusts the current pygame.font.Font object according to actual settings.
        Private."""

        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)
        self.font.set_underline(self.underlined)

    def set_update(self, old=None, **kwargs):
        """Actualises its image on the screen after setting new values to attributes in most efficient way.
        Private."""

        if kwargs:
            new = False
            set = False
            render = False
            for name in kwargs.keys():
                if name in self.pub_arg_dict["Text_render"]:
                    render = True
                elif name in self.pub_arg_dict["Text_set_font"]:
                    set = True
                elif name in self.pub_arg_dict["Text_new_font"]:
                    new = True
                    break
            if new:
                self.new_font()
            elif set:
                self.set_font()
            if new or set or render:
                old_surf = self.my_surf.copy()
                self.generate_surf()
                if old_surf.get_size() != self.my_surf.get_size():
                    self.disappear()
                    self.master_rect.size = self.my_surf.get_size()
                    self.create_subsurface()
                if old_surf != self.my_surf:
                    self.appear()
            self.set_event(old, **kwargs)


class Label(Text_):
    """Widget with 1-line unchangable text on a solid or transparent background."""

    def __init__(self, master, topleft=(0, 0), size=(1, 1), **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, Rect(topleft, size), **updated)
        self.new_font()
        self.safe_init(**kwargs)

    def generate_surf(self):
        """Generates new surface of appearance.
        Private."""

        text = self.font.render(self.text, self.smooth, self.font_color, self.bg_color)
        if self.auto_res:
            self.my_surf = text
            return
        self.my_surf = pg.Surface(self.master_rect.size, SRCALPHA)
        self.my_surf.fill(self.bg_color if self.bg_color else THECOLORS['transparent'])
        dest = (self.alignment_x * (self.my_surf.get_width() - text.get_width()) / 2,
                self.alignment_y * (self.my_surf.get_height() - text.get_height()) / 2)
        self.my_surf.blit(text, dest)
        self.my_surf.convert_alpha()

    def set_event(self, old=None, **kwargs):
        """Places events on the queue based on changed attributes.
        Private."""

        if old is None:
            old = dict()
        for name, value in kwargs.items():
            pg.event.post(pg.event.Event(LABEL_TEXT if name == 'text' else LABEL_ATTR, widget=self,
                                         name=name, new=value, old=old[name] if name in old else None))


class Button(Text_):
    def __init__(self, master, topleft=(0, 0), size=(1, 1), **kwargs):
        updated = kwargs.copy()
        updated[CONST.SUPER] = True
        super().__init__(master, Rect(topleft, size), **updated)
        self.new_font()
        self.safe_init(**kwargs)
