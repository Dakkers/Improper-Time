import pyglet, drawable

class Item(drawable.Drawable):
    # We'll keep icons to a 20x20 size for now.
    icon_hsize = 50
    icon_vsize = 50

    # name: String
    # icon_path: String
    # x, y: Location of item
    def __init__(self, name, icon_path, x, y, *args, **kwargs):
        super(Item, self).__init__(image_name=icon_path, *args, **kwargs)
        self.name = name
        self.posx = x
        self.posy = y