import arcade
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"

class Aw(arcade.SpriteSolidColor):
    def __init__(self, width: int, height: int, color):
        super().__init__(width, height, color)
        self.center_x = 100
        self.center_y = 100
        self.target_x = 760
        self.target_y = 560
        self.t = 0
        self.angle = 45
        self.base_range = 5
        self.max_angle = 50
        self.ratio = 0.7

    def update(self):
        super().update()
        p2 = (self.target_x-self.center_x, self.target_y-self.center_x)

        dist = arcade.get_distance(self.center_x, self.center_y, self.target_x, self.target_y)

        self.angle = self.angle * dist / self.base_range
        if self.angle > self.max_angle:
            self.angle = self.max_angle

        p1x = p2[0] * self.ratio
        p1y = math.sin(math.degrees(self.angle)) * abs(p1x) / math.cos(math.degrees(self.angle))
        p1 = (p1x, p1y)
        look = (p1x, p1y)


        vx = 2 * (1 - self.t) * self.t *

aw = Aw(10,10,(250,100,0))

s_list = arcade.SpriteList()
s_list.append(aw)
class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        s_list.draw()

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

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
        """
        Called when the user presses a mouse button.
        """
        pass

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