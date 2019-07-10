from RagnarokEngine3 import RE3
from os.path import join

engine = RE3.Ragnarok(RE3.Vector2(640, 480), "RAGNAROK TUTORIAL 1")

world = engine.get_world()

world.clear_color = (255, 255, 255)

#end of tutorial 1

sprite = RE3.Sprite()

sprite.update_order = 0
sprite.draw_order = 0

sprite.load_texture("Ragnarok.jpg")

world.add_obj(sprite)

engine.run()

#end of tutorial 2
