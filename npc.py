import pyglet as pyg
import pymunk as pym
from pyglet.window import key
from pymunk.vec2d import Vec2d
import resources, drawable

NPC_VELOCITY = 375.0

class NPC(drawable.Drawable):
    """def __init__(self, image_name, *args, **kwargs):
		super(NPC.self).__init__(img=pyglet.resource.image(image_name), *args, **kwargs)
		self.children = []
		self.posx = 0.0
		self.posy = 0.0

    def walk():
        from random import randint
        fps = 60;
        while True:
            direction = random.randint(0,1)
            walk_duration  = random.randint(1*fps, 7*fps)
            wait_duration  = random.randint(1*fps, 10*fps)
            for i in xrange(walk_duration):
                if direction == 0:
                    yield -1 # move to the left
                else:
                    yield 1 # move to the right

            for i in xrange(wait_duration):
                yield 0 # wait

    # Inventory inventory()"""
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

    char_stationary_right = pyg.image.load('resources/charRight.png')
    char_stationary_left = pyg.image.load('resources/charLeft.png')
    char_moveleft1 = pyg.image.load('resources/charAnim/left01.png')
    char_moveleft2 = pyg.image.load('resources/charAnim/left02.png')
    char_moveleft3 = pyg.image.load('resources/charAnim/left03.png')
    char_moveleft4 = pyg.image.load('resources/charAnim/left04.png')
    char_moveleft5 = pyg.image.load('resources/charAnim/left05.png')
    char_moveleft6 = pyg.image.load('resources/charAnim/left06.png')
    char_moveleft7 = pyg.image.load('resources/charAnim/left07.png')
    char_moveleft8 = pyg.image.load('resources/charAnim/left08.png')
    char_moveleft9 = pyg.image.load('resources/charAnim/left09.png')
    char_moveright1 = pyg.image.load('resources/charAnim/right01.png')
    char_moveright2 = pyg.image.load('resources/charAnim/right02.png')
    char_moveright3 = pyg.image.load('resources/charAnim/right03.png')
    char_moveright4 = pyg.image.load('resources/charAnim/right04.png')
    char_moveright5 = pyg.image.load('resources/charAnim/right05.png')
    char_moveright6 = pyg.image.load('resources/charAnim/right06.png')
    char_moveright7 = pyg.image.load('resources/charAnim/right07.png')
    char_moveright8 = pyg.image.load('resources/charAnim/right08.png')
    char_moveright9 = pyg.image.load('resources/charAnim/right09.png')
    anim_left = pyg.image.Animation.from_image_sequence([char_moveleft1,
            char_moveleft2, char_moveleft3, char_moveleft4, char_moveleft5,
            char_moveleft6, char_moveleft7, char_moveleft8, char_moveleft9], 0.1, True)
    anim_right = pyg.image.Animation.from_image_sequence([char_moveright1,
            char_moveright2, char_moveright3, char_moveright4, char_moveright5,
            char_moveright6, char_moveright7, char_moveright8, char_moveright9], 0.1, True)

    grounding = {
                'normal' : Vec2d.zero(),
                'penetration' : Vec2d.zero(),
                'impulse' : Vec2d.zero(),
                'position' : Vec2d.zero(),
                'body' : None
                }

    def __init__(self, space, *args, **kwargs):
        super(NPC,self).__init__(image_name='charRight.png',*args, **kwargs)
        space.add(self.body, self.head, self.head2, self.feet)
        self.posx, self.posy = 150,150

    """def walk():
        from random import randint
        fps = 60;
        while True:
            direction = random.randint(0,1)
            walk_duration  = random.randint(1*fps, 7*fps)
            wait_duration  = random.randint(1*fps, 10*fps)
            for i in xrange(walk_duration):
                if direction == 0:
                    yield -1 # move to the left
                else:
                    yield 1 # move to the right"""

    """def move_right(self, flag):
        if flag:
            self.image = self.anim_right
            self.v_x = NPC_VELOCITY
        else:
            self.image = self.char_stationary_right
            self.v_x = 0"""


    def move(self, flag):
        if flag:
            self.image = self.anim_left
            self.v_x = -NPC_VELOCITY
        else:
            self.image = self.anim_right
            self.v_x = NPC_VELOCITY
        return self.v_x
        """else:
            self.image = self.char_stationary_left
            self.v_x = 0"""


    """def on_key_press(self, symbol, modifiers):

        if symbol == key.RIGHT:
            if self.key_handler[key.LEFT]:  #if LEFT is being held and RIGHT is hit
                self.move_left(False)
            else:                           #if only RIGHT is hit
                self.move_right(True)

        if symbol == key.LEFT:
            if self.key_handler[key.RIGHT]: #if RIGHT is being held and LEFT is hit
                self.move_right(False)
            else:                           #if only LEFT is hit
                self.move_left(True)


    def on_key_release(self, symbol, modifiers):

        if symbol == key.RIGHT:
            if self.key_handler[key.LEFT]:  #if BOTH are being held and RIGHT is released
                self.move_left(True)
            else:                           #if only RIGHT was being held and released
                self.move_right(False)

        if symbol == key.LEFT:
            if self.key_handler[key.RIGHT]: #if BOTH are being held and LEFT is released
                self.move_right(True)
            else:                           #if only LEFT was being held and released
                self.move_left(False)"""

    def update(self, flag, dt):
        self.v_x = npc.move(flag)
        self.feet.surface_velocity = self.v_x, 0
        self.posx, self.posy = self.body.position

#newnpc = NPC('resources/charLeft.png')