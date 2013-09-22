import pyglet

class Item(pyglet.sprite.Sprite):
    # We'll keep icons to a 20x20 size for now.
    icon_hsize = 50
    icon_vsize = 50

    # name: String
    # icon: AbstractImage or Animation
    # x, y: Location of item
    def __init__(self, name, icon, x, y, *args, **kwargs):
        super(Item, self).__init__(icon, *args, **kwargs)
        self.name = name