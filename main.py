import pyglet as pyg
from pyglet.window import key
import pymunk as pym
from pymunk.pyglet_util import draw as pdraw
import resources, player, drawable, npc

count = 0
flag_glob = 0

"""
class TimeEvolve(drawable.Drawable):
	def __init__(self, initback):
		self.bg = pyg.sprite.Sprite(pyg.resource.image(initback))
		self.posx, self.posy = self.bg.position

	def triggered(self, newback):
		self.bg = pyg.sprite.Sprite(pyg.resource.image(newback))"""

window = pyg.window.Window(800,400)
space = pym.Space()
#space1 = pym.Space()
space.gravity = 0, -1000					#looks more real than -9.8 or -10
space.collision_slop = 0.0000001			#reduce penetration
space.collision_bias = pow(1.0-0.4, 120)	#determine speed of overlap - reduce penetration
space.iterations = 8 						#reduce penetration (haha penetration)
floor = pym.Segment(space.static_body, (-1000,10), (5000,10), 14)
floor.friction = 1.0
floor.group = 1 		#objects of the same (non-zero) group do not collide!
floor.restituion = 0.0 	#reduce bounciness
space.add(floor)

drawable_batch = pyg.graphics.Batch()
npc_batch = pyg.graphics.Batch()
char = player.Player(space=space, batch=drawable_batch)
npc_char = npc.NPC(space=space, batch=npc_batch)

bg = drawable.Drawable('Backgrounds/back.png')
fg = pyg.sprite.Sprite(pyg.image.load('resources/Backgrounds/front.png'), x=0, y=0)

forest_bg = pyg.image.load('resources/Backgrounds/back.png')
lab_bg = pyg.image.load('resources/bg-02.png')
bg.add_child(char)
bg.add_child(npc_char)
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
	npc_batch.draw()
	fg.draw()
	pyg.gl.glPopMatrix()

@window.event
def on_key_press(symbol, modifiers):
	global drawEngine
	if symbol == key.E:
		drawEngine = not drawEngine


def update(dt):
	global count
	global flag_glob
	count += 1
	global xoffset
	space.step(dt)
	#space1.step(dt)
	char.update(dt)
	#npc.update(dt)
	if count % 10 == 0:
		flag_glob = 1
	elif count % 5 == 0:
		flag_glob = 0
	npc_char.update(flag_glob, dt)


	if char.posx + xoffset > 600:		#when char gets to right side of screen, scroll right by using glTranslatef(xoffset)
		xoffset = 600 - char.posx
	elif char.posx + xoffset < 200:		#when char gets to left side...
		xoffset = 200 - char.posx
	if xoffset > 0:						#when char gets to left side of entire background, stop scrolling
		xoffset = 0
	elif xoffset < (-bgw+ww):			#when char gets to right side of entire...
		xoffset = -bgw + ww

	print char.posx

"""
	if char.posx < -20:
		bg.image = lab_bg
		char.posx = char.posx + 810
	"""

	 


	

window.push_handlers(char)
window.push_handlers(char.key_handler)
pyg.clock.schedule_interval(update, 1/120.0)

if __name__ == '__main__':
	pyg.app.run()