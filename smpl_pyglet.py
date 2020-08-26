import arcade
import pyglet
from pyglet import image, window


class MGS(arcade.Window):
    def __init__(self):
        super().__init__(width=500, height=500, resizable=True)

        image = arcade.load_texture("image\Effect1.png")

    def on_draw(self):
        arcade.start_render()
        txti = arcade.texture.make_soft_square_texture(300,arcade.color.AERO_BLUE,222,30)

def main():
    window = MGS()
    arcade.run()

if __name__ == "__main__":
    main() 
