from particle import AttackParticle
from random import uniform
from constants import *


class AttackEffect:
    def __init__(self, owner, attack_target):
        self.attack_delay = 15
        self.step = GRID_SIZE // 2

        self.owner = owner
        self.attack_target = attack_target
        self.from_x = owner.center_x
        self.from_y = owner.center_y
        self.attack_target_x = attack_target.center_x


    def attack(self):
        self.attack_target.state = state.DEFENSE

        if self.attack_delay == 6:
            for i in range(13):
                if i % 2 == 0:
                    self.attack_target.center_x += 1
                else:
                    self.attack_target.center_x -= 1

        if self.attack_delay % 2 == 0:

            self.attack_target.alpha = 10
        else:
            self.attack_target.alpha = 155

        if self.owner.state != state.TURN_END:
            self.attack_delay -= 1

            if 0 > self.attack_delay:
                self.attack_target.alpha = 255
                self.attack_target.center_x = self.attack_target_x
                self.owner.center_y = self.owner.from_y
                self.owner.center_x = self.owner.from_x
                self.owner.change_x, self.owner.change_y = 0, 0
                self.owner.wait = self.owner.fighter.attack_speed
                self.owner.state = state.TURN_END
