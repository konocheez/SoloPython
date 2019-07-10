import pygame

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

display_height = 500
display_width = 500

win = pygame.display.set_mode((display_height, display_width))
pygame.display.set_caption("First Game")

x = 50
y = 50
width = 40
height = 60
acc = 0
vel = 5

isJump = False
jumpCount = 10

running = True
while running:
    pygame.time.delay(100) #delays by 100ms so game isn't too fast

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    keys = pygame.key.get_pressed()

    # if keys[pygame.K_LEFT]:
    #     x -= vel
    # if keys[pygame.K_RIGHT]:
    #     x += vel
    # if keys[pygame.K_UP]:
    #     y -= vel
    # if keys[pygame.K_DOWN]:
    #     y += vel

    # if event.key == pygame.K_LEFT:
    #alternative style

    """Playing with acceleration"""

    # if event.type == pygame.KEYDOWN:
    """requires key to be held down for any movement (i.e. jump
    freezes when released)"""

    #for locked boundaries on screen
    # if keys[pygame.K_LEFT] and x > vel:
    if keys[pygame.K_LEFT]:
        acc = 1
        if vel <= 50:
            vel += acc
        x -= vel
    # if keys[pygame.K_RIGHT] and x < 500 - vel - width:
    if keys[pygame.K_RIGHT]:
        acc = 1
        if vel <= 50:
            vel += acc
        x += vel
    # if keys[pygame.K_UP] and y > vel:
    if not isJump:
        if keys[pygame.K_UP]:
            acc = 1
            if vel <= 50:
                vel += acc
            y -= vel
        # if keys[pygame.K_DOWN] and y < 500 - height - vel:
        if keys[pygame.K_DOWN]:
            acc = 1
            if vel <= 50:
                vel += acc
            y += vel
        if keys[pygame.K_SPACE]:
            isJump = True
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
    if event.type == pygame.KEYUP:
        acc = 0
        vel = 5

    """This is the screen loopy boy"""
    if y < 0:
        y = display_height
    elif y > display_height:
        y = 0

    if x < 0:
        x = display_width
    elif x > display_width:
        x = 0



    win.fill((0,0,0))
    pygame.draw.rect(win, (255, 0, 255), (x, y, width, height))

    pygame.display.update()

pygame.quit()
