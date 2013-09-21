import pyglet, drawable, pymunk
from pyglet.window import key
from pymunk.vec2d import Vec2d

PLAYER_VELOCITY = 200.0
JUMP_VELOCITY = 500.0
JUMP_CUTOFF_VELOCITY = 100

class Player(drawable.Drawable):

	body = pymunk.Body(5, pymunk.inf)
	body.position = 100,100
	head = pymunk.Circle(body, 10, (0,5))
	head2 = pymunk.Circle(body, 10, (0,13))
	feet = pymunk.Circle(body, 10, (0,-5))
	feet.friction = 1.0
	feet.restitution, head.restitution, head2.restitution = 0.0, 0.0, 0.0
	body.restitution = 0.0
	body.penetration = 0.001

	target_vx = 0.0
	remaining_jumps = 2
	well_grounded = False

	grounding = {
					'normal' : Vec2d.zero(),
					'penetration' : Vec2d.zero(),
					'impulse' : Vec2d.zero(),
					'position' : Vec2d.zero(),
					'body' : None
					}

	def __init__(self, space, *args, **kwargs):
		super(Player,self).__init__(image_name='nonmovingR.png',*args, **kwargs)

		space.add(self.body, self.head, self.head2, self.feet)
		self.feet.surface_velocity = (0,0)

		self.key_handler = key.KeyStateHandler()
		self.sprite_nonmoving = pyglet.image.load('nonmoving.png')
		self.sprite_right = pyglet.image.load('nonmovingR.png')
		self.sprite_mvright0 = pyglet.image.load('movingright0.png')
		self.sprite_mvright1 = pyglet.image.load('movingright1.png')
		self.sprite_left = pyglet.image.load('nonmovingL.png')
		self.sprite_mvleft0 = pyglet.image.load('movingleft0.png')
		self.sprite_mvleft1 = pyglet.image.load('movingleft1.png')

		self.anim_right = pyglet.image.Animation.from_image_sequence([self.sprite_mvright0, 
			self.sprite_mvright1], 0.5, True)
		self.anim_left = pyglet.image.Animation.from_image_sequence([self.sprite_mvleft0, 
			self.sprite_mvleft1], 0.5, True)


	def move_right(self, flag):
		if flag:
			self.image = self.anim_right
		else:
			self.image = self.sprite_right


	def move_left(self, flag):
		if flag:
			self.image = self.anim_left
		else:
			self.image = self.sprite_left

	def f(self, arbiter):
		n = -arbiter.contacts[0].normal
		if n.y > self.grounding['normal'].y:
			self.grounding['normal'] = n
			self.grounding['penetration'] = -arbiter.contacts[0].distance
			self.grounding['body'] = arbiter.shapes[1].body
			self.grounding['impulse'] = arbiter.total_impulse
			self.grounding['position'] = arbiter.contacts[0].position

	def update(self, dt):
		"""grounding = {
											'normal' : Vec2d.zero(),
											'penetration' : Vec2d.zero(),
											'impulse' : Vec2d.zero(),
											'position' : Vec2d.zero(),
											'body' : None
											}"""
		# find out if player is standing on ground
		
		self.grounding['normal'] = Vec2d.zero()
		self.grounding['penetration'] = Vec2d.zero()
		self.grounding['impulse'] = Vec2d.zero()
		self.grounding['position'] = Vec2d.zero()
		self.grounding['body'] = None

		self.body.each_arbiter(self.f)
			
		self.well_grounded = False
		if self.grounding['body'] != None and abs(Vec2d.dot(self.grounding['normal'], (0,1))) > 0.9:
			self.well_grounded = True
			self.remaining_jumps = 2


		if self.key_handler[key.LEFT]:
			self.target_vx = -PLAYER_VELOCITY

		if self.key_handler[key.RIGHT]:
			self.target_vx = PLAYER_VELOCITY

		self.feet.surface_velocity = self.target_vx, 0
		"""Okay, so phuc. Why does this change the velocity of the player, if 
		Circle.surface_velocity is used when calculating friction? Fuck. It just
		gives the god damn object a velocity upon contact.
		http://4-akamai.tapcdn.com/images/thumbs/taps/2012/12/deal-with-it-1-c13c59de-original.gif"""

		self.posx = self.body.position.x
		self.posy = self.body.position.y



	def on_key_press(self, symbol, modifiers):
		if symbol == key.RIGHT:
			self.target_vx = PLAYER_VELOCITY

			if self.key_handler[key.LEFT]:      #when LEFT is being held down and RIGHT is hit
				self.move_left(False)
			else:								#if only RIGHT is hit
				self.move_right(True)


		if symbol == key.LEFT:
			self.target_vx = -PLAYER_VELOCITY

			if self.key_handler[key.RIGHT]:     #when RIGHT is being held down and LEFT is hit
				self.move_right(False)
			else:								#if only LEFT is hit
				self.move_left(True)


		if symbol == key.UP:

			if self.well_grounded or self.remaining_jumps > 0:                    
					self.body.velocity.y = JUMP_VELOCITY    # + ground_velocity
					self.remaining_jumps -=1
					print("jump keypress")



	def on_key_release(self, symbol, modifiers):
		if symbol == key.RIGHT:

			if self.key_handler[key.LEFT]:		#when both are held down and RIGHT is released
				self.move_left(True)
				self.target_vx = -PLAYER_VELOCITY
			else:								#if only RIGHT is being held down and released
				self.move_right(False)
				self.target_vx = 0


		if symbol == key.LEFT:

			if self.key_handler[key.RIGHT]:		#when both are held down and LEFT is released
				self.move_right(True)
				self.target_vx = PLAYER_VELOCITY
			else:								#if only LEFT is being held down and released
				self.move_left(False)
				self.target_vx = 0


		if symbol == key.UP:
			self.body.velocity.y = min(self.body.velocity.y, JUMP_CUTOFF_VELOCITY)
			print("jump keyreleases")