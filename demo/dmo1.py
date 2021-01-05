import arcade

from arcade import Vector
from arcade.utils import _Vec2
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"



class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.dig = 70

        arcade.set_background_color(arcade.color.AMAZON)
        self.x, self.y = 100, 100
        self.en_list = arcade.SpriteList()
        self.target_x = 10
        self.target_y = 1

        self.en = arcade.SpriteCircle(10,(255,255,255))
        # self.en.center_x = SCREEN_WIDTH/2
        # self.en.center_y = SCREEN_HEIGHT/2
        self.en_list.append(self.en)



        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

    def on_draw(self):
        """
        Render the screen.
        """       
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        self.en_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.en_list.update()
        # try:
        # self.target_x = self.en.center_x - self.target_x
        # self.target_y = self.en.center_y - self.target_y
        self.b = math.tan(math.degrees(self.dig))
        self.a = (self.target_y - self.b * self.target_x) / (self.target_x * self.target_x)

        self.en.center_y = (self.a * self.en.center_x**2 + self.b * self.en.center_x)

        # except:
        #     pass
    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        print(x)
        self.en.center_x = x -20
        self.en.center_y = y -20
        self.en.change_x = 1
        self.target_x = x
        self.target_y = y


        

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()