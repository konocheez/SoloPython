import pygame
from os.path import join

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


walkRight = [pygame.image.load(join('tims_pygame_images', 'R1.png')),
pygame.image.load(join('tims_pygame_images', 'R2.png')),
pygame.image.load(join('tims_pygame_images', 'R3.png')),
pygame.image.load(join('tims_pygame_images', 'R4.png')),
pygame.image.load(join('tims_pygame_images', 'R5.png')),
pygame.image.load(join('tims_pygame_images', 'R6.png')),
pygame.image.load(join('tims_pygame_images', 'R7.png')),
pygame.image.load(join('tims_pygame_images', 'R8.png')),
pygame.image.load(join('tims_pygame_images', 'R9.png'))]

walkLeft = [pygame.image.load(join('tims_pygame_images', 'L1.png')),
pygame.image.load(join('tims_pygame_images', 'L2.png')),
pygame.image.load(join('tims_pygame_images', 'L3.png')),
pygame.image.load(join('tims_pygame_images', 'L4.png')),
pygame.image.load(join('tims_pygame_images', 'L5.png')),
pygame.image.load(join('tims_pygame_images', 'L6.png')),
pygame.image.load(join('tims_pygame_images', 'L7.png')),
pygame.image.load(join('tims_pygame_images', 'L8.png')),
pygame.image.load(join('tims_pygame_images', 'L9.png'))]

bg = pygame.image.load(join('tims_pygame_images', 'bg.jpg'))
char = pygame.image.load(join('tims_pygame_images', 'standing.png'))

display_height = 500
display_width = 480

win = pygame.display.set_mode((display_height, display_width))
pygame.display.set_caption("First Game")

x = 50
y = 400
width = 64
height = 64
acc = 0
vel = 10

isJump = False
jumpCount = 10
left = False
right = False
walkCount = 0

def redrawGameWindow():
    global walkCount


    win.fill((0,0,0))
    win.blit(bg, (0,0))

    if walkCount + 1 >= 27: #9 sprites, show each sprite for 3 frames
        walkCount = 0
    if left:
        win.blit(walkLeft[walkCount//6], (x, y))
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount//6], (x, y))
        walkCount += 1
    else:
        win.blit(char, (x, y))

    pygame.display.update()

#mainloop

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(54)
    pygame.time.delay(100) #delays by 100ms so game isn't too fast

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < 500 - width - vel:
        x += vel
        right = True
        left = False
    else:
        right = False
        left = False
        walkCount = 0

    if not isJump:
        if keys[pygame.K_UP]:
            isJump = True
            right = False
            left = False
            walkCount = 0
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            #quadratic for parabolic effect of jump
            #sprite moves up less after each count, then moves down @jumpCount = 0
            jumpCount -= 1

        else:
            isJump = False
            jumpCount = 10


    # """This is the screen loopy boy"""
    # if y < 0:
    #     y = display_height
    # elif y > display_height:
    #     y = 0
    #
    # if x < 0:
    #     x = display_width
    # elif x > display_width:
    #     x = 0

    redrawGameWindow()

pygame.quit()
