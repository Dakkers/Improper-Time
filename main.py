import pyglet as pyg
from pyglet.window import key
import pymunk as pym
import resources

window = pyg.window.Window(800,400)

mario = pyg.resource.image('mario.png')
bg = pyg.sprite.Sprite(mario)



@window.event
def on_draw():
	window.clear()
	bg.draw()


if __name__ == '__main__':
	pyg.app.run()