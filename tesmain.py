import arcade
from collections import deque
from status_bar import draw_status_bar

class MG(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.pc = arcade.SpriteSolidColor(width=32, height=32, color=arcade.color.BATTLESHIP_GREY)
        self.pc.name = "entity"
        self.pc.center_x = 50
        self.pc.center_y = 50
        self.enm = arcade.SpriteSolidColor(width=32, height=32, color=arcade.color.RACKLEY)
        self.enm.name = "actor"
        self.enm.center_x = 200
        self.enm.center_y = 200
        self.list = arcade.SpriteList()
        self.list.append(self.pc)
        self.list.append(self.enm)
        self.mouse_over_text = None
        self.log = []
        self.a = False

        self.hp = 45
        self.messages = deque(maxlen=3)
    def on_draw(self):
        arcade.start_render()
        arcade.draw_xywh_rectangle_filled(380,120,220,300, color=arcade.color.AIR_FORCE_BLUE)
        arcade.draw_xywh_rectangle_filled(20,0,500,100, color=arcade.color.BALL_BLUE)
        self.list.draw()
        text = f" HP:{self.hp} self.hp/ self.max_hp"
        arcade.draw_text(text, 20, 0, arcade.color.WHITE)

        size = 65
        margin = 30
        draw_status_bar(size / 2 + margin, 24, size, 10, self.hp, 50)

        # while len(self.messages) > 3:
        #     self.messages.pop()

        # if len(self.messages) >= 1:
        #     text = self.messages[0]
        #     arcade.draw_text(text, 200, 35, arcade.color.WHITE)

        # if len(self.messages) >= 2:
        #     text = self.messages[1]
        #     arcade.draw_text(text, 200, 20, arcade.color.DAFFODIL)
        
        # if len(self.messages) == 3:
        #     text = self.messages[2]
        #     arcade.draw_text(text, 200, 5, arcade.color.AFRICAN_VIOLET)
        y = 60
        for message in self.messages:
            arcade.draw_text(message, 200, y, color=arcade.color.WHITE,anchor_x="right")
            self.log.append(self.messages[0])
            y -= 20
        
        if self.mouse_over_text:
            x, y = self.mouse_position
            arcade.draw_rectangle_filled(x, y+8, 160, 16, arcade.color.BLACK_BEAN)
            arcade.draw_text(self.mouse_over_text, x, y, arcade.color.WHITE, anchor_x="center")
    def on_update(self, delta_time):
        self.list.update()
        if self.a:
            self.attack()

        

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.pc.center_y += 32
            self.hp -= 1
            self.messages.appendleft("torn")
        if key == arcade.key.DOWN:
            self.hp += 1
            self.pc.center_y += -32
            self.messages.appendleft("557989")
        if key == arcade.key.LEFT:
            self.pc.center_x += - 32
            self.messages.appendleft("context")
        if key == arcade.key.RIGHT:
            self.pc.center_x += 32
            self.messages.appendleft("def text")
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.A:
            self.dist = self.pc.center_x+32
            self.a = True
        print(self.messages)
        # print("LOG:",self.log)

    def attack(self):
        self.pc.change_x += 5 
        if self.dist < self.pc.center_x:
            self.pc.center_x = self.dist-32
            self.pc.change_x = 0
            self.a = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_position = x, y
        # print(self.mouse_position)
        sprite_list = arcade.get_sprites_at_point((x, y), self.list)
        print(sprite_list)
        self.mouse_over_text = None
        for sprite in sprite_list:
            if sprite:
                self.mouse_over_text = f"{sprite.name} in wark"

window = MG(500, 500)
arcade.run()

