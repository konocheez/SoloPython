import pygame
from os.path import join
import time


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 15, self.y + 12, 29, 52)
    def draw(self, win, walkLeft, walkRight):
        if self.walkCount + 1 >= 27:
            #total 9 sprites, show each sprite for 3 frames
            self.walkCount = 0

        if not (self.standing):
            #walks to the right or the left
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            #stands looking to the right or the left
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 15, self.y + 12, 29, 52)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 20 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy(object):
    GwalkRight = [pygame.image.load(join('tims_pygame_images', 'R1E.png')),
    pygame.image.load(join('tims_pygame_images', 'R2E.png')),
    pygame.image.load(join('tims_pygame_images', 'R3E.png')),
    pygame.image.load(join('tims_pygame_images', 'R4E.png')),
    pygame.image.load(join('tims_pygame_images', 'R5E.png')),
    pygame.image.load(join('tims_pygame_images', 'R6E.png')),
    pygame.image.load(join('tims_pygame_images', 'R7E.png')),
    pygame.image.load(join('tims_pygame_images', 'R8E.png')),
    pygame.image.load(join('tims_pygame_images', 'R9E.png')),
    pygame.image.load(join('tims_pygame_images', 'R10E.png')),
    pygame.image.load(join('tims_pygame_images', 'R11E.png'))]

    GwalkLeft = [pygame.image.load(join('tims_pygame_images', 'L1E.png')),
    pygame.image.load(join('tims_pygame_images', 'L2E.png')),
    pygame.image.load(join('tims_pygame_images', 'L3E.png')),
    pygame.image.load(join('tims_pygame_images', 'L4E.png')),
    pygame.image.load(join('tims_pygame_images', 'L5E.png')),
    pygame.image.load(join('tims_pygame_images', 'L6E.png')),
    pygame.image.load(join('tims_pygame_images', 'L7E.png')),
    pygame.image.load(join('tims_pygame_images', 'L8E.png')),
    pygame.image.load(join('tims_pygame_images', 'L9E.png')),
    pygame.image.load(join('tims_pygame_images', 'L10E.png')),
    pygame.image.load(join('tims_pygame_images', 'L11E.png'))]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 15, self.y + 2, 31, 57)

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(self.GwalkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1

        else:
            win.blit(self.GwalkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        self.hitbox = (self.x + 15, self.y + 2, 31, 57)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x < self.vel + self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

        else:
            if self.x > self.vel + self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

    def hit(self):
        print('THE GOBLIN HAS BEEN STRUCK')


def redrawGameWindow(win, bg, man, goblin):
    win.blit(bg, (0,0))
    man.draw(win, walkLeft, walkLeft)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

man = player(200, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 300)

#mainloop
def main():

    pygame.init()

    display_height = 500
    display_width = 480

    win = pygame.display.set_mode((display_height, display_width))
    pygame.display.set_caption("First Game")

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

    clock = pygame.time.Clock()
    shootloop = 0

    bullets = []
    running = True
    while running:
        clock.tick(27)

        if shootloop > 0:
            shootloop += 1
        if shootloop > 3:
            shootloop = 0
        #this is a bullet cooldown; shoots one bullet per 4 presses; prevents spamming

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        for bullet in bullets:
            radius_y = bullet.y - bullet.radius
            radius_x = bullet.x - bullet.radius
            gbox_top = goblin.hitbox[1]
            gbox_bottom = goblin.hitbox[1] + goblin.hitbox[3]
            gbox_left = goblin.hitbox[0]
            gbox_right = goblin.hitbox[0] + goblin.hitbox[2]

            if radius_y < gbox_bottom and radius_y > gbox_top:
                    if radius_x > gbox_left and radius_x < gbox_right:
                        goblin.hit()
                        bullets.pop(bullets.index(bullet))
                        #if bullet is in hitbox, hit goblin and delete bullets

            if bullet.x < 500 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and shootloop == 0:
        #len(bullets) == 0:
            if man.left:
                facing = -1
            else:
                facing = 1

            if len(bullets) <= 5:
                bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0, 0, 0), facing))

            shootloop = 1
                # time.sleep(1) #everything freezes, no bueno
                # pygame.time.delay(150) #also delay everything, no bueno

            #bullets are an empty list with unnamed projectiles appended with bullet features

        if keys[pygame.K_LEFT] and man.x > man.vel:
            man.x -= man.vel
            man.left = True
            man.right = False
            man.standing = False

        elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
            man.x += man.vel
            man.right = True
            man.left = False
            man.standing = False
        else:
            man.standing = True
            man.walkCount = 0

        if not (man.isJump):
            if keys[pygame.K_UP]:
                man.isJump = True
                man.right = False
                man.left = False
                man.walkCount = 0
        else:
            if man.jumpCount >= -10:
                man.y -= (man.jumpCount * abs(man.jumpCount)) * 0.5
                man.jumpCount -= 1

            else:
                man.isJump = False
                man.jumpCount = 10
        redrawGameWindow(win, bg, man, goblin)
    pygame.quit()


if __name__ == "__main__":
    main()
