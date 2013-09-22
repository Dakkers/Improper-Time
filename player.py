import pyglet as pyg
import pymunk as pym
from pyglet.window import key
from pymunk.vec2d import Vec2d
import resources, drawable

PLAYER_VELOCITY = 600.0

class Player(drawable.Drawable):

	body = pym.Body(5, pym.inf)
	body.position = 100,100
	head = pym.Circle(body, 12, (17,95))
	head2 = pym.Circle(body, 9, (18,19))
	feet = pym.Circle(body, 9, (18,10))
	feet.friction = 1.0
	feet.restitution, head.restitution, head2.restitution = 0.0, 0.0, 0.0
	body.restitution = 0.0
	body.penetration = 0.001
	feet.surface_velocity = (0,0)

	v_x  = 0.0
	remaining_jumps = 2
	well_grounded = False

	key_handler = key.KeyStateHandler()
	char_stationary_right = pyg.image.load('resources/char/right.png')
	char_stationary_left = pyg.image.load('resources/char/left.png')
	char_moveleft1 = pyg.image.load('resources/char/leftwalk01.png')
	char_moveleft2 = pyg.image.load('resources/char/leftwalk02.png')
	char_moveleft3 = pyg.image.load('resources/char/leftwalk03.png')
	char_moveleft4 = pyg.image.load('resources/char/leftwalk04.png')
	char_moveleft5 = pyg.image.load('resources/char/leftwalk05.png')
	char_moveleft6 = pyg.image.load('resources/char/leftwalk06.png')
	char_turnleft = pyg.image.load('resources/char/leftturn.png')
	char_moveright1 = pyg.image.load('resources/char/rightwalk01.png')
	char_moveright2 = pyg.image.load('resources/char/rightwalk02.png')
	char_moveright3 = pyg.image.load('resources/char/rightwalk03.png')
	char_moveright4 = pyg.image.load('resources/char/rightwalk04.png')
	char_moveright5 = pyg.image.load('resources/char/rightwalk05.png')
	char_moveright6 = pyg.image.load('resources/char/rightwalk06.png')
	char_turnright = pyg.image.load('resources/char/rightturn.png')
	anim_walkleft = pyg.image.Animation.from_image_sequence([char_moveleft1,
			char_moveleft2, char_moveleft3, char_moveleft4, char_moveleft5,
			char_moveleft6], 0.1, True)
	anim_walkright = pyg.image.Animation.from_image_sequence([char_moveright1,
			char_moveright2, char_moveright3, char_moveright4, char_moveright5,
			char_moveright6], 0.1, True)

	grounding = {
				'normal' : Vec2d.zero(),
				'penetration' : Vec2d.zero(),
				'impulse' : Vec2d.zero(),
				'position' : Vec2d.zero(),
				'body' : None
				}

	def __init__(self, space, *args, **kwargs):
		super(Player,self).__init__(image_name='char/right.png',*args, **kwargs)
		space.add(self.body, self.head, self.head2, self.feet)
		self.posx, self.posy = 100,100


	def move_right(self, flag):
		if flag:
			self.image = self.anim_walkright
			self.v_x = PLAYER_VELOCITY
		else:
			self.image = self.char_stationary_right
			self.v_x = 0


	def move_left(self, flag):
		if flag:
			self.image = self.anim_walkleft
			self.v_x = -PLAYER_VELOCITY
		else:
			self.image = self.char_stationary_left
			self.v_x = 0


	def on_key_press(self, symbol, modifiers):

		if symbol == key.RIGHT:
			if self.key_handler[key.LEFT]:	#if LEFT is being held and RIGHT is hit
				self.move_left(False)
			else:							#if only RIGHT is hit
				self.move_right(True)

		if symbol == key.LEFT:
			if self.key_handler[key.RIGHT]:	#if RIGHT is being held and LEFT is hit
				self.move_right(False)
			else:							#if only LEFT is hit
				self.move_left(True)



	def on_key_release(self, symbol, modifiers):

		if symbol == key.RIGHT:
			if self.key_handler[key.LEFT]:	#if BOTH are being held and RIGHT is released
				self.move_left(True)
			else:							#if only RIGHT was being held and released
				self.move_right(False)

		if symbol == key.LEFT:
			if self.key_handler[key.RIGHT]:	#if BOTH are being held and LEFT is released
				self.move_right(True)
			else:							#if only LEFT was being held and released
				self.move_left(False)

	def update(self, dt):
		self.feet.surface_velocity = self.v_x, 0
		self.posx, self.posy = self.body.position