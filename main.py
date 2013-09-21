import pyglet as pyg
from pyglet.window import key
import pymunk as pym
from pymunk.pyglet_util import draw as pdraw
import resources, player, drawable

class TimeEvolve():
	def __init__(self, initback):
		self.bg = pyg.sprite.Sprite(pyg.resource.image(initback))

	def triggered(self, newback):
		self.bg = pyg.sprite.Sprite(pyg.resource.image(newback))

window = pyg.window.Window(800,400)
space = pym.Space()
space.gravity = 0, -1000	#looks more real than -9.8 or -10
floor = pym.Segment(space.static_body, (0,10), (500,10), 14)
floor.friction = 1.0
floor.group = 1 		#objects of the same (non-zero) group do not collide!
floor.restituion = 0.0 	#reduce bounciness
space.add(floor)

drawable_batch = pyg.graphics.Batch()
char = player.Player(space=space, batch=drawable_batch)

#mario = pyg.resource.image('mario.png')
#bg = pyg.sprite.Sprite(mario)
initback = TimeEvolve('mario.png')
bg = initback.bg
#Sprite has height and width attributes - use that for scrolling
drawEngine = False

@window.event
def on_draw():
	global drawEngine
	window.clear()
	#pyg.gl.glPushMatrix()
	bg.draw()
	drawable_batch.draw()
	if drawEngine:
		pdraw(space)
	#pyg.gl.glPopMatrix()

@window.event
def on_key_press(symbol, modifiers):
	global drawEngine
	if symbol == key.E:
		drawEngine = not drawEngine


def update(dt):
	#print 'derp'
	space.step(dt)
	char.update(dt)
	

window.push_handlers(char)
window.push_handlers(char.key_handler)
pyg.clock.schedule_interval(update, 1/60.0)

if __name__ == '__main__':
	pyg.app.run()