import pygame_widgets
from pygame_widgets.constants import *


def Zmacknuti(event, okno):
    okno.set(size=okno.attributes.size1 if event.button == BUTTON_LEFT else okno.attributes.size2)


def PretahnutiSS(self, value):
    self.attributes.drag = value


def Pretahnuti(self, event):
    if event.buttons[MOTION_LEFT] and self.attributes.drag:
        self.move_resize(event.rel, 'rel')


Okno = pygame_widgets.Window((500, 300), RESIZABLE)
Okno.attributes.size1 = (500, 400)
Okno.attributes.size2 = (300, 300)
Tlaco2 = pygame_widgets.Button(Okno, topleft=(0, 200), size=(100, 20), text='Pretahni me')
Tlaco2.attributes.drag = False
Tlaco2.add_handler(E_BUTTON_PRESSED, button_wrapper(PretahnutiSS, self_arg=True), *Args(True))
Tlaco2.add_handler(E_BUTTON_RELEASED, button_wrapper(PretahnutiSS, self_arg=True), *Args(False))
Tlaco2.add_handler(MOUSEMOTION, Pretahnuti)
Tlaco2.handlers[MOUSEMOTION] = [Tlaco2.handlers[MOUSEMOTION][-1]] + Tlaco2.handlers[MOUSEMOTION][:-1]
Tlaco = pygame_widgets.Button(Okno, (200, 150), (100, 20), text='Zmackni me')
Tlaco.add_handler(E_BUTTON_BUMPED, button_wrapper(Zmacknuti, (BUTTON_LEFT, BUTTON_RIGHT), event_arg=True), [Okno])
Textove_pole = pygame_widgets.Entry(Okno, (100, 100), (200, 20))
cursor = pygame_widgets.pygame.cursors.compile(pygame_widgets.pygame.cursors.textmarker_strings)
pygame_widgets.pygame.mouse.set_cursor((8, 16), (4, 8), *cursor)

while True:
    events = pygame_widgets.pygame.event.get()
    if events:
        pass
        # print(*events, sep='\n')
    for e in events:
        Okno.handle_event(e)
    Okno.update_display()
