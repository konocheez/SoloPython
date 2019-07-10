# Pygame template - skeleton for a new pygame project
import pygame as pg
import random

WIDTH = 360
HEIGHT = 480
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game")
clock = pg.time.Clock()

def main():
    # Game loop
    running = True
    while running:
        # keep loop running at the right speed
        clock.tick(FPS)
        # Process input (events)
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                running = False

        # Update

        # Draw / render
        screen.fill(BLACK)
        # *after* drawing everything, flip the display
        pg.display.flip()

    pg.quit()

if __main__ = "__name__":
    main()
