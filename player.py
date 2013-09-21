import pyglet as pyg
import pymunk as pym
from pyglet.window import key
from pymunk.vec2d import Vec2d
import resources, drawable

PLAYER_VELOCITY = 100.0

class Player(drawable.Drawable):

	body = pym.Body(5, pym.inf)
	body.position = 100,100
	head = pym.Circle(body, 10, (0,5))
	head2 = pym.Circle(body, 10, (0,13))
	feet = pym.Circle(body, 10, (0,-5))
	feet.friction = 1.0
	feet.restitution, head.restitution, head2.restitution = 0.0, 0.0, 0.0
	body.restitution = 0.0
	body.penetration = 0.001

	target_vx = 0.0
	remaining_jumps = 2
	well_grounded = False

	key_handler = key.KeyStateHandler()
	#sprite_nonmoving = pyg.resource.image('stationary.png')
	sprite_right = pyg.resource.image('char1.png')
	#sprite_mvright0 = pyg.resource.image('movingright0.png')
	#sprite_mvright1 = pyg.resource.image('movingright1.png')
	sprite_left = pyg.resource.image('char2.png')
	#sprite_mvleft0 = pyg.resource.image('movingleft0.png')
	#sprite_mvleft1 = pyg.resource.image('movingleft1.png')

	grounding = {
					'normal' : Vec2d.zero(),
					'penetration' : Vec2d.zero(),
					'impulse' : Vec2d.zero(),
					'position' : Vec2d.zero(),
					'body' : None
					}

	def __init__(self, space, *args, **kwargs):
		super(Player,self).__init__(image_name='char1.png',*args, **kwargs)
		#Name non-moving stationary

		space.add(self.body, self.head, self.head2, self.feet)
		self.feet.surface_velocity = (0,0)





	def on_key_press(symbol, modifiers):
		if symbol == key.RIGHT:
			self.image = pyg.sprite.Sprite(sprite_right)

		if symbol == key.LEFT:
			self.image = pyg.sprite.Sprite(sprite_left)

	"""self.animate_right = pyg.image.Animation.from_image_sequence([self.sprite_mvright0, 
			self.sprite_mvright1], 0.5, True)
		self.anim_left = pyg.image.Animation.from_image_sequence([self.sprite_mvleft0, 
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
			self.image = self.sprite_left"""