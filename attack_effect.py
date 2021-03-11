from particle import AttackParticle
from random import uniform
from constants import *


class AttackEffect:
    def __init__(self, owner, attack_target):
        self.attack_delay = 17
        self.step = GRID_SIZE // 2

        self.owner = owner
        self.attack_target = attack_target
        self.owner.from_x = owner.center_x
        self.owner.from_y = owner.center_y
        self.owner.fx = owner.x
        self.owner.fy = owner.y

        self.owner.state = state.ATTACK
        if Tag.player in self.owner.tag:
            self.owner.change_y = owner.dy * (MOVE_SPEED -4)
            self.owner.change_x = owner.dx * (MOVE_SPEED -4)
        else:
            self.owner.change_y = owner.dy * (MOVE_SPEED +3)
            self.owner.change_x = owner.dx * (MOVE_SPEED +3)

    def attack(self):
        if abs(self.owner.from_x - self.owner.center_x) >= self.step and self.owner.dx or\
            abs(self.owner.from_y - self.owner.center_y) >= self.step and self.owner.dy:
            self.owner.change_x = 0
            self.owner.change_y = 0
    
        # if self.attack_delay == 6:
        #     for i in range(13):
        #         if i % 2 == 0:
        #             self.attack_target.center_x += 1
        #         else:
        #             self.attack_target.center_x -= 1

        self.attack_delay -= 1

        if 0 > self.attack_delay:
            self.attack_target.alpha = 255
            # self.attack_target.center_x = self.attack_target_x
            # self.owner.center_y = self.owner.from_y
            # self.owner.center_x = self.owner.from_x
            self.owner.y = self.owner.fy
            self.owner.x = self.owner.fx
            self.owner.change_x, self.owner.change_y = 0, 0
            self.owner.dx, self.owner.dy = 0, 0
            self.owner.wait += self.owner.fighter.attack_speed
            self.owner.state = state.TURN_END

