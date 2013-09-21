import pyglet as pyg
from pyglet.window import key
import pymunk as pym

window = pyg.window.Window(800,400)



@window.event
def on_draw():
	window.clear()


if __name__ == '__main__':
	pyg.app.run()