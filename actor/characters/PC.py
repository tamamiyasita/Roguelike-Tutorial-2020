# from actor.actor import Actor
from actor.actor import Actor
from actor.player_fighter import PC_Fighter
from actor.equipment import Equipment
from data import *
from constants import *
from util import exp_calc, grid_to_pixel
from random import choices
from actor.skills.base_skill import BaseSkill
from random import uniform
from enum import Enum, auto
import random

class Player(Actor):
    def __init__(self, x=0, y=0, inventory=0):
        unarmed_component = BaseSkill()
        unarmed_component.tag.append(Tag.weapon)
        fighter_component = PC_Fighter(hp=85, STR=2, DEX=3, INT=3,
                                    resist={"physical": 1, "fire": 0, "ice": 1, "elec":1, "acid": 1, "poison": 1, "mind": 1},#雷忘れてた
                                    defense=2,
                                    evasion=5,
                                    level=1
                                    )
        equip_component = Equipment()
        super().__init__(
            name="Rou",
            image="Rou",
            x=x,
            y=y,
            color=COLORS["white"],
            blocks=True,

            inventory=inventory,
            equipment=equip_component,
            

        )
        self.fighter=fighter_component
        self.fighter.owner = self

        self.tag = [Tag.player, Tag.use_door]
        self.race = "Alraune"

        self.state = state.READY
        self.tmp_state = state.READY
        self.delay_time = 5
        self.visible_check = False
        self.form = form.NORMAL

        self.unarmed = unarmed_component
        self.unarmed.owner = self

        self.experience_per_level = exp_calc()

    




    def update(self):
        super().update()

            
        if self.state == state.ON_MOVE:

            if abs(self.from_x - self.center_x) >= GRID_SIZE  or abs(self.from_y - self.center_y) >= GRID_SIZE:
                self.change_x = 0
                self.change_y = 0
                self.x += self.dx
                self.y += self.dy
                # self.fighter.wait += self.fighter.speed
                self.dx, self.dy = 0, 0
                
                self.from_x, self.from_y = self.center_x, self.center_y
                self.state = state.TURN_END
                self.form = form.NORMAL
        if self.state == state.TURN_END:
            self.change_x = 0
            self.change_y = 0
            self.center_x, self.center_y = grid_to_pixel(self.x, self.y)
        elif self.state == state.READY:
            self.change_x = 0
            self.change_y = 0
            self.center_x, self.center_y = grid_to_pixel(self.x, self.y)


    def update_animation(self, delta_time=1 / 60):
        super().update_animation(delta_time)

        if self.state == state.ON_MOVE and not self.left_face and self.tmp_state != state.AUTO:
            self.form = form.ON_MOVE
            self.delay_time = 3
            self.texture = pc_move1[0]
        if self.state == state.ON_MOVE and self.left_face and self.tmp_state != state.AUTO:
            self.form = form.ON_MOVE
            self.delay_time = 3
            self.texture = pc_move1[1]

        if self.state == state.ATTACK and not self.left_face:
            self.form = form.ATTACK
            self.texture = pc_attack[0]
        if self.state == state.ATTACK and self.left_face:
            self.form = form.ATTACK
            self.texture = pc_attack[1]

        if self.tmp_state == state.AUTO and not self.left_face:
            self.form = form.AUTO_MOVE
            p = random.randint(0,2)
            self.texture = pc_auto_move[p][0]
        if self.tmp_state == state.AUTO and self.left_face:
            self.form = form.AUTO_MOVE
            p = random.randint(0,2)
            self.texture = pc_auto_move[p][1]

        


        if self.form == form.DOOR and not self.left_face:
            self.texture = pc_open[0]
        if self.form == form.DOOR and self.left_face:
            self.texture = pc_open[1]
  
        if self.form == form.SHOT and not self.left_face:
            self.texture = pc_shot2[0]
        if self.form == form.SHOT and self.left_face:
            self.texture = pc_shot2[1]

        if self.form == form.THROW and not self.left_face:
            self.texture = pc_throw[0]
        if self.form == form.THROW and self.left_face:
            self.texture = pc_throw[1]

        if self.form == form.SMILE and not self.left_face:
            self.texture = pc_smy[0]
        if self.form == form.SMILE and self.left_face:
            self.texture = pc_smy[1]

        if self.form == form.DEFENSE and not self.left_face:
            self.texture = pc_def[0]
            # self.change_x += uniform(-0.7, 0.7)

        if self.form == form.DEFENSE and self.left_face:
            self.texture = pc_def[1]




        if self.form == form.NORMAL and self.left_face:
            self.texture = player[1]
            self.delay_time -= delta_time
            if self.delay_time < 0.7:
                self.texture = pc_delay2[1]
            if self.delay_time <= 0.5:
                self.texture = pc_delay[1]
            if self.delay_time < 0:
                self.delay_time = 5
        if self.form == form.NORMAL and not self.left_face:
            self.texture = player[0]
            self.delay_time -= delta_time
            if self.delay_time < 0.7:
                self.texture = pc_delay2[0]
            if self.delay_time <= 0.5:
                self.texture = pc_delay[0]
            if self.delay_time < 0:
                self.delay_time = 5