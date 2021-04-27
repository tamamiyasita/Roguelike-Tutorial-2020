import arcade
import arcade.gl as gl


class MG(arcade.Window):
    def __init__(self, width, height, title="cell"):
        super().__init__(width, height, title)
        self.window = arcade.get_window()
        print(self.window.width)
        
        

        arcade.set_background_color((200,200,200))



    def on_draw(self):
        arcade.start_render()

        
        
                   
    def on_update(self, delta_time):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

def main():
    gam = MG(600, 600)
    arcade.run()

if __name__ == "__main__":
    main()

