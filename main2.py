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
		self.bg = pyg.sprite.Sprite(pyg.resource.image(newback))
"""

window = pyg.window.Window(800,400)
space  = pym.Space()

space.gravity        = 0, -1000			 #looks more real than -9.8 or -10
space.collision_slop = 0.0000001		 #reduce penetration
space.collision_bias = pow(1.0-0.4, 120) #determine speed of overlap - reduce penetration
space.iterations     = 8 				 #reduce penetration (haha penetration)

floor = pym.Segment(space.static_body, (-1000,10), (5000,10), 14)
floor.friction   = 1.0
floor.group      = 1 	#objects of the same (non-zero) group do not collide!
floor.restituion = 0.0 	#reduce bounciness
space.add(floor)

drawable_batch = pyg.graphics.Batch()
char = player.Player(space=space, batch=drawable_batch)

bg = [drawable.Drawable('backgrounds/labback.png'),
	  drawable.Drawable('backgrounds/pastforestback.png')]
fg = [drawable.Drawable('backgrounds/labfront.png'),
	  drawable.Drawable('backgrounds/pastforestfront.png')]

active_bg_id = 0
active_fg_id = 0

# activebg = drawable.Drawable('backgrounds/labback.png')
# activefg = pyg.sprite.Sprite(pyg.image.load('resources/backgrounds/labfront.png'), x=0, y=0)
# activebg.id = 0

# forest_past_bg = pyg.image.load('resources/backgrounds/pastforestback.png')
# forest_past_fg = pyg.image.load('resources/backgrounds/pastforestfront.png')

# lab_bg = pyg.image.load('resources/backgrounds/labback.png')
# lab_fg = pyg.image.load('resources/backgrounds/labfront.png')

# activebg.add_child(char)
bg[active_bg_id].add_child(char)
drawEngine = False
xoffset = 0.0

ww,  wh  = window.width, window.height
bgw, bgh = bg[active_bg_id].width, bg[active_bg_id].height

@window.event
def on_draw():
	global drawEngine
	global xoffset
	
	window.clear()
	
	# activebg.offsetdraw(0,0)
	# bg[active_bg_id].offsetdraw(0,0)
	bg[active_bg_id].offsetdraw(0,0)

	if drawEngine:
		pdraw(space)
	
	drawable_batch.draw()
	# activefg.draw()
	fg[active_fg_id].draw()

@window.event
def on_key_press(symbol, modifiers):
	global drawEngine

	if symbol == key.E:
		drawEngine = not drawEngine

def update(dt):
	global window
	global xoffset
	global bgw
	global ww
	global active_bg_id
	global active_fg_id
	
	space.step(dt)
	char.update(dt)

	if char.posx + xoffset > 600 :		#when char gets to right side of screen, scroll right by using glTranslatef(xoffset)
		xoffset = 600 - char.posx
	elif char.posx + xoffset < 200:		#when char gets to left side...
		xoffset = 200 - char.posx

	if xoffset > 0:
		# If the character gets to left side of entire background, stop scrolling.
		xoffset = 0
	elif xoffset < (-bgw+ww):
		# Else when character gets to right side of the entire background, stop scrolling as well.
		xoffset = -(ww - bgw)

	if (char.posx < 0) and (active_bg_id == 0):
		char.posx = 0
	elif (char.posx > bg[active_bg_id].width) and (active_bg_id == len(bg)):
		char.posx = bg[active_bg_id].width
	elif char.posx < 0:
		# Character has reached extreme left of screen, move to previous screen.
		bg[active_bg_id].remove_child(char)
		active_bg_id = active_bg_id - 1
		active_fg_id = active_fg_id - 1
		bg[active_bg_id].add_child(char)
		bgw, bgh = bg[active_bg_id].width, bg[active_bg_id].height
		char.posx = bg[active_bg_id].width
		xoffset = -(ww - bgw)

	elif char.posx > bg[active_bg_id].width:
		# Character has reached extreme right of screen, move to next screen.
		bg[active_bg_id].remove_child(char)
		active_bg_id = active_bg_id + 1
		active_fg_id = active_fg_id + 1
		pyg.gl.glLoadIdentity()	
		bg[active_bg_id].add_child(char)
		bgw, bgh  = bg[active_bg_id].width, bg[active_bg_id].height
		char.posx = 0
		xoffset   = 0

	# if char.posx < -30:
	# 	activebg.image = forest_past_bg
	# 	activebg.id = 1
	# 	bgw,bgh = activebg.width, activebg.height
	# 	char.posx = char.posx + bgw

	# if char.posx > 4490:
	# 	activebg.image = lab_bg
	# 	bgw,bgh = activebg.width, activebg.height
	# 	char.posx = char.posx - bgw

	print char.posx

window.push_handlers(char)
window.push_handlers(char.key_handler)
pyg.clock.schedule_interval(update, 1/100.0)

if __name__ == '__main__':
	pyg.app.run()