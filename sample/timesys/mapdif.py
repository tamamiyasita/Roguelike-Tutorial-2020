import arcade
import random
from arcade import particle

from arcade.gl import geometry

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
SCREEN_TITLE = "DEF"

PLAYING_FIELD_WIDTH = 5000
PLAYING_FIELD_HEIGHT = 1000

MINIMAP_HEIGHT = 200

MAIN_SCREEN_HEIGHT = SCREEN_HEIGHT - MINIMAP_HEIGHT


VIEWPORT_MARGIN = SCREEN_WIDTH / 2 -50
TOP_VIEWPORT_MARGIN = 30
DEFAULT_BOTTOM_VIEWPORT = -10

MAX_HORIZONTAL_MOVEMENT_SPEED = 10
MAX_VERTICAL_MOVEMENT_SPEED = 5
HORIZONTAL_ACCELERATION = 0.5
VERTICAL_ACCELERATION = 0.2
MOVEMENT_DRAG = 0.08

BULLET_MAX_DISTANCE = SCREEN_WIDTH * 0.75

class Player(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(40, 10, arcade.color.SLATE_GRAY)
        self.face_right = True

    def accelerate_up(self):
        self.change_y += VERTICAL_ACCELERATION
        if self.change_y > MAX_VERTICAL_MOVEMENT_SPEED:
            self.change_y = MAX_VERTICAL_MOVEMENT_SPEED

    def accelerate_down(self):
        self.change_y -= VERTICAL_ACCELERATION
        if self.change_y < MAX_VERTICAL_MOVEMENT_SPEED:
            self.change_y = -MAX_VERTICAL_MOVEMENT_SPEED

    def accelerate_right(self):
        self.face_right = True
        self.change_x += HORIZONTAL_ACCELERATION
        if self.change_x > MAX_HORIZONTAL_MOVEMENT_SPEED:
            self.change_x = MAX_HORIZONTAL_MOVEMENT_SPEED

    def accelerate_left(self):
        self.face_right = False
        self.change_x -= HORIZONTAL_ACCELERATION
        if self.change_x < MAX_HORIZONTAL_MOVEMENT_SPEED:
            self.change_x = -MAX_HORIZONTAL_MOVEMENT_SPEED

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x > 0:
            self.change_x -= MOVEMENT_DRAG            
        if self.change_x < 0:
            self.change_x += MOVEMENT_DRAG
        if abs(self.change_x) < MOVEMENT_DRAG:
            self.change_x = 0

        if self.change_y > 0:
            self.change_y -= MOVEMENT_DRAG            
        if self.change_y < 0:
            self.change_y += MOVEMENT_DRAG
        if abs(self.change_y) < MOVEMENT_DRAG:
            self.change_y = 0

        if self.left < 0:
            self.left = 0
        elif self.right > PLAYING_FIELD_WIDTH - 1:
            self.right = PLAYING_FIELD_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > PLAYING_FIELD_HEIGHT - 1:
            self.top = PLAYING_FIELD_HEIGHT - 1


class Bullet(arcade.SpriteSolidColor):
    def __init__(self, width, height, color):
        super().__init__(width, height, color)
        self.distance = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.distance > BULLET_MAX_DISTANCE:
            self.remove_from_sprite_lists()

class Particle(arcade.SpriteSolidColor):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.alpha -= 5
        if self.alpha <= 0:
            self.remove_from_sprite_lists()

class MG(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.player_list = None
        self.star_sprite_list = None
        self.enemy_sprite_list = None
        self.bullet_sprite_list = None

        self.player_sprite = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.view_bottom = 0
        self.view_left = 0

        arcade.set_background_color(arcade.color.BLACK)

        screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)

        mini_map_size = (SCREEN_WIDTH, MINIMAP_HEIGHT)

        mini_map_pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - MINIMAP_HEIGHT / 2)

        self.program = self.ctx.load_program(
            vertex_shader=arcade.resources.shaders.vertex.default_projection,
            fragment_shader=arcade.resources.shaders.fragment.texture
        )

        self.mini_map_color_attachment = self.ctx.texture(screen_size)

        self.mini_map_screen = self.ctx.framebuffer(color_attachments=[self.mini_map_color_attachment])

        self.mini_map_rect = geometry.screen_rectangle(0, SCREEN_WIDTH, MINIMAP_HEIGHT, SCREEN_HEIGHT)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.star_sprite_list = arcade.SpriteList()
        self.enemy_sprite_list = arcade.SpriteList()
        self.bullet_sprite_list = arcade.SpriteList()

        self.player_sprite = Player()
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        for i in range(100):
            sprite = arcade.SpriteSolidColor(4, 4, arcade.color.WHITE)
            sprite.center_x = random.randrange(PLAYING_FIELD_WIDTH)
            sprite.center_y = random.randrange(PLAYING_FIELD_HEIGHT)
            self.star_sprite_list.append(sprite)

        for i in range(30):
            sprite = arcade.SpriteSolidColor(20, 20, arcade.color.LIGHT_SALMON)
            sprite.center_x = random.randrange(PLAYING_FIELD_WIDTH)
            sprite.center_y = random.randrange(PLAYING_FIELD_HEIGHT)
            self.enemy_sprite_list.append(sprite)

    def on_draw(self):

        arcade.start_render()

        self.mini_map_screen.use()
        self.mini_map_screen.clear()

        arcade.set_viewport(0,
                            PLAYING_FIELD_WIDTH,
                            0,
                            PLAYING_FIELD_HEIGHT)
        self.enemy_sprite_list.draw()
        self.player_list.draw()

        self.use()

        arcade.set_viewport(self.view_left,
                            SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            SCREEN_HEIGHT + self.view_bottom)

        self.star_sprite_list.draw()
        self.enemy_sprite_list.draw()
        self.bullet_sprite_list.draw()
        self.player_list.draw()

        arcade.draw_rectangle_filled(SCREEN_WIDTH - SCREEN_WIDTH / 2 + self.view_left,
                                     SCREEN_HEIGHT - MINIMAP_HEIGHT + MINIMAP_HEIGHT / 2 + self.view_bottom,
                                     SCREEN_WIDTH,
                                     MINIMAP_HEIGHT,
                                     arcade.color.DARK_GREEN)

        self.mini_map_color_attachment.use(0)
        self.mini_map_rect.render(self.program)

        width_ratio = SCREEN_WIDTH / PLAYING_FIELD_WIDTH
        height_ratio = MINIMAP_HEIGHT / PLAYING_FIELD_HEIGHT
        width = width_ratio * SCREEN_WIDTH
        height = height_ratio * MAIN_SCREEN_HEIGHT

        x = (self.view_left + SCREEN_WIDTH / 2) * width_ratio + self.view_left
        y = (SCREEN_HEIGHT - MINIMAP_HEIGHT) + self.view_bottom + height / 2 + (MAIN_SCREEN_HEIGHT / PLAYING_FIELD_HEIGHT) * self.view_bottom

        arcade.draw_rectangle_outline(center_x=x, center_y=y, width=width, height=height, color=arcade.color.WHITE)

    def on_update(self, delta_time: float):

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.accelerate_up()
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.accelerate_down()

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.accelerate_left()
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.accelerate_right()

        self.player_list.update()
        self.bullet_sprite_list.update()

        for bullet in self.bullet_sprite_list:
            enemy_hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_sprite_list)
            for enemy in enemy_hit_list:
                enemy.remove_from_sprite_lists()
                for i in range(10):
                    particle = Particle(4,4,arcade.color.RED)
                    while particle.change_y == 0 and particle.change_x == 0:
                        particle.change_y = random.randrange(-2, 3)
                        particle.change_x = random.randrange(-2, 3)
                        particle.change_x = enemy.center_x
                        particle.change_y = enemy.center_y
                        self.bullet_sprite_list.append(particle)

        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left

        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.left - right_boundary 

        self.view_bottom = DEFAULT_BOTTOM_VIEWPORT
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN - MINIMAP_HEIGHT

        


        



