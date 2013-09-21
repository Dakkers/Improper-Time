import pyglet as pyg
import drawable as drw
import pymunk as pym
from pyg.window import key
from pym.vec2d import Vec2d

#Using same constants as your initial file
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
		super(Player,self).__init__(image_name='stationary.png',*args, **kwargs)
		#Name non-moving stationary

		space.add(self.body, self.head, self.head2, self.feet)
		self.feet.surface_velocity = (0,0)

		self.key_handler = key.KeyStateHandler()
		self.sprite_nonmoving = pyglet.image.load('stationary.png')
		self.sprite_right = pyglet.image.load('nonmovingR.png')
		self.sprite_mvright0 = pyglet.image.load('movingright0.png')
		self.sprite_mvright1 = pyglet.image.load('movingright1.png')
		self.sprite_left = pyglet.image.load('nonmovingL.png')
		self.sprite_mvleft0 = pyglet.image.load('movingleft0.png')
		self.sprite_mvleft1 = pyglet.image.load('movingleft1.png')

		self.animate_right = pyglet.image.Animation.from_image_sequence([self.sprite_mvright0, 
			self.sprite_mvright1], 0.5, True)
		self.anim_left = pyglet.image.Animation.from_image_sequence([self.sprite_mvleft0, 
			self.sprite_mvleft1], 0.5, True)
		