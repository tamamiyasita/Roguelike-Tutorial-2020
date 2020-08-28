from actor.actor import Actor
from constants import *
from data import *


class AttackEffect(Actor):
    def __init__(self, owner, effect_sprites=None):
        super().__init__(
            x=owner.x,
            y=owner.y,
            name=owner.name,
            color=COLORS["white"],
            attack_texture=owner.attack_texture
            
        )
        self.owner = owner
        self.effect_sprites = effect_sprites
        self.dx, self.dy = self.owner.dx, self.owner.dy

        if self.owner.attack_texture is not None:
            self.name = self.owner.attack_texture

        
        self.target_x = self.center_x
        self.target_y = self.center_y
        
        self.change_y = self.dy * 2
        self.change_x = self.dx * 2

        self.effect_sprites.append(self)
        self.alpha = 255
        
    def update(self):
        self.owner.alpha = 0
        step = GRID_SIZE // 2
        self.center_x += self.change_x
        self.center_y += self.change_y
                    
        if abs(self.target_x - self.center_x) >= step and self.dx:
            self.change_x = 0
            self.center_x = self.target_x
            self.owner.state = state.TURN_END
        if abs(self.target_y - self.center_y) >= step and self.dy:
            self.change_y = 0
            self.center_y = self.target_y
            self.owner.state = state.TURN_END
        
        if self.owner.state == state.TURN_END:
            self.effect_sprites.remove(self)
            self.owner.alpha = 255
