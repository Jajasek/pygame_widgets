import pygame_widgets as pw
from pygame_widgets.constants import *


def zmena_okna(self):
    global size
    size = self.surface.get_size()
    print(f'zmena_okna: {size}')
    self.my_surf = pw.pygame.Surface(size, SRCALPHA)
    color = self.attr.bg_color
    print(color)
    self.my_surf.fill(color)
    self.my_surf.convert()
    self.blit()
    self.add_update(self.surface.get_rect())


def Pripojeni(self, event):
    (self.disconnect() if self.connected else self.reconnect()) if event.key == K_c else None
    print('Pripojeni')


def Objeveni(self, event):
    if event.key != K_a:
        return
    if self.attr.onscreen:
        self.disappear()
    else:
        self.appear()
    self.attr.onscreen = not self.attr.onscreen


def Pohyb(self, event, btn, rel):
    print(f'moving {self}')
    try:
        b = event.buttons[btn]
    except AttributeError:
        b = event.button == btn
    if b:
        self.move_resize(event.rel if rel == 0 else event.pos, rel)


def main():
    size = (700, 500)
    Okno = pw.Window(size, RESIZABLE, min_size=(350, 250), max_size=(1920, 1080))
    Okno.attr.bg_color = THECOLORS['gray42']
    Okno.add_handler(VIDEORESIZE, zmena_okna, self_arg=True, event_arg=False)
    Okno.update_display()
    L_0 = pw.Label(Okno, auto_res=True, text=str(Okno.fps), font_color=THECOLORS['yellow3'], bg_color=THECOLORS['black'])
    print('L_0:', L_0.connected)
    Okno.update_display()
    H_0 = pw.Holder(Okno, topleft=(-40, 100), size=(400, 200))
    print('H_0:', H_0.connected)
    Okno.update_display()
    """L_1_0 = pw.Label(H_0, size=(190, 50), text='Label_1_0', background=THECOLORS['wheat1'], font_color=THECOLORS['black'],
                     font_size=30, alignment_x=2, alignment_y=0)"""
    L_1_0 = pw.Holder(H_0, topleft=(50, 100), size=(190, 50), color=THECOLORS['yellow1'])
    L_1_0.move_resize()
    print('L_1_0:', L_1_0.connected)
    Okno.update_display()
    L_1_1 = pw.Label(H_0, topleft=(0, 60), text='Label_1_1', auto_res=True, bold=True, underlined=True, italic=True,
                     font_size=25)
    L_1_0.attr['onscreen'] = True
    print('L_1_1:', L_1_1.connected)
    Okno.update_display()
    Okno.children.reverse()
    H_0.children.reverse()

    L_1_0.add_handler(KEYDOWN, Pripojeni)
    L_1_0.add_handler(KEYDOWN, Objeveni)
    L_1_0.add_handler(MOUSEMOTION, Pohyb, *Args(MOTION_MIDDLE, 0))
    L_1_1.add_handler(KEYDOWN, lambda self, event: self.set(visible=not self.visible) if event.key == K_v else None)
    L_1_1.add_handler(MOUSEBUTTONDOWN, Pohyb, *Args(BUTTON_LEFT, -1))
    L_1_1.add_handler(MOUSEMOTION, Pohyb, *Args(MOTION_LEFT, -1))
    H_0.add_handler(MOUSEMOTION, Pohyb, *Args(MOTION_RIGHT, 0))

    i = 0
    while True:
        events = pw.pygame.event.get()
        if events:
            pass
            # print(*events, sep='\n')
        Okno.handle_events(*events)
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_c and (e.mod & KMOD_LCTRL):
                    L_1_0.reconnect()
        L_0.set(text=str(Okno.clock.get_fps()))
        Okno.update_display()
        if i == 50:
            Okno.set(min_size=(None, 700))
        i += 1


if __name__ == '__main__':
    main()
