import arcade
import random
import math

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

        speed = random.random() * PARTICLE_SPEED_RANGE + PARTICLE_MIN_SPEED
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * speed
        self.change_y = math.cos(math.radians(direction)) * speed

        self.my_alpha = 255

    def update(self):

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

