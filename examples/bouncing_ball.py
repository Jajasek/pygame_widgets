import pygame_widgets, pathlib

size = width, height = 320, 240
speed = [2, 2]

window = pygame_widgets.Window(size, bg_color=(0, 0, 0), fps=0)

ball_img = pygame_widgets.pygame.image.load(f"{pathlib.Path(__file__).parent.absolute()}\\intro_ball.png")
ball = pygame_widgets.Image(window, auto_res=True, image=ball_img)

while True:
    window.handle_events(*pygame_widgets.pygame.event.get())
    ball.move_resize(speed)
    
    if ball.master_rect.left <= 0 or ball.master_rect.right >= width:
        speed[0] *= -1
    if ball.master_rect.top <= 0 or ball.master_rect.bottom >= height:
        speed[1] *= -1
    
    pygame_widgets.new_loop(window)
