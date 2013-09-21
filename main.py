import pyglet as pyg
from pyglet.window import key
import pymunk as pym
from pymunk.pyglet_util import draw as pdraw
import resources

window = pyg.window.Window(800,400)
space = pym.Space()

floor = pym.Segment(space.static_body, (0,10), (500,10), 5)
space.add(floor)


mario = pyg.resource.image('mario.png')
bg = pyg.sprite.Sprite(mario)

#Sprite has height and width attributes - use that for scrolling



@window.event
def on_draw():
	window.clear()
	bg.draw()
	pdraw(space)

def update(dt):
	#print 'derp'
	space.step(dt)

pyg.clock.schedule_interval(update, 1/30.0)

if __name__ == '__main__':
	pyg.app.run()