import pyglet as pyg
from pyglet.window import key
import pymunk as pym
from pymunk.pyglet_util import draw as pdraw
import resources, player, drawable

def floorfunc(a,b,w,fric,rest):
	f = pym.Segment(space.static_body, a, b, w)
	f.friction, f.restitution = fric, rest 	#reduce friction and bounciness
	f.group = 1 #objects of the same (non-zero) group do not collide
	return f

def switchbg(bg,fg,ID,XOFF,CHARX,portalbool):
	global activebg
	global activefg
	global char
	activebg.remove_child(char)
	activebg.image = bg
	activefg.image = fg
	activebg.id = ID
	bgw,bgh = activebg.width, activebg.height
	activebg.add_child(char)
	xoffset = XOFF
	char.body.position.x  = CHARX
	drawportal = portalbool

window = pyg.window.Window(800,400)
space = pym.Space()
space.gravity = 0, -1000					#looks more real than -9.8 or -10
space.collision_slop = 0.0000001			#reduce penetration
space.collision_bias = pow(1.0-0.4, 120)	#determine speed of overlap - reduce penetration
space.iterations = 8 						#reduce penetration (haha penetration)

labfloor = floorfunc((-1000,35), (1340,35), 14, 1.0, 0.0)
labwall = pym.Segment(space.static_body, (-35,-50), (-35, 1000), 20)
forestfloor = floorfunc((0,35), (5000,35), 14, 1.0, 0.0)
forestwall = pym.Segment(space.static_body, (4540,-50), (4540, 1000), 20)
space.add(labfloor, labwall, forestfloor, forestwall)

drawable_batch = pyg.graphics.Batch()
npc_batch = pyg.graphics.Batch()
char = player.Player(space=space, batch=drawable_batch)

activebg = drawable.Drawable('backgrounds/lab_bg.png')
activefg = pyg.sprite.Sprite(pyg.image.load('resources/backgrounds/lab_fg.png'), x=0, y=0)
activebg.id = 0
forest_bg = pyg.image.load('resources/backgrounds/forest_bg.png')
forest_fg = pyg.image.load('resources/backgrounds/forest_fg.png')
lab_bg = pyg.image.load('resources/backgrounds/lab_bg.png')
lab_fg = pyg.image.load('resources/backgrounds/lab_fg.png')
city_bg = pyg.image.load('resources/backgrounds/city_bg.png')
city_fg = pyg.image.load('resources/backgrounds/city_fg.png')
portal = pyg.sprite.Sprite(pyg.image.load('resources/portal-01.png'))
activebg.add_child(char)

drawEngine = False	#initially do not show hitboxes/floors
xoffset = 0.0
ww, wh = window.width, window.height
bgw, bgh = activebg.width, activebg.height
drawportal = False	#do not draw the portal immediately
timetravel = False


@window.event
def on_draw():
	global drawEngine
	global xoffset
	global drawportal
	window.clear()
	pyg.gl.glPushMatrix()
	pyg.gl.glTranslatef(xoffset, 0, 0)	#shift graphics by amount xoffset - like a camera moving
	activebg.offsetdraw(0,0)
	drawable_batch.draw()
	activefg.draw()
	if drawportal:
		portal.set_position(1970,58)
		portal.draw()
	if drawEngine:
		pdraw(space)

	pyg.gl.glPopMatrix()


@window.event
def on_key_press(symbol, modifiers):
	global drawEngine
	global timetravel
	if symbol == key.E:
		drawEngine = not drawEngine

	if symbol == key.UP and drawportal and (char.x < (portal.x + portal.width/2.0) and char.x > (portal.x - portal.width/2.0)):
		timetravel = not timetravel
		if timetravel:
			activebg.image = forest_bg
			activefg.image = forest_fg
			activebg.id = 3
		else:
			activebg.image = city_bg
			activefg.image = city_fg
			activebg.id = 1


def update(dt):
	global activebg
	global xoffset
	global bgw
	global ww
	global drawportal
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

	if timetravel:
		if char.posx < -15 and activebg.id == 3:
			activebg.remove_child(char)
			activebg.image = lab_bg
			activefg.image = lab_fg
			activebg.id = 0
			bgw,bgh = activebg.width, activebg.height
			activebg.add_child(char)
			xoffset = ww - bgw
			char.body.position.x  = char.posx + bgw
			drawportal = False

		if char.posx > 1315 and activebg.id == 2:
			activebg.remove_child(char)
			activebg.image = forest_bg
			activefg.image = forest_fg
			activebg.id = 1
			bgw,bgh = activebg.width, activebg.height
			activebg.add_child(char)
			xoffset = 0
			char.body.position.x = 0
			drawportal = True


	else:
		if char.posx < -15 and activebg.id == 1:

			activebg.remove_child(char)
			activebg.image = lab_bg
			activefg.image = lab_fg
			activebg.id = 0
			bgw,bgh = activebg.width, activebg.height
			activebg.add_child(char)
			xoffset = ww - bgw
			char.body.position.x  = char.posx + bgw
			drawportal = False
		

		if char.posx > 1315 and activebg.id == 0:
			activebg.remove_child(char)
			activebg.image = city_bg
			activefg.image = city_fg
			activebg.id = 1
			bgw,bgh = activebg.width, activebg.height
			activebg.add_child(char)
			xoffset = 0
			char.body.position.x = 0
			drawportal = True

	print char.x

"""
switchbg(lab_bg, lab_fg, 2, ww - bgw, char.posx + bgw, False)
switchbg(forest_bg, forest_fg, 3, 0, 0, True)
switchbg(lab_bg, lab_fg, 0, ww - bgw, char.posx + bgw, False)
switchbg(city_bg, city_fg, 1, 0, 0, True)
"""


window.push_handlers(char)
window.push_handlers(char.key_handler)
pyg.clock.schedule_interval(update, 1/100.0)

if __name__ == '__main__':
	pyg.app.run()