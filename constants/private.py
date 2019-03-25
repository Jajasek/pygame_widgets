from public import THECOLORS, SRCALPHA
from pygame import Surface


def button_bg(fill, edge):
    def func(self, text):
        surf = Surface(self.master_rect.size, SRCALPHA)
        surf.fill(edge)
        if self.master_rect.size[0] > 2 and self.master_rect.size[1] > 2:
            surf1 = Surface([a - 2 for a in self.master_rect.size], SRCALPHA)
            surf1.fill(fill)
            surf.blit(surf1, (1, 1))
        dest = (self.alignment_x * (self.master_rect.w - text.get_width()) / 2,
                self.alignment_y * (self.master_rect.h - text.get_height()) / 2)
        surf.blit(text, dest)
        surf.convert_alpha()
        return surf
    return func


class DEFAULT:
    # window attributes
    fps = 25
    window_color = THECOLORS['white']
    # Label attributes
    bg_color = THECOLORS['transparent']
    font_color = THECOLORS['black']
    font = 'calibri'
    font_size = 16
    # button attributes
    bg_normal = button_bg(THECOLORS['gray80'], THECOLORS['gray65'])
    bg_mouseover = button_bg(THECOLORS['lightblue1'], THECOLORS['blue'])
    bg_pressed = button_bg(THECOLORS['lightblue3'], THECOLORS['blue'])


SUPER = 's'  # kwarg used to detect if the class is initialising as super() or not
