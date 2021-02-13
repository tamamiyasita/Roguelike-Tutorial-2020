from particle import AttackParticle
from random import uniform
from constants import *
PARTICLE_COUNT = 7


class CombatEffect:
    def __init__(self,sprites):
        self.attack_delay = 7
        self.tmp_effect_sprites = sprites
        self.step = GRID_SIZE // 2


    def attack(self, owner, attack_target, from_x, from_y, attack_target_x):
        attack_target.state = state.DEFENSE
        

        if abs(from_x - owner.center_x) >= self.step and owner.dx or\
                abs(from_y - owner.center_y) >= self.step and owner.dy:
            owner.change_x = 0
            owner.change_y = 0

        if self.attack_delay == 6:
            for i in range(PARTICLE_COUNT):
                particle = AttackParticle()
                particle.position = (
                    owner.center_x + (owner.dx*20), owner.center_y + (owner.dy*20))
                self.tmp_effect_sprites.append(particle)
                attack_target.change_x += uniform(-0.7, 0.7)

        if self.attack_delay % 2 == 0:

            attack_target.alpha = 10
        else:
            attack_target.alpha = 155

        if owner.change_x == 0 and owner.change_y == 0 and owner.state != state.TURN_END:
            self.attack_delay -= 1

            if 0 > self.attack_delay:
                owner.center_y = owner.from_y
                owner.center_x = owner.from_x
                owner.change_x, owner.change_y = 0, 0
                attack_target.alpha = 255
                attack_target.change_x = 0
                attack_target.center_x = attack_target_x
                owner.wait = owner.fighter.attack_speed
                owner.state = state.TURN_END
