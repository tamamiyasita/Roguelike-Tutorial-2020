# from actor.actor import Actor
from actor.actor import Actor
from actor.fighter import Fighter
from actor.equipment import Equipment
from data import *
from constants import *
from util import exp_calc
from random import choices


class Player(Actor):
    def __init__(self, x=0, y=0, inventory=0):
        fighter_component = Fighter(hp=30, STR=30, DEX=4, INT=4,
                                    unarmed_attack=2,
                                    hit_rate=100,
                                    defense=1,
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

    # def check_experience_level(self, game_engine):
    #     # TODO やっぱengineに移動させよう
    #     flower_list = []

    #     if self.fighter.level < len(self.experience_per_level):
    #         xp_to_next_level = self.experience_per_level[self.fighter.level+1]
    #         if self.fighter.current_xp >= xp_to_next_level:
    #             self.fighter.level += 1
    #             self.fighter.ability_points += 1
    #             game_engine.action_queue.extend([{"message": "Level up!!!"}])
    #             game_engine.game_state = GAME_STATE.LEVEL_UP_WINDOW

    #         else:
    #             for flower in self.equipment.item_slot:
    #                 xp_to_next_level = flower.experience_per_level[flower.level+1]
    #                 if flower.current_xp >= xp_to_next_level and flower.max_level >= flower.level:
    #                     flower.level += 1
    #                     flower_list.append(flower)
    #                     game_engine.action_queue.extend([{"message": f"{flower.name} Level up!!!"}])
    #                     game_engine.game_state = GAME_STATE.LEVEL_UP_FLOWER
    #                     # flower.level_up()
    #                     break
    #                 else:
    #                     game_engine.game_state = GAME_STATE.NORMAL

    # def level_up(self):
    #     select = ["STR", "DEX", "INT"]
    #     bonus = choices(select, weights=[5, 2.5, 2.5])
    #     self.states_bonus.setdefault(bonus[0], 0)
    #     self.states_bonus[bonus[0]] += 1



    def update_animation(self, delta_time=1 / 60):
        super().update_animation(delta_time)

        if self.state == state.ON_MOVE and not self.left_face:
            self.texture = pc_move[0]
            
        if self.state == state.ON_MOVE and self.left_face:
            self.texture = pc_move[1]


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
