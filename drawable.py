import pyglet

class Drawable(pyglet.sprite.Sprite):

	def __init__(self, image_name, *args, **kwargs):
		super(Drawable,self).__init__(img=pyglet.resource.image(image_name), *args, **kwargs)
		self.children = []
		self.posx = 0.0
		self.posy = 0.0
		self.id = None

	def offsetdraw(self, x0, y0):
		self.set_position(x0 + self.posx, y0 + self.posy)
		self.draw()

		for child in self.children:
			child.offsetdraw(x0 + self.posx, y0 + self.posy)

	def add_child(self, child):
		if child not in self.children:
			self.children.append(child)

	def remove_child(self, child):
		if child in self.children:
			self.children.remove(child)