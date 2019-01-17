import pygame_widgets as pw
from public import *


def zmena_okna(self):
    global size
    size = Okno.surface.get_size()
    self.my_surf = pw.pygame.Surface(size, SRCALPHA)
    color = self.get_u('bg_color')[0]
    self.my_surf.fill(color)
    self.my_surf.convert()
    self.blit(self.surface.get_rect())
    self.add_update(self.surface.get_rect())


def Pripojeni(self, event):
    (self.disconnect() if self.connected else self.reconnect()) if event.key == K_c else None
    print('Pripojeni')


def Pohyb(self, event, btn, rel):
    try:
        b = event.buttons[btn]
    except AttributeError:
        b = event.button == btn
    if b:
        self.move_resize(event.rel if rel == 'rel' else event.pos, rel)


size = (700, 500)
Okno = pw.Window(size, RESIZABLE, min_size=(350, 250), max_size=(1920, 1080))
Okno.set_u(bg_color=THECOLORS['gray40'])
Okno.add_handler(VIDEORESIZE, zmena_okna, self_arg=True, event_arg=False, call_if_handled_by_children=True)
L_0 = pw.Label(Okno, auto_res=True, text='napoveda: ', font_color=THECOLORS['yellow3'], bg_color=THECOLORS['black'])
H_0 = pw.Holder(Okno, topleft=(100, 100), size=(400, 200))
L_1_0 = pw.Label(H_0, size=(190, 50), text='Label_1_0', bg_color=THECOLORS['wheat1'], font_color=THECOLORS['black'],
                 font_size=30, alignment_x=2, alignment_y=0)
L_1_1 = pw.Label(H_0, topleft=(0, 60), text='Label_1_1', auto_res=True, bold=True, underlined=True, italic=True,
                 font_size=25)
Okno.children.reverse()
H_0.children.reverse()

L_1_0.add_handler(KEYDOWN, Pripojeni)
L_1_0.add_handler(MOUSEMOTION, Pohyb, [1, 'rel'])
L_1_1.add_handler(KEYDOWN, lambda self, event: self.set(visible=not self.visible) if event.key == K_v else None)
L_1_1.add_handler(MOUSEBUTTONDOWN, Pohyb, [1, 'abs'])
L_1_1.add_handler(MOUSEMOTION, Pohyb, [0, 'abs'])


while True:
    events = pw.pygame.event.get()
    Okno.handle_events(*events)
    for e in events:
        if e.type == KEYDOWN:
            if e.key == K_c and (e.mod & KMOD_LCTRL):
                L_1_0.reconnect()
    Okno.update_display()
