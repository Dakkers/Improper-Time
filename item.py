import pyglet

class Item(pyglet.sprite.Sprite):
    # We'll keep icons to a 20x20 size for now.
    icon_hsize = 20
    icon_vsize = 20

    # name: String
    # icon: AbstractImage or Animation
    def __init__(self, name, icon, *args, **kwargs):
        super(Item, self).__init__(icon, *args, **kwargs)
        self.name = name