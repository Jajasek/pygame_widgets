import pygame_widgets as pw
from pygame.locals import *

size = 0, 0
label_x, label_y = label_size = 220, 180
Okno = pw.Window(size, RESIZABLE)
size = Okno.surface.get_size()
surf = pw.pygame.Surface(size)
surf.fill(pw.THECOLORS['red2'])
Okno.change_surface(surf)
pw.pygame.display.flip()
PomocnyWidget = pw.Holder(Okno, size=Okno.surface.get_size())
for i in range(size[0] // label_x):
    labels = list()
    for j in range(size[1] // label_y):
        labels.append(pw.Label(PomocnyWidget, size=label_size, font_size=100, bold=True, bg_color=pw.THECOLORS['red4'],
                               font_color=pw.THECOLORS['white'], text=f"{i}; {j}"))
    PomocnyWidget.create_row_layout(*labels, vertical=False, size=(0, size[1]), relative_position=(
        (int(i*(size[0] / (size[0] // label_x))), "left", None, "left"), (0, "top", None, "top")))

Okno.update_display()
pw.pygame.event.get()
print("cus")

print()
while True:
    Okno.handle_events(*[e for e in pw.pygame.event.get() if e != VIDEORESIZE])
    Okno.update_display()
