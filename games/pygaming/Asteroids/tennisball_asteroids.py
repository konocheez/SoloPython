import pygame
from math import cos, sin, pi, degrees, radians

pygame.init()

#game colors

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
turquoise = (0, 255, 255)
cottoncandy = (255, 179, 230)
amonscolor = (200, 0, 200)

# all_sprites = pygame.sprite.Group() #group to allow all sprites to be updated
# tennisballs = [] #list to enable multiple tennis balls to exist on screen


#initialize pygame and create window
width = 700
height = 700
fps = 20

win = pygame.display.set_mode((width, height))

pygame.display.set_caption("Tennis Ball Machine")
pygame.mixer.init() #handles sound effects/music

clock = pygame.time.Clock()

class Machine(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((5, 5))
        self.image.fill(white)

        self.rect = self.image.get_rect()

        self.rect.center = (width / 2, height /2)

# win.blit(win, (255, 0, 0), (self.x, self.y))

    def update(self, win):
        #restricted game bounds

        # win.blit(self.image, self.rect.center)
        win.blit(self.image, ((width / 2) - 20, (height / 2) - 25))

        if self.rect.left > width:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = width
        if self.rect.bottom > 0:
            self.rect.top = height
        if self.rect.top > height:
            self.rect.bottom = 0

class Shooterthing(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('ship1.png')
        self.orig_image = self.image
        self.image.convert_alpha(self.image)

        # self.image.fill(green)

        self.rect = self.image.get_rect()

        self.rect.center = ((width / 2), (height / 2))

        self.pos = pygame.math.Vector2(self.rect.centerx, self.rect.top)
        self.angle = radians(180)

        self.offset = pygame.math.Vector2(0, 0)
        self.trajectory = pygame.math.Vector2(cos(self.angle), sin(self.angle))
        self.trajectory = self.trajectory.rotate(90) #so that the balls shoot collinearly with shooter

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pygame.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        # self.rect = self.image.get_rect(center = (width / 2 + 5, height / 2 + 50))
        self.rect = self.image.get_rect(center = (self.pos + offset_rotated))

    def update(self, win):
        self.rotate()
        self.direction = self.trajectory.rotate(self.angle)

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos, direction, color, radius):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.color = color
        self.radius = radius
        # self.image.set_colorkey((0, 0, 0))
        # pygame.draw.circle(self.image, pygame.Color('green'), (4, 4), 4)
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.pos = pygame.math.Vector2(self.rect.center)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.rect.centerx), int(self.rect.centery)), self.radius)

    def update(self, win, dt):
        self.pos += self.direction * dt
        self.rect.center = self.pos

def main():
    #initialized values / runs only once when game is started

    all_sprites = pygame.sprite.Group() #group to allow all sprites to be updated
    tennisballs = [] #list to enable multiple tennis balls to exist on screen

    shooter = Shooterthing()
    machine = Machine()
    all_sprites.add(machine)
    all_sprites.add(shooter)
    shootloop = 0
    dt = 0
    #game loop / no looping happens before here
    running = True

    while running:
        #process input (events)
        dt = clock.tick(fps)

        if shootloop > 0:
            shootloop += 1
        if shootloop > 3:
            shootloop = 0

        # trajectory = pygame.math.Vector2(cos(shooter.angle), sin(shooter.angle))

        for event in pygame.event.get():
            #check for closing window
            if event.type == pygame.QUIT:
                running = False

        for ball in tennisballs:
            #if the bullet is within the x bounds of the screen, move it
            #otherwise, remove it from gameplay (pop)

            if ball.rect.centerx < width and ball.rect.centerx > 0:
                ball.update(win, dt)
            else:
                tennisballs.pop(tennisballs.index(ball))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_x]: #to be shot automatically
            if len(tennisballs) < 20:
                tennisballs.append(Ball(shooter.rect.center, shooter.direction, green, 5))
            shootloop += 1

        if keys[pygame.K_z]:
            shooter.angle += 9

        if keys[pygame.K_c]:
            shooter.angle -= 9

        #update
        win.fill(black)
        all_sprites.update(win)
        shooter.update(win)

        #draw / render
        all_sprites.draw(win)


        for ball in tennisballs:
            ball.draw(win)

        # after drawing everything, flip (update) the display
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
