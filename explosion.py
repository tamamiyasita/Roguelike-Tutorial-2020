import arcade

class Explosion(arcade.Sprite):
    def __init__(self, texture_list, position, sprites):
        super().__init__()

        self.current_texture = 0
        self.position = position
        self.textures = texture_list
        self.texture = texture_list[0]
        self.scale = 4
        self.timer = 0
        sprites.append(self)
        self.update_animation()

    def update_animation(self, delta_time=1 / 60):
        super().update_animation(delta_time)
        self.timer += delta_time
        if self.timer >= 0.04:

            self.current_texture += 1
            if self.current_texture < len(self.textures):
                self.set_texture(self.current_texture)
                self.timer = 0
            else:
                self.remove_from_sprite_lists()

