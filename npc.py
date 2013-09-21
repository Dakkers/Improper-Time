import Drawable

class NPC(Drawable.Drawable):
	def __init__(self, image_name, *args, **kwargs):
		super(NPC.self).__init__(img=pyglet.resource.image(image_name), *args, **kwargs)
		self.children = []
		self.posx = 0.0
		self.posy = 0.0

    def walk():
        from random import randint
        fps = 60;
        while True:
            direction = random.randint(0,1)
            walk_duration  = random.randint(1*fps, 7*fps)
            wait_duration  = random.randint(1*fps, 10*fps)
            for i in xrange(walk_duration):
                if direction == 0:
                    yield -1 # move to the left
                else:
                    yield 1 # move to the right

            for i in xrange(wait_duration):
                yield 0 # wait

    # Inventory inventory()