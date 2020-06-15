import arcade

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
TITLE = "Roguelike tutorial 2020"
pcimg = "rou6.png"


class MG(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.player = None

    def setup(self):
        arcade.set_background_color(arcade.color.WHITE)

        self.actor_list = arcade.SpriteList()
        self.player = arcade.Sprite(pcimg, center_x=50, center_y=50)
        self.actor_list.append(self.player)

    def on_draw(self):
        arcade.start_render()
        self.actor_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
