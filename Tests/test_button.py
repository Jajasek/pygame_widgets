import pygame_widgets
from pygame_widgets.constants.public import *


def Zmacknuti(event, okno):
    okno.set(size=okno.attributes.size1 if event.button == BUTTON_LEFT else okno.attributes.size2)


def PretahnutiSS(self, value):
    self.attributes.drag = value


def Pretahnuti(event, self):
    if event.buttons[MOTION_LEFT] and self.attributes.drag:
        self.move_resize(event.rel, 'rel')


Okno = pygame_widgets.Window((500, 300), RESIZABLE)
Okno.attributes.size1 = (500, 400)
Okno.attributes.size2 = (300, 300)
Tlaco2 = pygame_widgets.Button(Okno, size=(100, 20), text='Pretahni me')
Tlaco2.attributes.drag = False
Tlaco2.add_handler(BUTTON_PRESSED, button_wrapper(PretahnutiSS), *Args(True))
Tlaco2.add_handler(BUTTON_RELEASED, button_wrapper(PretahnutiSS), *Args(False))
Tlaco2.add_handler(MOUSEMOTION, Pretahnuti)
Tlaco = pygame_widgets.Button(Okno, (200, 150), (100, 20), text='Zmackni me')
Tlaco.add_handler(BUTTON_BUMPED, button_wrapper(Zmacknuti, (BUTTON_LEFT, BUTTON_RIGHT), True), [Okno], self_arg=False)

while True:
    events = pygame_widgets.pygame.event.get()
    if events:
        pass
        # print(*events, sep='\n')
    Okno.handle_events(*events)
    Okno.update_display()
