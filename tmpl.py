import arcade
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"

blank = 40
size = 20

WIDTH  = 640  # 幅
HEIGHT = 400  # 高さ
SIZE   = 20   # 辺長
BLANK  = 40   # 余白
angle = 0


class Aw(arcade.SpriteSolidColor):
    def __init__(self, width=20, height=20, color=arcade.color.BLACK_BEAN):
        super().__init__(width, height, color)
        self.center_x = 0
        self.center_y = 0
        # self._angle = 0

    # def ang(self):
    #     for x in range(0, SCREEN_WIDTH):
    #         self.left = x
    #         self.top = int(SCREEN_HEIGHT-math.sin(math.radians(self._angle))*(SCREEN_HEIGHT-blank))-size

    #         if self._angle >= 180-1:
    #             self._angle = 0
    #         else:
    #             self._angle += 1
   
        

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

        self._angle = 0
        self.p = 0
        self.state = 0
        self.x_point = 0
        self.y_point = 0
        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.aw = Aw()

        self.s_list = arcade.SpriteList()
        self.s_list.append(self.aw)
        # pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        self.s_list.draw()
        # for x in range(0, SCREEN_WIDTH):
            # self.aw.left =  x
            # self.aw.top = int(SCREEN_HEIGHT-math.sin(math.radians(self._angle))*(SCREEN_HEIGHT-blank))-size
            # self.s_list.draw()

            # if self.aw._angle >= 180-1:
            #     self.aw._angle = 0
            # else:
            #     self.aw._angle += 1

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        # self.s_list.update()
        if self.state:
            self.p += 1
            # if self.x_point < self.p:
            #     self.state = 0


            # self.aw.top = self.p
            self.aw.center_x = int(self.x_point-math.sin(math.radians(self._angle))*(self.x_point-BLANK))-SIZE
            self.aw.center_y = int(self.y_point-math.sin(math.radians(self.y_point))*(self.y_point-BLANK))-SIZE

            if self._angle >= 180-1:
                self._angle = 0
            else:
                self._angle += 1



        


    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.A:
            self.state = 1
        else:
            self.state = 0
            # self.p = 0
            # if self.p >= SCREEN_HEIGHT:
            #     self.p = 0
   


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
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.x_point = x
            self.y_point = y
            self.state = 1
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.state = 0
        """
        Called when the user presses a mouse button.
        """
        # pass
        

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(WIDTH, HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()