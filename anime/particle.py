from os import remove

from arcade import texture
from constants import GRID_SIZE, SPRITE_SCALE, TMP_EFFECT_SPRITES
import arcade
import random
import math

from arcade import particle

PARTICLE_FADE_RATE = 17

PARTICLE_MIN_SPEED = 3.5
PARTICLE_SPEED_RANGE = 2.5

PARTICLE_COUNT = 7

PARTICLE_RADIUS = 3

PARTICLE_COLORS =[
    arcade.color.YELLOW,
    arcade.color.WHITE,
    arcade.color.LAVA,
    arcade.color.ORANGE_RED,
    arcade.color.DARK_TANGERINE,
    arcade.color.BABY_BLUE,
    arcade.color.ALMOND
]

PARTICLE_SPARKLE_CHANCE = 0.02

class AttackParticle(arcade.SpriteCircle):

    def __init__(self):
        color = random.choice(PARTICLE_COLORS)
        super().__init__(radius=PARTICLE_RADIUS, color=color)

        self.normal_texture = self.texture

        a_speed = random.random() * PARTICLE_SPEED_RANGE + PARTICLE_MIN_SPEED
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * a_speed
        self.change_y = math.cos(math.radians(direction)) * a_speed

        self.my_alpha = 255

    def update_animation(self, delta_time):
        super().update_animation(delta_time)
        
        if self.my_alpha <= PARTICLE_FADE_RATE:
            # フェードアウトしたら消去
            self.remove_from_sprite_lists()
        
        else:
            # update
            self.my_alpha -= PARTICLE_FADE_RATE
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y

            if random.random() <= PARTICLE_SPARKLE_CHANCE:
                self.alpha = 255
                self.texture = arcade.make_circle_texture(self.width, arcade.color.WHITE)
            else:
                self.texture = self.normal_texture


class Expulsion(arcade.Sprite):
    def __init__(self, target, x_velocity=0, y_velocity=random.randint(-5,-2),  radius=4, color=(255,255,255), gravity_scale=1, image=None):
        super().__init__()
        self.scale = SPRITE_SCALE
        self.center_x = target.center_x
        self.center_y = target.center_y
        add = 0
        if target.left_face:
            add = random.randint(25,30)
        else:
            add = random.randint(-30,-25)

        self.x_velocity = x_velocity + add
        self.y_velocity = y_velocity
        self.radius = radius
        self.color = color
        self.gravity_scale = gravity_scale
        self.lifetime = 100
        self.gravity = 1
        self.texture = image
        TMP_EFFECT_SPRITES.append(self)

    def update(self):
        self.lifetime -= 1
        self.gravity -= self.gravity_scale
        self.center_x += self.x_velocity
        self.center_y += self.y_velocity * self.gravity
        self.angle += 50
        if self.lifetime < 0:
            self.remove_from_sprite_lists()


class Particle2(arcade.Sprite):
    def __init__(self, x, y, x_velocity, y_velocity,  radius=4, color=(255,255,255), gravity_scale=1, image=None):
        super().__init__()
        self.scale = SPRITE_SCALE
        self.center_x = x
        self.center_y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.radius = radius
        self.color = color
        self.gravity_scale = gravity_scale
        self.lifetime = 100
        self.gravity = 3
        self.texture = image

    def update(self):
        self.lifetime -= 1
        self.gravity -= self.gravity_scale
        self.center_x += self.x_velocity
        self.center_y += self.y_velocity * self.gravity
        self.angle += 50
        if self.lifetime < 0:
            self.remove_from_sprite_lists()
        # if not self.texture:
        #     arcade.draw_circle_filled(center_x=self.center_x, center_y=self.center_y, color=self.color, radius=self.radius)
        # else:
        #     arcade.draw_texture_rectangle(center_x=self.x, center_y=self.y, width=GRID_SIZE, height=GRID_SIZE, texture=self.image)


class MG(arcade.Window):
    def __init__(self, width, height, title="bsp"):
        super().__init__(width, height, title)
        # self.mx,self.my = 0,0
        self.particle = None
        


        arcade.set_background_color((200,200,200))





    def on_draw(self):
        arcade.start_render()
            


        if self.particle:
            for p in self.particle:
                p.update()
                
    def on_update(self, delta_time):
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.particle=[]
        self.mx = x
        self.my = y
        for p in range(10):
            c1,c2,c3 = random.randint(1,255),random.randint(1,255),random.randint(1,255)
            p = Particle2(self.mx, self.my, random.randrange(-8,8), random.randrange(-12, -1), 4, (c1,c2,c3),.5)
            self.particle.append(p)
        print(self.mx, self.my)

    def on_key_release(self, symbol: int, modifiers: int):
        self.mx, self.my = 0,0
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

def main():
    gam = MG(600, 600)
    arcade.run()

if __name__ == "__main__":
    main()


    
