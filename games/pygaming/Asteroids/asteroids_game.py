"""This is the asteroids game I've just really wanted to work on. This is the third attempt since I had a lot of trouble with using pygame rotation and then began implementation with a more developed engine based on pygame."""

import pygame
import random
from math import cos, sin, pi, degrees, radians

WIDTH = 800
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

bg = pygame.image.load('stars.png').convert_alpha()
surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
surf.fill(BLACK)
surf = surf.convert_alpha()
bg.set_alpha(50)
surf.set_alpha(255)

class Ship(pygame.sprite.Sprite):

    def __init__(self, w_speed = 9, linspeed = 0, accel = 0.2   , x = (WIDTH/2), y = (HEIGHT/2)):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.w_speed = w_speed
        self.linspeed = linspeed
        self.accel = accel

        self.image = pygame.image.load('ship1.png') # this is a surface, confirmed
        self.orig_image = self.image
        self.image.convert_alpha(self.image)
        # if you have overlay problems try to implement SRCALPHA
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.pos = pygame.math.Vector2(self.rect.centerx, self.rect.top)
        self.angle = radians(180)

        self.offset = pygame.math.Vector2(0, 0)
        self.trajectory = pygame.math.Vector2(cos(self.angle), sin(self.angle)) # trajectory for blasters and ship motion
        self.trajectory = self.trajectory.rotate(90) #so that the blasters are collinear

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pygame.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center = (self.pos + offset_rotated))

    def update(self, win):
        self.rotate()
        self.direction = self.trajectory.rotate(self.angle)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, rocksize):
        super().__init__()

        k = random.random() # temp val for x
        j = random.random() # temp val for y

        if round(k) == 1:
            self.x = random.randint(0, WIDTH)
        elif k > 0.25:
            self.x = 0
        else:
            self.x = WIDTH

        if round(j) == 0:
            self.y = random.randint(0, HEIGHT)
        elif j > 0.25:
            self.y = 0
        else:
            self.y = HEIGHT

        self.speed = random.randrange(0, 10)
        self.image = pygame.image.load(rocksize)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.pos = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.angle = radians(random.random()*2*pi) # randomized angle for trajectory

        self.offset = pygame.math.Vector2(0, 0)
        self.trajectory = pygame.math.Vector2(cos(self.angle), sin(self.angle)) # trajectory for blasters
        self.trajectory = self.trajectory.rotate(90) # controls direction of asteroid

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pygame.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        # self.rect = self.image.get_rect(center = (width / 2 + 5, height / 2 + 50))
        self.rect = self.image.get_rect(center = (self.pos + offset_rotated))

    def update(self, win, dt):
        self.rotate()
        self.angle += radians(random.randrange(-5, 5))
        self.direction = self.trajectory.rotate(self.angle)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

class Blast(pygame.sprite.Sprite):
    def __init__(self, pos, direction, color, radius):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.color = color
        self.radius = radius
        self.linspeed = 8
        # self.image.set_colorkey((0, 0, 0))
        # pygame.draw.circle(self.image, pygame.Color('green'), (4, 4), 4)
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.pos = pygame.math.Vector2(self.rect.center)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.rect.centerx), int(self.rect.centery)), self.radius)

    def update(self, win, dt):
        self.pos += self.direction * self.linspeed
        self.rect.center = self.pos

def main():
    # value/sprite initialization
    ship = Ship()
    shootloop = 0
    blasts = []
    asteroids = []
    if shootloop > 0:
        shootloop += 1
    if shootloop > 1:
        shootloop = 0
    dt = 0
    all_sprites = pygame.sprite.Group()
    all_sprites.add(ship)

    running = True
    # Game loop
    while running:
        # keep loop running at the right speed
        dt = clock.tick(FPS)
        keys = pygame.key.get_pressed() # needs to go in the while loop

        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False

        # blasters
        if keys[pygame.K_SPACE]: #to be shot automatically
            if len(blasts) < 1:
                blasts.append(Blast(ship.rect.center, ship.direction, WHITE, 2))
            shootloop += 1
        for blast in blasts:
            #if the bullet is within the x bounds of the screen, move it
            #otherwise, remove it from gameplay (pop)

            if blast.rect.centerx < WIDTH and blast.rect.centerx > 0 and blast.rect.centery < HEIGHT and blast.rect.centery > 0:
                blast.update(win, dt)
            else:
                blasts.pop(blasts.index(blast))

        # asteroids data
        # as long as there are 10 or less asteroids in play, the game will produce asteroids
        print(len(asteroids))
        while len(asteroids) < 10:
            asteroids.append(Asteroid('big_asteroid.png'))
            shootloop += 1
        for rock in asteroids:
            #if the asteroid is within the x bounds of the screen, move it
            #otherwise, remove it from gameplay (pop)
            if rock.rect.centerx < WIDTH and rock.rect.centerx > 0 and rock.rect.centery < HEIGHT and rock.rect.centery > 0:
                rock.update(win, dt)
                rock.draw(win)
            else:
                asteroids.pop(asteroids.index(rock))

        # if keys[pygame.K_DOWN]:
        #     asteroids.append(Asteroid('big_asteroid.png'))
        #
        #     win.blit(asteroid.image, (asteroid.x, asteroid.y))
        # ship navigation
        if keys[pygame.K_LEFT]:
            ship.angle -= ship.w_speed
        if keys[pygame.K_RIGHT]:
            ship.angle += ship.w_speed

        # thrusters with acceleration and de-acceleration
        # print(ship.linspeed)
        if keys[pygame.K_UP]:
            ship.linspeed += ship.accel
            ship.pos += ship.direction * ship.linspeed
            if ship.linspeed >= 5:
                ship.linspeed -= ship.accel/2
                ship.pos += ship.direction * ship.linspeed

        # when not being pressed, set linspeed to de-accelerate
        if not keys[pygame.K_UP] and ship.linspeed > 0:
            ship.linspeed -= ship.accel
            ship.pos += ship.direction * ship.linspeed


        # loop to other side of screen if exits screen
        if ship.y < 0:
            ship.y = HEIGHT
        elif ship.y > HEIGHT:
            ship.y = 0

        if ship.x < 0:
            ship.x = WIDTH
        elif ship.x > WIDTH:
            ship.x -= self.accel

        # Update
        win.blit(bg, (0, 0))

        # surf.blit(bg, bg.get_rect())
        # win.blit(surf, surf.get_rect())
        # # win.blit(bg, (0,0))
        ship.update(win)

        # print("\nRight: " + str(ship.rect.right))
        # print("Left: " + str(ship.rect.left))
        # print("Width: " + str(WIDTH))

        all_sprites.draw(win) #i'm pretty sure this blits everything, yep it blits everything
        # for some reason all_sprites draw works very effectively for coordinates
        for blast in blasts:
            blast.draw(win)

        # *after* drawing everything, flip the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
