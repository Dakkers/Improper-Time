import pyglet as pyg
from pyglet.window import key
import pymunk as pym
from pymunk.pyglet_util import draw as pdraw
import resources, player, drawable



window = pyg.window.Window(800,400)
space = pym.Space()
space.gravity = 0, -1000					#looks more real than -9.8 or -10
space.collision_slop = 0.0000001			#reduce penetration
space.collision_bias = pow(1.0-0.4, 120)	#determine speed of overlap - reduce penetration
space.iterations = 8 						#reduce penetration (haha penetration)
floor = pym.Segment(space.static_body, (-1000,10), (5000,10), 14)
floor.friction = 1.0
floor.group = 1 		#objects of the same (non-zero) group do not collide!
floor.restituion = 0.0 	#reduce bounciness
labwall = pym.Segment(space.static_body, (-35,-50), (-35, 1000), 20)
forestwall = pym.Segment(space.static_body, (4540,-50), (4540, 1000), 20)
space.add(floor, labwall, forestwall)

drawable_batch = pyg.graphics.Batch()
npc_batch = pyg.graphics.Batch()
char = player.Player(space=space, batch=drawable_batch)

activebg = drawable.Drawable('backgrounds/lab_now_bg.png')
activefg = pyg.sprite.Sprite(pyg.image.load('resources/backgrounds/lab_now_fg.png'), x=0, y=0)
activebg.id = 0
forest_past_bg = pyg.image.load('resources/backgrounds/forest_past_bg.png')
forest_past_fg = pyg.image.load('resources/backgrounds/forest_past_fg.png')
lab_now_bg = pyg.image.load('resources/backgrounds/lab_now_bg.png')
lab_now_fg = pyg.image.load('resources/backgrounds/lab_now_fg.png')
portal = pyg.sprite.Sprite(pyg.image.load('resources/portal-01.png'))
activebg.add_child(char)

drawEngine = False	#initially do not show hitboxes/floors
xoffset = 0.0
ww, wh = window.width, window.height
bgw, bgh = activebg.width, activebg.height


@window.event
def on_draw():
	global drawEngine
	global xoffset
	window.clear()
	pyg.gl.glPushMatrix()
	pyg.gl.glTranslatef(xoffset, 0, 0)	#shift graphics by amount xoffset - like a camera moving
	activebg.offsetdraw(0,0)
	if drawEngine:
		pdraw(space)
	drawable_batch.draw()
	activefg.draw()
	pyg.gl.glPopMatrix()

@window.event
def on_key_press(symbol, modifiers):
	global drawEngine
	if symbol == key.E:
		drawEngine = not drawEngine


def update(dt):
	global activebg
	global xoffset
	global bgw
	global ww
	space.step(dt)
	char.update(dt)


	if char.posx + xoffset > 600:		#when char gets to right side of screen, scroll right by using glTranslatef(xoffset)
		xoffset = 600 - char.posx
	elif char.posx + xoffset < 200:		#when char gets to left side...
		xoffset = 200 - char.posx
	if xoffset > 0:						#when char gets to left side of entire background, stop scrolling
		xoffset = 0
	elif xoffset < (-bgw+ww):			#when char gets to right side of entire...
		xoffset = -bgw + ww

	
	if char.posx < -30:
		activebg.remove_child(char)
		activebg.image = lab_bg
		activefg.image = lab_fg
		activebg.id = 0
		bgw,bgh = activebg.width, activebg.height
		activebg.add_child(char)
		xoffset = ww - bgw
		char.body.position.x = char.posx + bgw
	

	if char.posx > 1315 and activebg.id == 0:
		activebg.remove_child(char)
		activebg.image = forest_past_bg
		activefg.image = forest_past_fg
		activebg.id = 1
		bgw,bgh = activebg.width, activebg.height
		activebg.add_child(char)
		xoffset = 0
		char.body.position.x = 0
	print char.posx


window.push_handlers(char)
window.push_handlers(char.key_handler)
pyg.clock.schedule_interval(update, 1/100.0)

if __name__ == '__main__':
	pyg.app.run()