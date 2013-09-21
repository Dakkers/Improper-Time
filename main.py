import pyglet as pyg
from pyglet.window import key
import pymunk as pym
from pymunk.pyglet_util import draw as pdraw
import resources, player, drawable
"""
class TimeEvolve(drawable.Drawable):
	def __init__(self, initback):
		self.bg = pyg.sprite.Sprite(pyg.resource.image(initback))
		self.posx, self.posy = self.bg.position

	def triggered(self, newback):
		self.bg = pyg.sprite.Sprite(pyg.resource.image(newback))"""

window = pyg.window.Window(800,400)
space = pym.Space()
space.gravity = 0, -1000					#looks more real than -9.8 or -10
space.collision_slop = 0.0000001			#reduce penetration
space.collision_bias = pow(1.0-0.4, 120)	#determine speed of overlap - reduce penetration
space.iterations = 8 						#reduce penetration (haha penetration)
floor = pym.Segment(space.static_body, (0,10), (5000,10), 14)
floor.friction = 1.0
floor.group = 1 		#objects of the same (non-zero) group do not collide!
floor.restituion = 0.0 	#reduce bounciness
space.add(floor)

drawable_batch = pyg.graphics.Batch()
char = player.Player(space=space, batch=drawable_batch)

bg = drawable.Drawable('ColonialForest.png')
bg.add_child(char)
drawEngine = False
xoffset = 0.0
ww, wh = window.width, window.height
bgw, bgh = bg.width, bg.height


@window.event
def on_draw():
	global drawEngine
	global xoffset
	window.clear()
	pyg.gl.glPushMatrix()
	pyg.gl.glTranslatef(xoffset, 0, 0)	#shift graphics by amount xoffset - like a camera moving
	bg.offsetdraw(0,0)
	if drawEngine:
		pdraw(space)
	drawable_batch.draw()
	pyg.gl.glPopMatrix()

@window.event
def on_key_press(symbol, modifiers):
	global drawEngine
	if symbol == key.E:
		drawEngine = not drawEngine


def update(dt):
	global xoffset
	space.step(dt)
	char.update(dt)

	if char.x + xoffset > 600:		#when char gets to right side of screen, scroll right by using glTranslatef(xoffset)
		xoffset = 600 - char.x
	if char.x + xoffset < 200:		#when char gets to left side...
		xoffset = 200 - char.x
	if xoffset > 0:					#when char gets to left side of entire background, stop scrolling
		xoffset = 0
	if xoffset < (-bgw+ww):			#when char gets to right side of entire...
		xoffset = -bgw + ww


	

window.push_handlers(char)
window.push_handlers(char.key_handler)
pyg.clock.schedule_interval(update, 1/60.0)

if __name__ == '__main__':
	pyg.app.run()