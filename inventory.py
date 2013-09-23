import pyglet
import item

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
        if len(self.I) >= (self.rows*self.cols):
            print "Inventory is full! Cannot add " + item.name + "!"
        else:
            self.I.append(item)

    def removeItem(self, item):
        if item in self.I:
            self.I.remove(item)
        else:
            print item.name + " not found in inventory!"

    def updateItemPositions(self, charx, chary):
        for i in range(len(self.I)):
            if i < len(self.I):
                x_offset = 50 * (i % self.cols)
                y_offset = 50 * (i // self.rows)
                if charx < 200:
                    self.I[i].posx = 200
                else:
                    self.I[i].posx = charx
                self.I[i].posy = 350
            else:
                pass # Should probably blit a black square.