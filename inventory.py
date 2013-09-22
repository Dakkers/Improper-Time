import pyglet
import Icon

# An inventory consists of a list of length rows*cols and is always drawn with
# the top left corner at (x,y).
class Inventory:
    def __init__(self, rows, cols, x, y):
        self.I = []
        self.rows = rows
        self.cols = cols
        self.x    = x
        self.y    = y

    def addItem(self, item):
        if len(I) >= (rows*cols):
            print "Inventory is full! Cannot add " + item.name + "!"
        else:
            self.I.append(item)

    def removeItem(self, item):
        if item in self.I:
            self.I.remove(item)
        else:
            print item.name + " not found in inventory!"

    def draw():
        for i in range(len(self.I)):
            if i < len(self.I):
                x_offset = Icon.icon_hsize * (i % cols)
                y_offset = Icon.icon_vsize * (i // rows)
                I[i].blit(self.x + x_offset, self.y + y_offset)
            else:
                pass # Should probably blit a black square.