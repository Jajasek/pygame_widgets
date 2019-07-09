import widget
import text
import pygame
import holder
from pygame.colordict import THECOLORS
from pygame.locals import *
pygame.init()

size = (600, 500)
okno = widget.Window(size, RESIZABLE)
surf = pygame.Surface(size)
color = [255, 0, 0]
surf.fill(color)
okno.change_surface(surf)
Widget = holder.Holder(okno, size=(500, 200))
Label = text.Label(Widget, (100, 50), (200, 10), font_color=(255, 255, 255), smooth=False,
                   text="Hello World", font_size=30, bold=True, auto_res=True, alignment_x=2)
Label2 = text.Label(Widget, (50, 20), (200, 30), font_color=(255, 0, 0), text="This is a subsubwidget of okno", bg_color=THECOLORS['blue1'])
Label3 = text.Label(Widget, auto_res=True, text="I dont know", font_color=THECOLORS['salmon'])
LabelHelp = text.Label(okno, (0, 50), auto_res=True, text='T, C: _font; Esc, Enter: connection; '
                                                          'Arrows: _font size; else: visibility')
Running = True
pygame.display.flip()

while Running:
    okno.update_display()
    for event in pygame.event.get():
        okno.handle_events(event)
        if event.type == MOUSEMOTION:
            if event.buttons[0]:
                Label.move_resize(event.pos, 'abs')
            if event.buttons[1]:
                Label2.move_resize(event.rel, 'rel')
            if event.buttons[2]:
                Widget.move_resize(event.rel, 'rel')
        elif event.type == KEYDOWN:
            if event.key == K_t:
                Label.set(font_name="trebuchetms")
            elif event.key == K_c:
                Label.set(font_name="calibri")
            elif event.key == K_RETURN:
                print(Label2.reconnect())
            elif event.key == K_ESCAPE:
                Label2.disconnect()
            elif event.key == K_DOWN:
                Label.set(font_size=20)
            elif event.key == K_UP:
                Label.set(font_size=40)
            elif event.key == K_RIGHT:
                okno.surface.blit(okno.my_surf, (0, 0))
                print(Label2.connected)
            else:
                Label.set(visible=not Label.visible)

