import pygame_widgets
from pygame_widgets.constants import *
import pathlib


def main():
    Okno = pygame_widgets.Window((500, 300), RESIZABLE)
    with open("TestFile.gif", "rb") as file:
        gif = pygame_widgets.Gif(Okno, running=True, auto_res=True, filename=file)
    while True:
        events = pygame_widgets.pygame.event.get()
        for e in events:
            Okno.handle_event(e)
        pygame_widgets.new_loop(Okno)


if __name__ == '__main__':
    main()
