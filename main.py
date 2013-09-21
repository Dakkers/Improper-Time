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

floor = pym.Segment(space.static_body, (0,10), (500,10), 5)
space.add(floor)

drawable_batch = pyg.graphics.Batch()
char = player.Player(space=space, batch=drawable_batch, x=10, y=50)

#mario = pyg.resource.image('mario.png')
#bg = pyg.sprite.Sprite(mario)
initback = TimeEvolve('mario.png')
bg = initback.bg
#Sprite has height and width attributes - use that for scrolling

@window.event
def on_draw():
	window.clear()
	bg.draw()
	drawable_batch.draw()
	pdraw(space)

def update(dt):
	#print 'derp'
	space.step(dt)
	char.update(dt)
	

window.push_handlers(char)
window.push_handlers(char.key_handler)
pyg.clock.schedule_interval(update, 1/60.0)

if __name__ == '__main__':
	pyg.app.run()