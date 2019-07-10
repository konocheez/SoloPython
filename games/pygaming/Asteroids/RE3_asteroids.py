from RagnarokEngine3 import RE3 as R
import math
from random import randint, randrange
import pygame as pg

"""Open with RE3.py and tuto3.py for reference"""

class Ship(R.DrawableObj):
    def __init__(self, draw_order, update_order, speed = 5):
        """Creates a ship that's able to rotate, propel, and shoot"""

        super(Ship, self).__init__(draw_order, update_order)
        self.ship = R.Sprite()
        # Sprite is anything that moves around the screen therefore asteroids are sprites

        self.ship.load_texture("ship1.png")

        self.ship.coords = R.Ragnarok.get_world().get_backbuffer_size() / 2.0

        self.ship.angle = math.pi / 2
        self.ship.speed = speed

    def update(self, milliseconds):
        self.rotation_val = math.pi / 50
        self.ship.trajectory = R.Vector2(math.cos(self.ship.angle), math.sin(self.ship.angle))

        if R.Ragnarok.get_world().Keyboard.is_down(pg.K_LEFT):
            self.ship.angle -= self.rotation_val
            self.ship.rotation += math.degrees(self.rotation_val)

        if R.Ragnarok.get_world().Keyboard.is_down(pg.K_RIGHT):
            self.ship.angle += self.rotation_val
            self.ship.rotation -= math.degrees(self.rotation_val)

        if R.Ragnarok.get_world().Keyboard.is_down(pg.K_UP):
            self.ship.coords = self.ship.coords - (self.ship.speed * self.ship.trajectory)

        if R.Ragnarok.get_world().Keyboard.is_down(pg.K_DOWN):
            self.ship.coords = self.ship.coords + (self.ship.speed * self.ship.trajectory)

        # if R.Ragnarok.get_world().Keyboard.is_down(pg.K_SPACE):
        self.ship.update(milliseconds)

    def draw(self, milliseconds, surface):
        self.ship.draw(milliseconds, surface)
        super(Ship, self).draw(milliseconds, surface)

# class Asteroid(R.DrawableObj):
#     """Creates asteroids for the user to combat"""
#
#     def __init__(self, draw_order, update_order, slow = 2, med = 5, fast = 8):
#         super(Asteroid, self).__init__(draw_order, update_order)
#
#         self.asteroid = R.Sprite()
#         self.asteroid.load_texture('big_asteroid.png')
#         self.asteroid.coords = R.Ragnarok.get_world().get_backbuffer_size()
#         self.asteroid.angle = randrange(0, 2*math.pi)
#         self.asteroid.speed = randrange(slow, fast)
#
#     def __generate_location(self):
#         """Reset asteroid position once it leaves screen"""
#
#         screen_width = world.get_backbuffer_size().X
#         self.asteroid.coords = R.Vector2(screen_width + self.image.get_width(), randrange(0, world.get_backbuffer_size().Y))
#
#     def update(self, milliseconds):
#         self.asteroid.trajectory = R.Vector2(math.cos(self.asteroid.angle), math.sin(self.ship.angle))
#         self.asteroid.coords = self.asteroid.coords + (self.asteroid.speed + self.asteroid.trajectory)
#         self.asteroid.update(milliseconds)
#
#     def draw(self, milliseconds, surface):
#         self.asteroid.draw(milliseconds, surface)
#         super(Asteroid, self).draw(milliseconds, surface)

class ExitManager(R.UpdatableObj):
    """
    In this case, allows the Esc button to exit the game.
    """

    def update(self, milliseconds):
        if R.Ragnarok.get_world().Keyboard.is_clicked(pg.K_ESCAPE):
            engine.exit()


def main():
    num = 0
    engine = R.Ragnarok(R.Vector2(800, 600), "Ass-Steroids")

    world = engine.get_world()
    world.clear_color = (0, 0, 0)

    space = R.Sprite()
    space.load_texture("stars.jpg")
    space.scale_to(world.get_backbuffer_size())

    ship = Ship(1, 1)
    asteroids = []

    # while num < 10:
    #     asteroids.append(Asteroid(2, 2))
    #     num += 1
    #     if num == 10:
    #         num = 0


    exitManager = ExitManager()

    world.add_obj(space)
    world.add_obj(ship)
    world.add_obj(exitManager)

    engine.run()

if __name__ == "__main__":
    main()
