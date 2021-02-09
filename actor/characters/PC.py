# from actor.actor import Actor
from actor.actor import Actor
from actor.fighter import Fighter
from actor.equipment import Equipment
from data import *
from constants import *
from util import exp_calc
from random import choices
from actor.skills.base_skill import BaseSkill


class Player(Actor):
    def __init__(self, x=0, y=0, inventory=0):
        unarmed_component = BaseSkill(damage=2)
        fighter_component = Fighter(hp=15, STR=2, DEX=3, INT=3,
                                    unarmed=unarmed_component,
                                    resist={"physical": 1, "fire": 1, "ice": 1, "acid": 1, "poison": 1, "mind": 1},
                                    defense=2,
                                    evasion=5,
                                    level=1
                                    )
        equip_component = Equipment()
        super().__init__(
            name="Rou",
            x=x,
            y=y,
            color=COLORS["white"],

            inventory=inventory,
            fighter=fighter_component,
            equipment=equip_component,
            

        )
        self.tag = [Tag.player]
        self.race = "Alraune"

        self.state = state.READY
        self.delay_time = 5
        self.visible_check = False

        self.experience_per_level = exp_calc()



    def update_animation(self, delta_time=1 / 60):
        super().update_animation(delta_time)

        if self.state == state.ON_MOVE and not self.left_face:
            self.delay_time = 3
            self.texture = pc_move1[0]
            
        if self.state == state.ON_MOVE and self.left_face:
            self.delay_time = 3
            self.texture = pc_move1[1]

        if self.state == state.ATTACK and not self.left_face:
            self.texture = pc_attack[0]
        if self.state == state.ATTACK and self.left_face:
            self.texture = pc_attack[1]


        if self.state == state.DOOR and not self.left_face:
            self.texture = pc_open[0]
        if self.state == state.DOOR and self.left_face:
            self.texture = pc_open[1]
  
        if self.state == state.SHOT and not self.left_face:
            self.texture = pc_shot[0]
        if self.state == state.SHOT and self.left_face:
            self.texture = pc_shot[1]

        if self.state == state.THROW and not self.left_face:
            self.texture = pc_throw[0]
        if self.state == state.THROW and self.left_face:
            self.texture = pc_throw[1]

        if self.state == state.DEFENSE and not self.left_face:
            self.texture = pc_def[0]
        if self.state == state.DEFENSE and self.left_face:
            self.texture = pc_def[1]

        if self.state == state.READY and not self.left_face:
            self.texture = player[0]
            self.delay_time -= delta_time
            if self.delay_time < 0.7:
                self.texture = pc_delay2[0]
            if self.delay_time <= 0.5:
                self.texture = pc_delay[0]
            if self.delay_time < 0:
                self.delay_time = 5


        if self.state == state.READY and self.left_face:
            self.texture = player[1]
            self.delay_time -= delta_time
            if self.delay_time < 0.7:
                self.texture = pc_delay2[1]
            if self.delay_time <= 0.5:
                self.texture = pc_delay[1]
            if self.delay_time < 0:
                self.delay_time = 5

