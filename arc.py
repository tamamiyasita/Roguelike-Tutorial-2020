import arcade
from arcade import sprite
GRID_SIZE = 32

from data import * 

class Spriteset(arcade.Sprite):
    def __init__(self, Entity):
        super().__init__()

        self.entity = Entity
    def re_setup(self, Entity):
        self.entity = Entity

    def update(self, delta_time=1/60):
        super().update()
        if self.entity.move_sw:
            self.center_y = self.entity.center_y
            self.center_x = self.entity.center_x
            self.entity.move_sw = False
        self.change_y = self.entity.change_y
        self.change_x = self.entity.change_x
        self.color = self.entity.color
        self.alpha = self.entity.alpha
        if self.change_x:
            print(f"{self.change_x=}")
class Entity:
    def __init__(self, x=0, y=0, color=[255,255,255], alpha=255) -> None:
        self._x = x
        self._y = y
        self._center_x = None
        self._center_y = None
        self._color = color
        self._alpha = alpha
        self._change_x = 0
        self._change_y = 0
        self.move_sw = False
    @property
    def change_x(self):
        return self._change_x
    @change_x.setter
    def change_x(self, value):
        self._change_x = value
        return self._change_x
    
    @property
    def change_y(self):
        return self._change_y
    @change_y.setter
    def change_y(self, value):
        self._change_y = value
        return self._change_y

    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y
    @x.setter
    def x(self, value):
        self._x = value
        self.center_x = self._x * GRID_SIZE
        # self.sprite.center_x = self._x * GRID_SIZE
    @y.setter
    def y(self, value):
        self._y = value
        self.center_y = self._y * GRID_SIZE
        # self.sprite.center_y = self._y * GRID_SIZE

    @property
    def center_x(self):
        return self._center_x
    @property
    def center_y(self):
        return self._center_y
    @center_x.setter
    def center_x(self, value):
        self._center_x = value
        # self.sprite.center_x = self._center_x
        self._x = self._center_x // GRID_SIZE
    @center_y.setter
    def center_y(self, value):
        self._center_y = value
        # self.sprite.center_y = self._center_y
        self._y = self._center_y // GRID_SIZE

    @property
    def color(self):
        # self.sprite.color = self._color
        return self._color
    @color.setter
    def color(self,value):
        self._color = value
        # self.sprite.color = self._color

    @property
    def alpha(self):
        return self._alpha
    @alpha.setter
    def alpha(self, value):
        self._alpha = value
        if self._alpha > 255:
            self._alpha = 255
        elif self._alpha < 1:
            self._alpha = 0
        # self.sprite.alpha = self._alpha

    def __repr__(self) -> str:
        return f"{self.x=} {self.y=} {self.change_x=} {self.change_y=} {self.center_x=} {self.center_y=} {self.color=} {self.alpha=}"

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.move_sw = True

# TODO シェルフで保存に挑戦する 別の関数で整理しないと保存できないな
import shelve



MARGIN = GRID_SIZE
SCREEN_WIDTH=GRID_SIZE*20+MARGIN
SCREEN_HEIGHT=GRID_SIZE*15+MARGIN

class MG(arcade.Window):
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title="test"):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)


    def setup(self):
        self.pc_sprites = arcade.SpriteList()
        self.pc = Entity(10,10, color=[200,150,255])
        self.pc_sprite = Spriteset(self.pc)
        self.pc_sprite.texture = crab_0[0]
        self.pc_sprites.append(self.pc_sprite)

    def on_update(self, delta_time: float):
        self.pc_sprites.update()

    def on_draw(self):
        arcade.start_render()
        self.pc_sprites.draw()


    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.RIGHT:
            self.pc.move(1,0)
        if key == arcade.key.LEFT:
            self.pc.move(-1,0)
        if key == arcade.key.UP:
            self.pc.move(0,1)
        if key == arcade.key.DOWN:
            self.pc.move(0,-1)
        if key == arcade.key.B:
            self.pc.center_x = SCREEN_WIDTH // 2
        if key == arcade.key.C:
            self.pc.color[0] -= 40
        if key == arcade.key.D:
            self.pc.color[0] += 30
        if key == arcade.key.E:
            self.pc.alpha += 20
        if key == arcade.key.F:
            self.pc.alpha -= 20
        if key == arcade.key.K:
            self.pc.change_x = 5

        if key == arcade.key.S:
            a = shelve.open("tst_cls")
            a["tst"] = self.pc
            a.close()

        if key == arcade.key.L:
            a = shelve.open("tst_cls")
            self.pc = a["tst"]
            self.pc_sprite.re_setup(self.pc)
            a.close()
            


        if key == arcade.key.A:
            print(self.pc)
            

    def on_key_release(self, symbol: int, modifiers: int):
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        pass


def main():
    game = MG()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()


