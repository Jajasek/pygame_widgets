import pygame_widgets as pw


def main():
    okno = pw.Window((300, 300))

    while True:
        events = pw.pygame.event.get()
        okno.handle_events(*events)
        for e in events:
            print(e)


if __name__ == '__main__':
    main()
