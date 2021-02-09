from particle import AttackParticle
from random import uniform
from constants import *
PARTICLE_COUNT = 7


class AttackEffect:
    def __init__(self,sprites):
        self.attack_delay = 7
        self.tmp_effect_sprites = sprites
        self.step = GRID_SIZE // 2


    def start(self, actor, other, from_x, from_y, other_x):
        

        if abs(from_x - actor.center_x) >= self.step and actor.dx or\
                abs(from_y - actor.center_y) >= self.step and actor.dy:
            actor.change_x = 0
            actor.change_y = 0

        if self.attack_delay == 6:
            for i in range(PARTICLE_COUNT):
                particle = AttackParticle()
                particle.position = (
                    actor.center_x + (actor.dx*20), actor.center_y + (actor.dy*20))
                self.tmp_effect_sprites.append(particle)
                other.change_x += uniform(-0.7, 0.7)

        if self.attack_delay % 2 == 0:
            # if Tag.player in other.tag: 
            other.state = state.DEFENSE

            other.alpha = 10
        else:
            other.alpha = 155

        if actor.change_x == 0 and actor.change_y == 0 and actor.state != state.TURN_END:
            self.attack_delay -= 1

            if 0 > self.attack_delay:
                actor.center_y = actor.from_y
                actor.center_x = actor.from_x
                actor.change_x, actor.change_y = 0, 0
                other.alpha = 255
                other.change_x = 0
                other.center_x = other_x
                actor.state = state.TURN_END

        if actor.state == state.TURN_END:
            actor.wait = actor.fighter.attack_speed